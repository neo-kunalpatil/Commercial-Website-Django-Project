from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='seller_dashboard'),
    path('profile/update/', views.profile_update, name='seller_profile_update'),
    path('payment/setup/', views.payment_setup, name='seller_payment_setup'),
    path('profile/<str:username>/', views.public_profile, name='seller_public_profile'),
    # Order Fulfillment
    path('orders/', views.seller_orders_list, name='seller_orders'),
    path('orders/<int:order_id>/', views.seller_order_detail, name='seller_order_detail'),
    
    # Placeholders map to existing views to avoid NoReverseMatch
    path('payments/', views.seller_payments, name='seller_payments'),
    path('returns/', views.seller_returns_list, name='seller_returns'),
    path('stock/', views.stock_management, name='seller_stock'),
]
