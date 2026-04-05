from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.urls import reverse
from .models import Cart, CartItem, Wishlist, WishlistItem
from apps.products.models import Product

def buyer_check(user):
    return user.is_authenticated and getattr(user, 'is_buyer', False)

@login_required
@user_passes_test(buyer_check, login_url='/accounts/login/')
def cart_detail(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    active_items = cart.items.filter(is_saved_for_later=False).order_by('-created_at')
    saved_items = cart.items.filter(is_saved_for_later=True).order_by('-created_at')
    
    context = {
        'cart': cart,
        'items': active_items,
        'saved_items': saved_items,
    }
    return render(request, 'cart/cart_detail.html', context)

@login_required
@user_passes_test(buyer_check, login_url='/accounts/login/')
def cart_add(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        
        if product.stock < quantity:
            messages.error(request, f"Sorry, only {product.stock} items left in stock.")
            return redirect(request.META.get('HTTP_REFERER', '/'))

        cart_item, item_created = CartItem.objects.get_or_create(
            cart=cart, 
            product=product,
            defaults={'quantity': quantity}
        )
        
        if not item_created:
            if cart_item.quantity + quantity > product.stock:
                messages.error(request, "Cannot add more items, exceeds stock.")
            else:
                cart_item.quantity += quantity
                cart_item.save()
                messages.success(request, f"Updated {product.name} quantity in your cart.")
        else:
            messages.success(request, f"Added {product.name} to your cart.")
            
    return redirect('cart:cart_detail')

@login_required
@user_passes_test(buyer_check, login_url='/accounts/login/')
def cart_update(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        
        if quantity > 0 and quantity <= cart_item.product.stock:
            cart_item.quantity = quantity
            cart_item.save()
            messages.success(request, "Cart updated.")
        elif quantity <= 0:
            cart_item.delete()
            messages.success(request, "Item removed from cart.")
        else:
            messages.error(request, "Requested quantity exceeds available stock.")
            
    return redirect('cart:cart_detail')

@login_required
@user_passes_test(buyer_check, login_url='/accounts/login/')
def cart_remove(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    messages.success(request, "Item removed from your cart.")
    return redirect('cart:cart_detail')

@login_required
@user_passes_test(buyer_check, login_url='/accounts/login/')
def buy_now(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        
        if quantity > product.stock:
            messages.error(request, "Requested quantity exceeds stock.")
            return redirect(request.META.get('HTTP_REFERER', '/'))
            
        request.session['buy_now_item'] = {
            'product_id': product.id,
            'quantity': quantity
        }
        
        return redirect('orders:checkout')
        
    return redirect('cart:cart_detail')

# --- SAVE FOR LATER LOGIC ---

@login_required
@user_passes_test(buyer_check, login_url='/accounts/login/')
def save_for_later(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.is_saved_for_later = True
    cart_item.save()
    messages.success(request, f"{cart_item.product.name} saved for later.")
    return redirect('cart:cart_detail')

@login_required
@user_passes_test(buyer_check, login_url='/accounts/login/')
def move_to_cart_from_saved(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    if cart_item.quantity > cart_item.product.stock:
        messages.error(request, f"Sorry, only {cart_item.product.stock} left in stock. Adjust quantity to move to cart.")
        return redirect('cart:cart_detail')
    cart_item.is_saved_for_later = False
    cart_item.save()
    messages.success(request, f"{cart_item.product.name} moved back to active cart.")
    return redirect('cart:cart_detail')

# --- WISHLIST LOGIC ---

@login_required
@user_passes_test(buyer_check, login_url='/accounts/login/')
def wishlist_view(request):
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    return render(request, 'cart/wishlist.html', {'wishlist': wishlist})

@login_required
@user_passes_test(buyer_check, login_url='/accounts/login/')
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    WishlistItem.objects.get_or_create(wishlist=wishlist, product=product)
    messages.success(request, f"{product.name} added to your wishlist.")
    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required
@user_passes_test(buyer_check, login_url='/accounts/login/')
def remove_from_wishlist(request, item_id):
    item = get_object_or_404(WishlistItem, id=item_id, wishlist__user=request.user)
    item.delete()
    messages.success(request, "Item removed from wishlist.")
    return redirect(request.META.get('HTTP_REFERER', reverse('cart:wishlist_view')))
