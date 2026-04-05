from django.db import models
from django.conf import settings
from apps.orders.models import Order
import uuid

class ReturnRequest(models.Model):
    STATUS_CHOICES = (
        ('REQUESTED', 'Return Requested'),
        ('APPROVED', 'Return Approved'),
        ('REJECTED', 'Return Rejected'),
        ('PICKUP_SCHEDULED', 'Pickup Scheduled'),
        ('PICKED_UP', 'Picked Up'),
        ('REFUND_PROCESSED', 'Refund Processed'),
        ('REFUNDED', 'Refund Completed'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='return_request')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='returns')
    
    reason = models.CharField(max_length=255)
    comment = models.TextField(blank=True, null=True)
    admin_notes = models.TextField(blank=True, null=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='REQUESTED')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Return {self.id} for Order {self.order.order_id}"
