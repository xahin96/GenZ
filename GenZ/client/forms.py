from django import forms
from .models import Rating

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['stars', 'feedback']
        widgets = {
            'stars': forms.RadioSelect,
            'feedback': forms.Textarea(attrs={'rows': 4}),
        }