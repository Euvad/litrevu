from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from tickets.models import Ticket
from reviews.models import Review
from social.models import UserFollows
# Create your views here.
class FeedView(LoginRequiredMixin, ListView):
    template_name = 'feed/feed.html'
    context_object_name = 'tickets'

    def get_queryset(self):
        # Get IDs of users followed by the current user
        followed_users = UserFollows.objects.filter(user=self.request.user).values_list('followed_user', flat=True)
        # Include tickets from followed users and the current user
        return Ticket.objects.filter(user__in=followed_users).union(Ticket.objects.filter(user=self.request.user))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Include reviews for tickets from followed users and the current user
        context['reviews'] = Review.objects.filter(
            ticket__user__in=self.get_queryset().values_list('user', flat=True)
        ).union(Review.objects.filter(ticket__user=self.request.user))
        return context

