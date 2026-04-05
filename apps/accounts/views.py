from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm
from .models import Address
from apps.orders.models import Order
from apps.returns_app.models import ReturnRequest
from apps.cart.models import WishlistItem

def role_select(request):
    if request.user.is_authenticated:
        return redirect('profile')
    return render(request, 'accounts/role_select.html')

def register(request):
    if request.user.is_authenticated:
        return redirect('profile')
        
    role = request.GET.get('role', 'BUYER')
    if role not in ['BUYER', 'SELLER']:
        role = 'BUYER'

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = role
            user.save()
            messages.success(request, f'Account created successfully as {role}. You can now log in.')
            return redirect('login')
    else:
        # Pre-fill the role in the form if needed, though we set it explicitly above
        form = CustomUserCreationForm(initial={'role': role})

    return render(request, 'accounts/register.html', {'form': form, 'role': role})

@login_required
def profile(request):
    if request.user.is_seller:
        return redirect('seller_dashboard')
        
    recent_orders = Order.objects.filter(buyer=request.user).order_by('-created_at')[:3]
    active_returns_count = ReturnRequest.objects.filter(user=request.user).exclude(status__in=['REFUNDED', 'REJECTED']).count()
    wishlist_count = WishlistItem.objects.filter(wishlist__user=request.user).count()
    addresses = Address.objects.filter(user=request.user)
    default_address = addresses.filter(is_default=True).first() or addresses.first()

    context = {
        'recent_orders': recent_orders,
        'active_returns_count': active_returns_count,
        'wishlist_count': wishlist_count,
        'default_address': default_address,
        'addresses_count': addresses.count(),
    }
    return render(request, 'accounts/dashboard.html', context)

@login_required
def address_add(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        phone = request.POST.get('phone')
        address_line_1 = request.POST.get('address_line_1')
        address_line_2 = request.POST.get('address_line_2', '')
        city = request.POST.get('city')
        state = request.POST.get('state')
        pincode = request.POST.get('pincode')
        landmark = request.POST.get('landmark', '')
        is_default = request.POST.get('is_default') == 'on'

        Address.objects.create(
            user=request.user,
            full_name=full_name,
            phone=phone,
            address_line_1=address_line_1,
            address_line_2=address_line_2,
            city=city,
            state=state,
            pincode=pincode,
            landmark=landmark,
            is_default=is_default
        )
        messages.success(request, 'Address added successfully!')
        
        next_url = request.GET.get('next')
        if next_url:
            return redirect(next_url)
        return redirect('profile')

    return render(request, 'accounts/address_form.html')
