from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from apps.accounts.decorators import seller_required
from .models import SellerProfile
from .forms import SellerProfileForm
from apps.products.models import Product

@seller_required
def dashboard(request):
    try:
        profile = request.user.sellerprofile
    except SellerProfile.DoesNotExist:
        profile = None

    from django.db.models import Sum
    from apps.orders.models import Order
    from apps.returns_app.models import ReturnRequest

    total_products = Product.objects.filter(seller=request.user).count()
    active_products = Product.objects.filter(seller=request.user, available=True).count()
    out_of_stock = Product.objects.filter(seller=request.user, stock=0).count()
    
    orders = Order.objects.filter(seller=request.user)
    total_orders = orders.count()
    
    # Calculate Earnings (Only DELIVERED orders)
    earnings_query = orders.filter(status='DELIVERED').aggregate(Sum('total_amount'))
    total_earnings = earnings_query['total_amount__sum'] or 0.00
    from apps.payments.models import Payment

    user = request.user
    products = Product.objects.filter(seller=user)
    orders = Order.objects.filter(seller=user)
    
    # Pending Verifications count and amount
    pending_verifications = Payment.objects.filter(order__seller=user, status__in=['PROOF_SUBMITTED', 'UNDER_VERIFICATION']).count()
    pending_verification_earnings = Payment.objects.filter(
        order__seller=user, 
        status__in=['PROOF_SUBMITTED', 'UNDER_VERIFICATION']
    ).aggregate(Sum('amount'))['amount__sum'] or 0.00
    
    context = {
        'total_products': products.count(),
        'active_products': products.filter(available=True).count(),
        'out_of_stock': products.filter(stock=0).count(),
        'total_orders': orders.count(),
        'pending_orders': orders.filter(status__in=['PLACED', 'CONFIRMED', 'PACKED', 'SHIPPED', 'OUT_FOR_DELIVERY']).count(),
        'delivered_orders': orders.filter(status='DELIVERED').count(),
        'total_earnings': orders.filter(status='DELIVERED').aggregate(Sum('total_amount'))['total_amount__sum'] or 0.00,
        'recent_products': products.order_by('-created_at')[:5],
        'profile': profile,
        'return_requests': ReturnRequest.objects.filter(order__seller=user, status='REQUESTED').count(),
        'pending_verifications': pending_verifications,
        'pending_verification_earnings': pending_verification_earnings,
    }
    return render(request, 'sellers/dashboard.html', context)

@seller_required
def stock_management(request):
    products = Product.objects.filter(seller=request.user).order_by('-created_at')
    
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        new_stock = request.POST.get('stock')
        if product_id and new_stock is not None:
            try:
                product = Product.objects.get(id=product_id, seller=request.user)
                product.stock = max(0, int(new_stock))
                product.save()
                messages.success(request, f"Stock updated for {product.name}")
            except (Product.DoesNotExist, ValueError):
                messages.error(request, "Error updating stock.")
        return redirect('seller_stock')
        
    return render(request, 'sellers/stock_management.html', {'products': products})

@seller_required
def seller_orders_list(request):
    from apps.orders.models import Order
    orders = Order.objects.filter(seller=request.user).order_by('-created_at')
    
    # Filter by status if provided
    status = request.GET.get('status')
    if status:
        orders = orders.filter(status=status)
        
    return render(request, 'sellers/seller_orders_list.html', {
        'orders': orders,
        'current_status': status
    })

@seller_required
def seller_order_detail(request, order_id):
    from apps.orders.models import Order
    order = get_object_or_404(Order, id=order_id, seller=request.user)
    
    if request.method == 'POST':
        # Update Order Status and Tracking info
        new_status = request.POST.get('status')
        tracking_id = request.POST.get('tracking_id')
        courier_name = request.POST.get('courier_name')
        
        if new_status and new_status in dict(Order.STATUS_CHOICES).keys():
            order.status = new_status
            
        if tracking_id is not None:
            order.tracking_id = tracking_id
        if courier_name is not None:
            order.courier_name = courier_name
            
        order.save()
        messages.success(request, f"Order #{order.id} updated successfully.")
        return redirect('seller_order_detail', order_id=order.id)
        
    return render(request, 'sellers/seller_order_detail.html', {'order': order})

@seller_required
def seller_returns_list(request):
    from apps.returns_app.models import ReturnRequest
    returns = ReturnRequest.objects.filter(order__seller=request.user).order_by('-created_at')
    
    if request.method == 'POST':
        return_id = request.POST.get('return_id')
        new_status = request.POST.get('status')
        admin_notes = request.POST.get('admin_notes')
        
        if return_id and new_status:
            try:
                ret = ReturnRequest.objects.get(id=return_id, order__seller=request.user)
                ret.status = new_status
                if admin_notes:
                    ret.admin_notes = admin_notes
                ret.save()

                # Jointing: Sync Order status based on Return progress
                order = ret.order
                if new_status in ['APPROVED', 'PICKUP_SCHEDULED', 'PICKED_UP']:
                    order.status = 'RETURNED'
                elif new_status in ['REFUND_PROCESSED', 'REFUNDED']:
                    order.status = 'REFUNDED'
                order.save()
                
                messages.success(request, f"Return request #{ret.id} updated and Order status synced to {order.get_status_display()}.")
            except ReturnRequest.DoesNotExist:
                messages.error(request, "Return request not found.")
        return redirect('seller_returns')
        
    return render(request, 'sellers/seller_returns_list.html', {'returns': returns})

@seller_required
def seller_payments(request):
    from django.db.models import Sum
    from django.utils import timezone
    from datetime import timedelta
    from apps.orders.models import Order
    from .models import SellerPayout
    
    now = timezone.now()
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    week_start = today_start - timedelta(days=today_start.weekday())
    month_start = today_start.replace(day=1)

    all_delivered = Order.objects.filter(seller=request.user, status='DELIVERED')
    
    # Calculate pending earnings (Confirmed but not delivered)
    pending_earnings = Order.objects.filter(
        seller=request.user, 
        status__in=['PLACED', 'CONFIRMED', 'PACKED', 'SHIPPED', 'OUT_FOR_DELIVERY']
    ).aggregate(Sum('total_amount'))['total_amount__sum'] or 0.00

    # New: Pending Verification (Buyer submitted but seller hasn't confirmed)
    from apps.payments.models import Payment
    pending_verification_earnings = Payment.objects.filter(
        order__seller=request.user,
        status__in=['PROOF_SUBMITTED', 'UNDER_VERIFICATION']
    ).aggregate(Sum('amount'))['amount__sum'] or 0.00
    
    total_earnings = all_delivered.aggregate(Sum('total_amount'))['total_amount__sum'] or 0.00
    today_earnings = all_delivered.filter(updated_at__gte=today_start).aggregate(Sum('total_amount'))['total_amount__sum'] or 0.00
    week_earnings = all_delivered.filter(updated_at__gte=week_start).aggregate(Sum('total_amount'))['total_amount__sum'] or 0.00
    month_earnings = all_delivered.filter(updated_at__gte=month_start).aggregate(Sum('total_amount'))['total_amount__sum'] or 0.00
    
    # Pending earnings = CONFIRMED, PACKED, SHIPPED
    pending_orders = Order.objects.filter(seller=request.user, status__in=['CONFIRMED', 'PACKED', 'SHIPPED'])
    pending_earnings = pending_orders.aggregate(Sum('total_amount'))['total_amount__sum'] or 0.00
    
    # Payouts
    payouts = SellerPayout.objects.filter(seller=request.user).order_by('-created_at')
    released_payouts = payouts.filter(status='RELEASED').aggregate(Sum('amount'))['amount__sum'] or 0.00
    
    try:
        has_payment_setup = bool(request.user.sellerprofile.bank_account_number or request.user.sellerprofile.upi_id)
    except Exception:
        has_payment_setup = False
    
    return render(request, 'sellers/seller_payments.html', {
        'total_earnings': total_earnings,
        'today_earnings': today_earnings,
        'week_earnings': week_earnings,
        'month_earnings': month_earnings,
        'pending_earnings': pending_earnings,
        'pending_verification_earnings': pending_verification_earnings,
        'released_payouts': released_payouts,
        'recent_transactions': all_delivered.order_by('-updated_at')[:15],
        'payouts': payouts[:10],
        'has_payment_setup': has_payment_setup,
    })

@seller_required
def profile_update(request):
    try:
        profile = request.user.sellerprofile
    except SellerProfile.DoesNotExist:
        profile = None

    if request.method == 'POST':
        form = SellerProfileForm(request.POST, instance=profile)
        if form.is_valid():
            new_profile = form.save(commit=False)
            new_profile.user = request.user
            new_profile.save()
            messages.success(request, 'Seller profile updated successfully!')
            return redirect('seller_dashboard')
    else:
        form = SellerProfileForm(instance=profile)

    return render(request, 'sellers/seller_profile_form.html', {'form': form})

from .forms import SellerPaymentSetupForm

@seller_required
def payment_setup(request):
    try:
        profile = request.user.sellerprofile
    except SellerProfile.DoesNotExist:
        messages.error(request, 'Please complete your main seller profile first.')
        return redirect('seller_profile_update')
        
    if request.method == 'POST':
        form = SellerPaymentSetupForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Payment receiving configurations updated successfully!')
            return redirect('seller_dashboard')
    else:
        form = SellerPaymentSetupForm(instance=profile)
        
    return render(request, 'sellers/payment_setup.html', {'form': form})

def public_profile(request, username):
    from apps.accounts.models import CustomUser
    seller_user = get_object_or_404(CustomUser, username=username, role='SELLER')
    profile = get_object_or_404(SellerProfile, user=seller_user)
    products = Product.objects.filter(seller=seller_user, available=True).order_by('-created_at')
    
    return render(request, 'sellers/public_profile.html', {
        'seller': seller_user,
        'profile': profile,
        'products': products,
    })
