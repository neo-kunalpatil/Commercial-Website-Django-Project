from django.urls import path
from . import views

urlpatterns = [
    # Seller Views
    path('manage/', views.seller_product_list, name='seller_product_list'),
    path('add/', views.product_create, name='product_create'),
    path('<int:pk>/edit/', views.product_update, name='product_update'),
    path('<int:pk>/delete/', views.product_delete, name='product_delete'),
    
    # Buyer Views
    path('', views.product_list, name='product_list'),
    path('categories/', views.category_list, name='category_list'),
    path('category/<slug:slug>/', views.category_products, name='category_products'),
    path('<int:pk>/', views.product_detail, name='product_detail'),
]
