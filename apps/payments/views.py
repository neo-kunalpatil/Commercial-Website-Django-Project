from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from apps.orders.models import Order
from apps.accounts.decorators import seller_required
from .models import Payment


@login_required
def payment_gateway(request, order_id):
    order = get_object_or_404(Order, order_id=order_id, buyer=request.user)

    if order.status not in ['PENDING_PAYMENT', 'PLACED']:
        # Allow re-upload if payment was rejected
        try:
            if order.payment.status == 'REJECTED':
                pass  # Allow through
            else:
                messages.info(request, "This order is already processed.")
                return redirect('orders:order_history')
        except Payment.DoesNotExist:
            pass

    # Check if there is a rejected payment
    rejected_payment = None
    try:
        p = order.payment
        if p.status == 'REJECTED':
            rejected_payment = p
    except Exception:
        pass

    try:
        seller_profile = order.seller.sellerprofile
    except Exception:
        seller_profile = None

    context = {
        'order': order,
        'profile': seller_profile,
        'rejected_payment': rejected_payment,
    }
    return render(request, 'payments/upi_qr_payment.html', context)


@login_required
def payment_success(request, order_id):
    order = get_object_or_404(Order, order_id=order_id, buyer=request.user)

    if request.method == 'POST':
        transaction_id = request.POST.get('transaction_id', '').strip()
        proof_image = request.FILES.get('proof_image')

        if not transaction_id or len(transaction_id) < 4:
            messages.error(request, 'Please enter a valid UPI Transaction ID / Reference Number.')
            return redirect('payments:payment_gateway', order_id=order.order_id)

        # Check if re-submitting (rejected payment)
        try:
            existing_payment = order.payment
            if existing_payment.status == 'REJECTED':
                existing_payment.transaction_id = transaction_id
                existing_payment.status = 'PROOF_SUBMITTED'
                existing_payment.rejection_reason = None
                if proof_image:
                    existing_payment.proof_image = proof_image
                existing_payment.save()
                order.status = 'PLACED'
                order.save()
                messages.success(request, 'Payment proof re-submitted! The seller will verify shortly.')
                return redirect('orders:order_detail', order_id=order.order_id)
        except Payment.DoesNotExist:
            pass

        # Create new Payment with PROOF_SUBMITTED status
        Payment.objects.create(
            order=order,
            payment_method='UPI',
            amount=order.total_amount,
            status='PROOF_SUBMITTED',
            transaction_id=transaction_id,
            proof_image=proof_image if proof_image else None,
        )

        # Order moves to PLACED (awaiting seller verification)
        order.status = 'PLACED'
        order.save()

        messages.success(request, 'Payment proof submitted! The seller will verify and confirm your order shortly.')
        return redirect('payments:success_page', order_id=order.order_id)

    return redirect('payments:payment_gateway', order_id=order.order_id)


@login_required
def success_page(request, order_id):
    order = get_object_or_404(Order, order_id=order_id, buyer=request.user)
    return render(request, 'payments/payment_success.html', {'order': order})


@login_required
def payment_failed(request, order_id):
    order = get_object_or_404(Order, order_id=order_id, buyer=request.user)
    return render(request, 'payments/payment_failed.html', {'order': order})


@login_required
def receipt_view(request, order_id):
    order = get_object_or_404(Order, order_id=order_id, buyer=request.user)

    # Allow access for reports if proof is submitted
    try:
        payment = order.payment
        # No longer blocking: we will show the status on the receipt itself
    except Exception:
        messages.error(request, 'No payment found for this order. Please complete payment first.')
        return redirect('payments:payment_gateway', order_id=order.order_id)

    return render(request, 'payments/receipt.html', {'order': order})


# ── SELLER VIEWS ──────────────────────────────────────────────────────────────

@seller_required
def payment_verification_list(request):
    """Seller sees all orders with proof submitted awaiting verification."""
    pending_payments = Payment.objects.filter(
        order__seller=request.user,
        status__in=['PROOF_SUBMITTED', 'UNDER_VERIFICATION']
    ).select_related('order', 'order__buyer').order_by('-created_at')

    completed_payments = Payment.objects.filter(
        order__seller=request.user,
        status='COMPLETED'
    ).select_related('order', 'order__buyer').order_by('-verified_at')[:20]

    rejected_payments = Payment.objects.filter(
        order__seller=request.user,
        status='REJECTED'
    ).select_related('order', 'order__buyer').order_by('-updated_at')[:10]

    context = {
        'pending_payments': pending_payments,
        'completed_payments': completed_payments,
        'rejected_payments': rejected_payments,
    }
    return render(request, 'sellers/payment_verification.html', context)


@seller_required
def verify_payment(request, payment_id):
    """Seller confirms or rejects a specific payment proof."""
    payment = get_object_or_404(Payment, payment_id=payment_id, order__seller=request.user)

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'confirm':
            payment.status = 'COMPLETED'
            payment.verified_at = timezone.now()
            payment.rejection_reason = None
            payment.save()

            # Confirm order and update stock
            order = payment.order
            order.status = 'CONFIRMED'
            order.save()

            for item in order.items.all():
                if item.product and item.product.stock >= item.quantity:
                    item.product.stock -= item.quantity
                    item.product.save()

            messages.success(request, f'Payment for Order #{str(order.order_id)[:8]} confirmed! Order is now active.')

        elif action == 'reject':
            reason = request.POST.get('rejection_reason', '').strip()
            if not reason:
                messages.error(request, 'Please provide a rejection reason.')
                return redirect('payments:verify_payment', payment_id=payment_id)

            payment.status = 'REJECTED'
            payment.rejection_reason = reason
            payment.save()

            # Revert order to pending
            order = payment.order
            order.status = 'PENDING_PAYMENT'
            order.save()

            messages.warning(request, f'Payment rejected. Buyer has been notified to re-submit proof.')

        return redirect('payments:payment_verification_list')

    # GET — show the verification detail page
    return render(request, 'sellers/verify_payment_detail.html', {'payment': payment})
