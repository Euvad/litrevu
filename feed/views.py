from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from tickets.models import Ticket
from reviews.models import Review
from social.models import UserFollows
from itertools import chain

class FeedView(LoginRequiredMixin, ListView):
    template_name = 'feed/feed.html'
    context_object_name = 'feed_items'

    def get_queryset(self):
        my_posts = self.request.GET.get('my_posts') == 'true'

        if my_posts:
            # Get the user's own tickets
            tickets = Ticket.objects.filter(user=self.request.user).order_by('-created_at')

            # Get reviews the user made on other people's tickets
            reviews = Review.objects.filter(user=self.request.user).exclude(ticket__user=self.request.user).select_related('ticket')

            # Combine tickets and reviews into one list
            feed_items = sorted(
                chain(tickets, reviews),
                key=lambda item: item.created_at if hasattr(item, 'created_at') else item.ticket.created_at,
                reverse=True
            )
        else:
            # Show all tickets and reviews for the user and followed users
            followed_users = UserFollows.objects.filter(user=self.request.user).values_list('followed_user', flat=True)
            tickets = Ticket.objects.filter(user__in=list(followed_users) + [self.request.user]).order_by('-created_at')

            # Annotate tickets with a flag indicating if the user has reviewed them
            for ticket in tickets:
                ticket.has_reviewed = Review.objects.filter(ticket=ticket, user=self.request.user).exists()
                ticket.user_review = Review.objects.filter(ticket=ticket, user=self.request.user).first()

            feed_items = tickets

        return feed_items

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['feed_items'] = self.get_queryset()
        context['my_posts'] = self.request.GET.get('my_posts') == 'true'
        return context
