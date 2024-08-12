from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from tickets.models import Ticket
from reviews.models import Review
from social.models import UserFollows

class FeedView(LoginRequiredMixin, ListView):
    template_name = 'feed/feed.html'
    context_object_name = 'tickets'

    def get_queryset(self):
        followed_users = UserFollows.objects.filter(user=self.request.user).values_list('followed_user', flat=True)
        tickets = Ticket.objects.filter(
            user__in=list(followed_users) + [self.request.user]
        ).order_by('created_at')  # Ascending order

        # Annotate tickets with a flag indicating if the user has reviewed it
        for ticket in tickets:
            ticket.has_reviewed = Review.objects.filter(ticket=ticket, user=self.request.user).exists()
            ticket.user_review = Review.objects.filter(ticket=ticket, user=self.request.user).first()  # Fetch user's review if it exists

        return tickets

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tickets'] = self.get_queryset()
        return context
