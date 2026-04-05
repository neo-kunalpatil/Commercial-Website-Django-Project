from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from apps.orders.models import Order
from .models import ReturnRequest
from .forms import ReturnRequestForm

def buyer_check(user):
    return user.is_authenticated and getattr(user, 'is_buyer', False)

@login_required
@user_passes_test(buyer_check, login_url='/accounts/login/')
def request_return(request, order_id):
    order = get_object_or_404(Order, order_id=order_id, buyer=request.user)
    
    # Status Validation: Allow for testing (PLACED/CONFIRMED) or final (DELIVERED)
    if order.status not in ['DELIVERED', 'PLACED', 'CONFIRMED']:
        messages.error(request, "You can only return items that have been placed, confirmed, or delivered.")
        return redirect('orders:order_detail', order_id=order_id)
        
    if hasattr(order, 'return_request'):
        messages.warning(request, "A return request already exists for this order.")
        return redirect('returns:return_list')
        
    if request.method == 'POST':
        form = ReturnRequestForm(request.POST)
        if form.is_valid():
            return_req = form.save(commit=False)
            return_req.order = order
            return_req.user = request.user
            return_req.save()
            messages.success(request, f"Return requested securely for order {order.order_id}.")
            return redirect('returns:return_list')
    else:
        form = ReturnRequestForm()
        
    return render(request, 'returns/request_return.html', {'form': form, 'order': order})

@login_required
@user_passes_test(buyer_check, login_url='/accounts/login/')
def return_list(request):
    returns = ReturnRequest.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'returns/return_list.html', {'returns': returns})
