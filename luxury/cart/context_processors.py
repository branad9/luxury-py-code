from .models import CartItem


def cart_counter(request):
    count = 0
    if not request.user.is_authenticated:
        return {'cp_cart_count': count}
    try:
        cart_items = CartItem.objects.filter(user=request.user)
        for item in cart_items:
            count += item.qty
    except CartItem.DoesNotExist:
        count = 0
    return {'cp_cart_count': count}

