from django import forms
from .models import ReturnRequest

class ReturnRequestForm(forms.ModelForm):
    REASON_CHOICES = (
        ('Defective', 'Item is defective or doesn’t work'),
        ('Wrong Item', 'Received wrong item'),
        ('Not Needed', 'Item arrived too late or no longer needed'),
        ('Other', 'Other reason (Please explain below)'),
    )
    reason = forms.ChoiceField(choices=REASON_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}))
    comment = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Optional details...'}))

    class Meta:
        model = ReturnRequest
        fields = ['reason', 'comment']
