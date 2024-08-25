from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from tickets.models import Ticket
from reviews.models import Review
from social.models import UserFollows
from itertools import chain

class BaseFeedView(LoginRequiredMixin, ListView):
    template_name = 'feed/feed.html'
    context_object_name = 'feed_items'

    def get_followed_users(self):
        """
        Retrieve the list of users that the current user follows.
        Returns a queryset of user IDs.
        """
        return UserFollows.objects.filter(user=self.request.user).values_list('followed_user', flat=True)

class FeedView(BaseFeedView):

    def get_queryset(self):
        """
        Retrieve the feed items based on the user's choice between 'my posts' or the general feed.
        If 'my_posts' is True, only the user's own posts (tickets and reviews) are returned.
        Otherwise, the feed consists of tickets from followed users and the current user.
        The tickets are annotated with information about whether the current user has reviewed them.
        """
        if self.request.GET.get('my_posts') == 'true':
            # Fetch only the current user's posts (tickets and reviews)
            tickets = Ticket.objects.filter(user=self.request.user).order_by('-created_at')
            reviews = Review.objects.filter(user=self.request.user).exclude(ticket__user=self.request.user).select_related('ticket').order_by('-created_at')
            return sorted(chain(tickets, reviews), key=lambda item: item.created_at, reverse=True)
        else:
            # Fetch posts from followed users and the current user
            followed_users = self.get_followed_users()
            tickets = Ticket.objects.filter(user__in=list(followed_users) + [self.request.user]).order_by('-created_at')
            
            # Use select_related to minimize queries and prefetch related reviews
            reviews = Review.objects.filter(ticket__in=tickets, user=self.request.user).select_related('ticket')

            # Create a dictionary to map tickets to their reviews
            review_map = {review.ticket_id: review for review in reviews}
            
            # Annotate tickets with information about whether the user has reviewed them
            for ticket in tickets:
                ticket.has_reviewed = ticket.id in review_map
                ticket.user_review = review_map.get(ticket.id)

            return tickets

    def get_context_data(self, **kwargs):
        """
        Add additional context to the template.
        Specifically, indicate whether the 'my_posts' filter is active.
        """
        context = super().get_context_data(**kwargs)
        context['my_posts'] = self.request.GET.get('my_posts') == 'true'
        return context
