from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('BUYER', 'Buyer'),
        ('SELLER', 'Seller'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='BUYER')

    def __str__(self):
        return f"{self.username} - {self.get_role_display()}"

    @property
    def is_buyer(self):
        return self.role == 'BUYER'

    @property
    def is_seller(self):
        return self.role == 'SELLER'

class Address(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='addresses')
    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=20)
    landmark = models.CharField(max_length=255, blank=True, null=True)
    is_default = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.is_default:
            Address.objects.filter(user=self.user).exclude(pk=self.pk).update(is_default=False)
        super(Address, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.full_name} - {self.city} ({self.pincode})"
