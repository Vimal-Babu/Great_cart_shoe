from .models import CartItem  # Import your CartItem model

def cart_quantity(request):
    cart_item_count = CartItem.objects.filter(user=request.user).count() if request.user.is_authenticated else 0
    return {'cart_item_count': cart_item_count}
