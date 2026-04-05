from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),
    path('add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('update/<int:item_id>/', views.cart_update, name='cart_update'),
    path('remove/<int:item_id>/', views.cart_remove, name='cart_remove'),
    path('buy-now/<int:product_id>/', views.buy_now, name='buy_now'),
    path('save-for-later/<int:item_id>/', views.save_for_later, name='save_for_later'),
    path('move-to-cart/<int:item_id>/', views.move_to_cart_from_saved, name='move_to_cart_from_saved'),
    path('wishlist/', views.wishlist_view, name='wishlist_view'),
    path('wishlist/add/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:item_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
]
