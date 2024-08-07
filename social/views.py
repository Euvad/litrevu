from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib import messages
from django.views import View
from django.views.generic import ListView, FormView
from .models import UserFollows
from .forms import FollowForm

# Create your views here.

class ListFollowedUsersView(LoginRequiredMixin, ListView):
    model = UserFollows
    template_name = 'socials/list_followed_users.html'
    context_object_name = 'followed_users'

    def get_queryset(self):
        return UserFollows.objects.filter(user=self.request.user)


class AddFollowView(LoginRequiredMixin, FormView):
    template_name = 'socials/add_follow.html'
    form_class = FollowForm

    def form_valid(self, form):
        if 'search' in self.request.POST:
            username = form.cleaned_data['username']
            search_results = User.objects.filter(username__icontains=username).exclude(id=self.request.user.id)
            if not search_results:
                messages.error(self.request, 'No users found with that username.')
            return self.render_to_response(self.get_context_data(form=form, search_results=search_results))

        elif 'follow' in self.request.POST:
            try:
                username_to_follow = self.request.POST.get('username')
                user_to_follow = User.objects.get(username=username_to_follow)
                if user_to_follow != self.request.user:
                    UserFollows.objects.get_or_create(user=self.request.user, followed_user=user_to_follow)
                    messages.success(self.request, f'You are now following {user_to_follow.username}.')
                else:
                    messages.error(self.request, "You cannot follow yourself.")
            except User.DoesNotExist:
                messages.error(self.request, 'User does not exist.')
            return redirect('list_followed_users')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.setdefault('search_results', [])
        return context


class RemoveFollowView(LoginRequiredMixin, View):
    def post(self, request, follow_id):
        follow = get_object_or_404(UserFollows, id=follow_id, user=request.user)
        follow.delete()
        messages.success(request, f'You have unfollowed {follow.followed_user.username}.')
        return redirect('list_followed_users')

