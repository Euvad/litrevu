from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views import View
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Review
from .forms import ReviewForm
from tickets.models import Ticket

class CreateReviewView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'reviews/create_review.html'
    success_url = reverse_lazy('feed')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class EditReviewView(LoginRequiredMixin, UpdateView):
    model = Review
    form_class = ReviewForm
    template_name = 'reviews/edit_review.html'
    success_url = reverse_lazy('feed')

    def get_queryset(self):
        return Review.objects.filter(user=self.request.user)


class DeleteReviewView(LoginRequiredMixin, DeleteView):
    model = Review
    template_name = 'reviews/delete_review.html'
    success_url = reverse_lazy('feed')

    def get_queryset(self):
        return Review.objects.filter(user=self.request.user)

class CreateReviewForTicketView(LoginRequiredMixin, View):
    def get(self, request, ticket_id, *args, **kwargs):
        ticket = get_object_or_404(Ticket, id=ticket_id)
        
        # Check if the user has already created a review for this ticket
        if Review.objects.filter(ticket=ticket, user=request.user).exists():
            messages.error(request, "You have already reviewed this ticket.")
            return redirect('feed')

        review_form = ReviewForm()
        return render(request, 'reviews/create_review_for_ticket.html', {
            'ticket': ticket,
            'review_form': review_form,
        })

    def post(self, request, ticket_id, *args, **kwargs):
        ticket = get_object_or_404(Ticket, id=ticket_id)
        
        # Check if the user has already created a review for this ticket
        if Review.objects.filter(ticket=ticket, user=request.user).exists():
            messages.error(request, "You have already reviewed this ticket.")
            return redirect('feed')

        review_form = ReviewForm(request.POST)
        
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            
            messages.success(request, 'Review created successfully.')
            return redirect('feed')
        else:
            messages.error(request, 'Please correct the errors below.')
        
        return render(request, 'reviews/create_review_for_ticket.html', {
            'ticket': ticket,
            'review_form': review_form,
        })
