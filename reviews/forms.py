from django import forms
from .models import Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["rating", "headline", "body"]  # Include all necessary fields

    def clean_rating(self):
        rating = self.cleaned_data.get("rating")
        if rating is None:
            raise forms.ValidationError("Rating is required.")
        if rating < 1 or rating > 5:
            raise forms.ValidationError("Rating must be between 1 and 5.")
        return rating


class TicketReviewForm(forms.Form):
    ticket_title = forms.CharField(max_length=128, label="Ticket Title")
    ticket_description = forms.CharField(
        widget=forms.Textarea, label="Ticket Description", required=False
    )
    review_rating = forms.IntegerField(
        min_value=0,
        max_value=5,
        label="Review Rating",
        widget=forms.NumberInput(attrs={"type": "range", "min": 0, "max": 5}),
    )
    review_headline = forms.CharField(max_length=128, label="Review Headline")
    review_body = forms.CharField(
        widget=forms.Textarea, label="Review Body", required=False
    )
