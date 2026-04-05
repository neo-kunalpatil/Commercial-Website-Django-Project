from django.db import models
from apps.orders.models import Order
import uuid

class Payment(models.Model):
    METHOD_CHOICES = (
        ('UPI', 'UPI / Scan and Pay'),
        ('COD', 'Cash on Delivery'),
    )
    
    STATUS_CHOICES = (
        ('PENDING', 'Pending Payment'),
        ('PROOF_SUBMITTED', 'Proof Submitted'),
        ('UNDER_VERIFICATION', 'Under Verification'),
        ('COMPLETED', 'Payment Confirmed'),
        ('REJECTED', 'Payment Rejected'),
        ('FAILED', 'Failed'),
        ('REFUNDED', 'Refunded'),
    )
    
    payment_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment')
    
    payment_method = models.CharField(max_length=20, choices=METHOD_CHOICES, default='UPI')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='PENDING')
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    
    # Buyer proof of payment
    proof_image = models.ImageField(upload_to='payment_proofs/', blank=True, null=True)
    
    # Seller verification
    rejection_reason = models.TextField(blank=True, null=True)
    verified_at = models.DateTimeField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Payment {self.payment_id} for Order {self.order.order_id}"
