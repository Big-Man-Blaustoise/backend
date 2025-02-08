# gym/forms.py
from django import forms
from .models import GymVisit

class GymVisitAdminForm(forms.ModelForm):
    class Meta:
        model = GymVisit
        fields = ['user', 'entry_time', 'exit_time', 'gym_location']
    
    entry_time = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    exit_time = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
