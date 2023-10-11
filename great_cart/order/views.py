from django.shortcuts import render,redirect
from .models import Orders
from cart.models import CartItem
# Create your views here.
from wallet.models import Wallet  # Import the Wallet model



# def place_order(request):
#     return render(request,'order/placeorder.html')

#  Cartitem = CartItem.objects.get(id = id)
    # order = Order.objects.create(
    #     user = request.user,
    #     products =CartItem.products,
    # )