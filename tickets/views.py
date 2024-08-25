from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views import View
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Ticket
from .forms import TicketForm
from reviews.forms import ReviewForm


# Create your views here.
class CreateTicketView(LoginRequiredMixin, CreateView):
    model = Ticket
    form_class = TicketForm
    template_name = "tickets/create_ticket.html"
    success_url = reverse_lazy("feed")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class EditTicketView(LoginRequiredMixin, UpdateView):
    model = Ticket
    form_class = TicketForm
    template_name = "tickets/edit_ticket.html"
    success_url = reverse_lazy("feed")

    def get_queryset(self):
        return Ticket.objects.filter(user=self.request.user)


class DeleteTicketView(LoginRequiredMixin, DeleteView):
    model = Ticket
    template_name = "tickets/delete_ticket.html"
    success_url = reverse_lazy("feed")

    def get_queryset(self):
        return Ticket.objects.filter(user=self.request.user)


class CreateTicketReviewView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        ticket_form = TicketForm()
        review_form = ReviewForm()
        return render(
            request,
            "tickets/create_ticket_review.html",
            {
                "ticket_form": ticket_form,
                "review_form": review_form,
            },
        )

    def post(self, request, *args, **kwargs):
        ticket_form = TicketForm(request.POST, request.FILES)
        review_form = ReviewForm(request.POST)

        if ticket_form.is_valid() and review_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()

            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()

            messages.success(request, "Ticket and review created successfully.")
            return redirect("feed")
        else:
            messages.error(request, "Please correct the errors below.")

        return render(
            request,
            "tickets/create_ticket_review.html",
            {
                "ticket_form": ticket_form,
                "review_form": review_form,
            },
        )
