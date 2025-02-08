# gym/forms.py
from django import forms
from .models import GymVisit


class GymVisitAdminForm(forms.ModelForm):
    class Meta:
        model = GymVisit
        fields = ['user', 'entry_time', 'gym_location', 'gym_busy_rating']

    gym_busy_rating = forms.ChoiceField(
        choices=GymVisit._meta.get_field('gym_busy_rating').choices,
        widget=forms.Select
    )
