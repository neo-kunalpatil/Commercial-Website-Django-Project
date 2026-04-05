from .models import Cart

def cart_count(request):
    if request.user.is_authenticated and getattr(request.user, 'is_buyer', False):
        try:
            cart = Cart.objects.get(user=request.user)
            return {'cart_item_count': cart.get_item_count}
        except Cart.DoesNotExist:
            return {'cart_item_count': 0}
    return {'cart_item_count': 0}
