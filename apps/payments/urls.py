from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('gateway/<uuid:order_id>/', views.payment_gateway, name='payment_gateway'),
    path('callback/success/<uuid:order_id>/', views.payment_success, name='payment_success'),
    path('callback/failed/<uuid:order_id>/', views.payment_failed, name='payment_failed'),
    path('success/<uuid:order_id>/', views.success_page, name='success_page'),
    path('receipt/<uuid:order_id>/', views.receipt_view, name='receipt_view'),
    # Seller Verification URLs
    path('verify/', views.payment_verification_list, name='payment_verification_list'),
    path('verify/<uuid:payment_id>/', views.verify_payment, name='verify_payment'),
]
