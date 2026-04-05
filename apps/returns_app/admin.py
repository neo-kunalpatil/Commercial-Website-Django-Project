from django.contrib import admin
from .models import ReturnRequest

@admin.register(ReturnRequest)
class ReturnRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'user', 'status', 'created_at')
    list_filter = ('status', 'created_at')
