from django.contrib import admin
from .models import SellerProfile

@admin.register(SellerProfile)
class SellerProfileAdmin(admin.ModelAdmin):
    list_display = ('business_name', 'user', 'verification_status', 'created_at')
    list_filter = ('verification_status',)
    search_fields = ('business_name', 'user__username', 'business_email')
