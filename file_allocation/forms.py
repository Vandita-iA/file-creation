# file_allocation/forms.py

from django import forms
from .models import Campaign

class DataFilterForm(forms.Form):
    campaign_name = forms.ModelChoiceField(queryset=Campaign.objects.all())
    last_updated_group1_values = forms.ChoiceField(choices=[], required=False)
    # Add other multiple choice fields as needed
