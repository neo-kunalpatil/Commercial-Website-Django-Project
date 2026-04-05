from django.db import models
from django.conf import settings

class SellerProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sellerprofile')
    business_name = models.CharField(max_length=255)
    business_email = models.EmailField(blank=True, null=True)
    business_phone = models.CharField(max_length=20, blank=True, null=True)
    gst_number = models.CharField(max_length=50, blank=True, null=True)
    business_address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    pincode = models.CharField(max_length=20, blank=True, null=True)
    verification_status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Payment Fields
    payment_receiver_name = models.CharField(max_length=255, blank=True, null=True)
    upi_id = models.CharField(max_length=100, blank=True, null=True)
    bank_name = models.CharField(max_length=100, blank=True, null=True)
    bank_account_number = models.CharField(max_length=50, blank=True, null=True)
    ifsc_code = models.CharField(max_length=20, blank=True, null=True)
    qr_code_image = models.ImageField(upload_to='qr_codes/', blank=True, null=True)
    payment_note = models.TextField(blank=True, null=True)
    is_payment_active = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.business_name} - {self.user.username}"


class SellerPayout(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('RELEASED', 'Released'),
        ('ON_HOLD', 'On Hold'),
    )
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='payouts')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    payout_date = models.DateField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payout ₹{self.amount} to {self.seller.username} [{self.status}]"
