from django.shortcuts import render,redirect
from order.models import Orders
from . models import Wallet
from django.contrib.auth.decorators import login_required
from decimal import Decimal
# Create your views here.

@login_required
def my_wallet(request):
    user = request.user
    wallet = Wallet.objects.get(user_id = user )
    return render(request,'wallet/my_wallet.html',{'wallet':wallet})

    
    
    
    
    # canceled_orders = Orders.objects.filter(user = user,order_status ='Cancelled')
    # if canceled_orders:
    #     total_refund_amount = Decimal('0.00')
    #     total_refund_amount = sum(order.total_price for order in canceled_orders)
    #     user_wallet, created = Wallet.objects.get_or_create(user=user)
        
    #     user_wallet.balance += total_refund_amount
    #     user_wallet.save()
    #     print(user_wallet,'userrrrrrrrrrrrrrr walllllllllettttt')
    #     return redirect('my_wallet') 
    # else:
    #     print('nooooooooooooooooooooo cancel order')
    #     return render(request,'wallet/my_wallet.html')
