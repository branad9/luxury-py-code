from .models import Wishlist


def wishlist_counter(request):
    count = 0
    if not request.user.is_authenticated:
        return {'cp_wishlist_count': count}
    try:
        count = Wishlist.objects.filter(user=request.user).count()
    except Wishlist.DoesNotExist:
        count = 0
    return {'cp_wishlist_count': count}

