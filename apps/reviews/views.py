from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.products.models import Product
from apps.orders.models import Order
from .models import Review
from .forms import ReviewForm

@login_required
def add_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    # Verified Purchase Logic: Must have paid/processing order containing product
    valid_statuses = ['PROCESSING', 'SHIPPED', 'DELIVERED']
    is_verified_purchase = Order.objects.filter(
        buyer=request.user, 
        status__in=valid_statuses, 
        items__product=product
    ).exists()

    if not is_verified_purchase:
        messages.error(request, "You can only review products that you have successfully purchased.")
        return redirect('product_detail', pk=product_id)

    # Check if review already exists (so we update instead of duplicate)
    existing_review = Review.objects.filter(product=product, user=request.user).first()
    
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=existing_review)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.is_verified_purchase = is_verified_purchase
            review.save()
            messages.success(request, "Thank you for your review! It has been submitted.")
            return redirect('product_detail', pk=product_id)
    else:
        form = ReviewForm(instance=existing_review)
        
    return render(request, 'reviews/add_review.html', {
        'form': form,
        'product': product,
        'is_update': existing_review is not None
    })
