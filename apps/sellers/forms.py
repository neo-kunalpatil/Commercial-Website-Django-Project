from django import forms
from .models import SellerProfile

class SellerProfileForm(forms.ModelForm):
    class Meta:
        model = SellerProfile
        exclude = ('user', 'verification_status')
        widgets = {
            'business_name': forms.TextInput(attrs={'class': 'form-control'}),
            'business_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'business_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'gst_number': forms.TextInput(attrs={'class': 'form-control'}),
            'business_address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'pincode': forms.TextInput(attrs={'class': 'form-control'}),
        }

class SellerPaymentSetupForm(forms.ModelForm):
    class Meta:
        model = SellerProfile
        fields = ('payment_receiver_name', 'upi_id', 'bank_name', 'bank_account_number', 'ifsc_code', 'qr_code_image', 'payment_note', 'is_payment_active')
        widgets = {
            'payment_receiver_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Ramesh Electronics'}),
            'upi_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 9876543210@paytm'}),
            'bank_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. HDFC Bank'}),
            'bank_account_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 50100123456789'}),
            'ifsc_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. HDFC0001234'}),
            'qr_code_image': forms.FileInput(attrs={'class': 'form-control'}),
            'payment_note': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Optional instructions... E.g. Please share screenshot on whatsapp.'}),
            'is_payment_active': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }
