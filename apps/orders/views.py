from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from apps.cart.models import Cart
from apps.accounts.models import Address
from apps.products.models import Product
from .models import Order, OrderItem
from apps.returns_app.models import ReturnRequest

def buyer_check(user):
    return user.is_authenticated and getattr(user, 'is_buyer', False)

@login_required
@user_passes_test(buyer_check, login_url='/accounts/login/')
def checkout(request):
    addresses = Address.objects.filter(user=request.user)
    
    # Check if this is a Buy Now flow
    buy_now_item = request.session.get('buy_now_item')
    
    if buy_now_item:
        product = get_object_or_404(Product, id=buy_now_item['product_id'])
        quantity = buy_now_item['quantity']
        
        # Mock a cart-like structure for the template
        class MockItem:
            def __init__(self, product, quantity):
                self.product = product
                self.quantity = quantity
                self.get_cost = product.price * quantity
                
        mock_item = MockItem(product, quantity)
        subtotal = mock_item.get_cost
        discount = 0
        shipping = 0 # Placeholder
        total = subtotal - discount + shipping
        
        context = {
            'items': [mock_item],
            'subtotal': subtotal,
            'discount': discount,
            'shipping': shipping,
            'total': total,
            'item_count': quantity,
            'addresses': addresses,
            'is_buy_now': True
        }
    else:
        # Standard Cart checkout flow
        try:
            cart = Cart.objects.get(user=request.user)
            items = cart.items.filter(is_saved_for_later=False)
            
            if not items.exists():
                messages.warning(request, "Your cart is empty.")
                return redirect('cart:cart_detail')
                
            context = {
                'items': items,
                'subtotal': cart.get_subtotal,
                'discount': cart.get_discount,
                'shipping': cart.get_shipping,
                'total': cart.get_total,
                'item_count': cart.get_item_count,
                'addresses': addresses,
                'is_buy_now': False
            }
        except Cart.DoesNotExist:
            messages.warning(request, "Your cart is empty.")
            return redirect('cart:cart_detail')
            
    if request.method == 'POST':
        address_id = request.POST.get('address_id')
        if not address_id:
            messages.error(request, "Please select a delivery address.")
            return redirect('orders:checkout')
            
        try:
            shipping_address = Address.objects.get(id=address_id, user=request.user)
        except Address.DoesNotExist:
            messages.error(request, "Invalid address selected.")
            return redirect('orders:checkout')
            
        # Group items by seller
        seller_items = {}
        for item in context['items']:
            seller = item.product.seller
            if seller not in seller_items:
                seller_items[seller] = []
            seller_items[seller].append(item)
            
        created_orders = []
        for seller, s_items in seller_items.items():
            # Calculate totals per seller
            s_subtotal = sum((i.get_cost if hasattr(i, 'get_cost') else i.get_subtotal()) for i in s_items)
            
            addr_str = f"{shipping_address.address_line_1}, {shipping_address.address_line_2}"
            
            order = Order.objects.create(
                buyer=request.user,
                seller=seller,
                full_name=shipping_address.full_name,
                phone=shipping_address.phone,
                shipping_address=addr_str,
                city=shipping_address.city,
                state=shipping_address.state,
                pincode=shipping_address.pincode,
                subtotal=s_subtotal,
                shipping_charge=0.00,
                discount=0.00,
                total_amount=s_subtotal,
                status='PENDING_PAYMENT'
            )
            
            for item in s_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    product_name=item.product.name,
                    quantity=item.quantity,
                    price=item.product.price
                )
            created_orders.append(order)
            
        # Clear buy now session or actual cart
        if 'buy_now_item' in request.session:
            del request.session['buy_now_item']
        else:
            try:
                Cart.objects.get(user=request.user).items.filter(is_saved_for_later=False).delete()
            except Cart.DoesNotExist:
                pass
            
        if len(created_orders) > 1:
            messages.success(request, f"Your cart items were split into {len(created_orders)} separate orders. Please proceed with payment.")
        else:
            messages.success(request, "Order generated! Please complete your payment.")
            
        return redirect('payments:payment_gateway', order_id=created_orders[0].order_id)

    return render(request, 'orders/checkout.html', context)

@login_required
@user_passes_test(buyer_check, login_url='/accounts/login/')
def order_history(request):
    orders = Order.objects.filter(buyer=request.user).order_by('-created_at')
    
    pending_orders = orders.filter(status='PENDING_PAYMENT')
    active_orders = orders.exclude(status__in=['PENDING_PAYMENT', 'CANCELLED', 'DELIVERED'])
    past_orders = orders.filter(status='DELIVERED')
    cancelled_orders = orders.filter(status='CANCELLED')
    
    return render(request, 'orders/order_history.html', {
        'pending_orders': pending_orders,
        'active_orders': active_orders,
        'past_orders': past_orders,
        'cancelled_orders': cancelled_orders,
    })

@login_required
@user_passes_test(buyer_check, login_url='/accounts/login/')
def order_detail(request, order_id):
    order = get_object_or_404(Order, order_id=order_id, buyer=request.user)
    
    # Updated Tracking Timeline for realistic marketplace
    timeline = [
        ('PENDING_PAYMENT', 'Payment Pending'),
        ('PLACED', 'Proof Submitted'),
        ('CONFIRMED', 'Payment Confirmed'),
        ('PACKED', 'Packed'),
        ('SHIPPED', 'Shipped'),
        ('OUT_FOR_DELIVERY', 'Out for Delivery'),
        ('DELIVERED', 'Delivered')
    ]
    
    status_list = [step[0] for step in timeline]
    try:
        current_index = status_list.index(order.status)
    except ValueError:
        if order.status == 'CANCELLED':
            current_index = -2 # Special case for cancelled
        else:
            current_index = 0 # Default to start
        
    # Check for payment state
    payment = None
    try:
        payment = order.payment
    except Exception:
        pass
        
    # Check for return request
    try:
        return_req = order.return_request
        has_return = True
    except ReturnRequest.DoesNotExist:
        return_req = None
        has_return = False
        
    return render(request, 'orders/order_detail.html', {
        'order': order,
        'timeline': timeline,
        'current_index': current_index,
        'has_return': has_return,
        'return_req': return_req
    })

@login_required
@user_passes_test(buyer_check, login_url='/accounts/login/')
def cancel_order(request, order_id):
    if request.method == 'POST':
        order = get_object_or_404(Order, order_id=order_id, buyer=request.user)
        if order.status in ['PENDING_PAYMENT', 'PLACED', 'CONFIRMED']:
            order.status = 'CANCELLED'
            order.save()
            messages.success(request, f"Order {order.order_id} has been fully cancelled.")
        else:
            messages.error(request, "This order cannot be cancelled as it has already progressed.")
    return redirect('orders:order_detail', order_id=order_id)
