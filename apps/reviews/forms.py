from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'headline', 'comment']
        widgets = {
            'rating': forms.Select(choices=[(i, f'{i} Stars') for i in reversed(range(1, 6))], attrs={'class': 'form-select'}),
            'headline': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "What's most important to know?"}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': "What did you like or dislike? What did you use this product for?"}),
        }
