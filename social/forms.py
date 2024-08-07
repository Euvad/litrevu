from django import forms

class FollowForm(forms.Form):
    username = forms.CharField(max_length=150, label='Search User to Follow')
