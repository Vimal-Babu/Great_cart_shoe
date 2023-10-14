from .models import CartItem  # Import your CartItem model

# def cart_quantity(request):
#     cart_item_count = CartItem.objects.filter(user=request.user).count() if request.user.is_authenticated else None
#     return {'cart_item_count': cart_item_count}


def cart_quantity(request):
    if request.user.is_authenticated:
        cart_item_count = CartItem.objects.filter(user=request.user).count()
    else:
        cart_item_count = 0
    return {'cart_item_count': cart_item_count}
