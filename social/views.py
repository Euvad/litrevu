from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib import messages
from django.views import View
from django.views.generic import ListView, FormView
from .models import UserFollows
from .forms import FollowForm

# View to display the list of users followed by the current user
class ListFollowedUsersView(LoginRequiredMixin, ListView):
    model = UserFollows  # The model used for this view
    template_name = "socials/list_followed_users.html"  # The template to render the list
    context_object_name = "followed_users"  # The name used for the context in the template

    # Custom queryset to filter only the users followed by the current user
    def get_queryset(self):
        return UserFollows.objects.filter(user=self.request.user)

# View to handle adding a new user to the list of followed users
class AddFollowView(LoginRequiredMixin, FormView):
    template_name = "socials/add_follow.html"  # The template for the follow form
    form_class = FollowForm  # The form class used in this view

    # Method called when the form is valid
    def form_valid(self, form):
        # Check if the "search" button was clicked
        if "search" in self.request.POST:
            username = form.cleaned_data["username"]  # Get the username from the form
            search_results = User.objects.filter(username__icontains=username).exclude(
                id=self.request.user.id  # Exclude the current user from search results
            )
            # If no users found, display an error message
            if not search_results:
                messages.error(self.request, "No users found with that username.")
            # Re-render the form with the search results
            return self.render_to_response(
                self.get_context_data(form=form, search_results=search_results)
            )

        # Check if the "follow" button was clicked
        elif "follow" in self.request.POST:
            try:
                username_to_follow = self.request.POST.get("username")  # Get the username to follow
                user_to_follow = User.objects.get(username=username_to_follow)
                # Ensure the user is not trying to follow themselves
                if user_to_follow != self.request.user:
                    # Create a new follow relationship if it doesn't exist
                    UserFollows.objects.get_or_create(
                        user=self.request.user, followed_user=user_to_follow
                    )
                    # Display success message
                    messages.success(
                        self.request,
                        f"You are now following {user_to_follow.username}.",
                    )
                else:
                    messages.error(self.request, "You cannot follow yourself.")
            except User.DoesNotExist:
                messages.error(self.request, "User does not exist.")
            # Redirect to the list of followed users after following
            return redirect("list_followed_users")

    # Method to add additional context to the template
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Ensure 'search_results' is always in the context, even if empty
        context.setdefault("search_results", [])
        return context

# View to handle unfollowing a user
class RemoveFollowView(LoginRequiredMixin, View):
    # Handle POST requests to remove a follow relationship
    def post(self, request, follow_id):
        # Ensure the follow relationship exists and belongs to the current user
        follow = get_object_or_404(UserFollows, id=follow_id, user=request.user)
        follow.delete()  # Delete the follow relationship
        # Display success message after unfollowing
        messages.success(
            request, f"You have unfollowed {follow.followed_user.username}."
        )
        # Redirect to the list of followed users after unfollowing
        return redirect("list_followed_users")
