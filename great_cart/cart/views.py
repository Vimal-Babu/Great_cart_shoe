from django.shortcuts import get_object_or_404, redirect, render
from admin_panel.models import Product
from .models import  CartItem
from django.contrib.auth.decorators import login_required
from authentication.models import Address
from order.models import Orders
from django.shortcuts import get_object_or_404
import uuid



@login_required(login_url='handle_login')
def cart(request, total_price = 0):
    cart_item = CartItem.objects.filter(user = request.user).order_by('id')
    for cart in cart_item:
        total_price += cart.cart_price
    
    context = {
        'cart_item': cart_item,
        'total_price':total_price,
    }
    return render(request,'cart/cart.html',context)


def add_to_cart(request, id):
    try:
        cart_item = CartItem.objects.get(user=request.user, product_id=id)
        cart_item.quantity += 1
        cart_item.cart_price = cart_item.product.price * cart_item.quantity
        cart_item.save()
    except CartItem.DoesNotExist:
        # If the cart item doesn't exist, create a new one
        product = get_object_or_404(Product, id=id)
        CartItem.objects.create(
            quantity=1,
            product=product,
            cart_price=product.price,
            user=request.user,
        )
    return redirect('cart')


def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    cart_item.delete()
    return redirect('cart') 


def update_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'increase':
            cart_item.quantity += 1
            # cart_item.cart_price += cart_item.product.price 
            cart_item.cart_price = cart_item.product.price * cart_item.quantity
        elif action == 'decrease': 
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.cart_price = cart_item.product.price * cart_item.quantity
                # cart_item.cart_price -= cart_item.product.price
            else:
                cart_item.delete()

        cart_item.save()
    return redirect('cart')



def checkout(request,total_price = 0):
    try:
        address = Address.objects.filter(user=request.user)
        print(address)
    except:
        return redirect('user_address')
    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')
        cart_items = CartItem.objects.filter(user = request.user)
        total_quantity = len(cart_items)
        for cart_item in cart_items:
            order = Orders(
                user = request.user,
                total_price=total_price,
                quantity=total_quantity,
                order_status='Pending', 
                payment_type=payment_method,
                delivery_address=address,
                product_id = cart_item.product.id,
            )
        order.save()
        return redirect('cart')
        
    cart_item = CartItem.objects.filter(user = request.user).order_by('id')
    try:
        address = Address.objects.get(set_default=True)   # pappu make setdefault button on user side show addres page .....**********
    except:
        if not address:
            return redirect('user_address')
        else:
            set_default_address = Address.objects.filter(user = request.user).first()
            set_default_address.set_default = True
            set_default_address.save()
    for cart in cart_item:
        total_price += cart.cart_price

    context = {
        'cart_item': cart_item,
        'total_price':total_price,
        'address':address,
    }
    return render(request,'cart/checkout.html',context)




def generate_uuid():
    # Generate a random UUID (version 4)
    uuid_obj = uuid.uuid4()
    
    # Convert the UUID to a string
    uuid_str = str(uuid_obj)
    
    return uuid_str




def place_order(request,address=0):
    if request.method == 'POST':    
        # address_id = request.POST.get('address')
        payment_method = request.POST.get('payment_method')
        address_id = request.POST.get('selected_address')
        try:
            address = Address.objects.get(id = address_id)
        except:
            pass
        # try:
        #     address = Address.objects.get(user=request.user, set_default = True)
        # except:
        #     pass

        total_price = 0
        cart_items = CartItem.objects.filter(user=request.user).order_by('id')
        
        order_id = generate_uuid()
        for cart_item in cart_items:
            total_price += cart_item.product.price * cart_item.quantity
            order = Orders(
                user=request.user,
                product=cart_item.product,
                # total_price=total_price,
                total_price=cart_item.product.price * cart_item.quantity,
                quantity=cart_item.quantity,
                delivery_address=address,
                payment_type=payment_method, 
                order_id = order_id,
            )
            order.save()
        return redirect('order_success',order.order_id)
    
    return render(request,'cart/checkout.html')
# total_price=cart_item.product.price * cart_item.quantity,  # Use the correct price


def order_success(request,order_id):
    user = request.user
    orders = Orders.objects.filter(order_id=order_id).order_by('id')
    grand_total = sum(order.total_price for order in orders)
    context = {
        'orders':orders, 
        'grand_total':grand_total,     
    }
    return render(request,"order/order_success.html",context)
    # return render(request,'order/order_details.html')

    
def your_orders_page(request):
    user = request.user
    orders = Orders.objects.filter(user_id=user.id)
    grand_total = sum(order.total_price for order in orders)
    context={
        'orders':orders,
        'grand_total':grand_total
    }
    return render(request,'order/your_orders_page.html',context)



def order_details(request):
    return render(request,'order/order_details.html')



def payment_page(request):
    # NOWWWWWWWWWWW after payment???
    return render(request,'cart/payment_page.html')





# def place_order(request):
#     if request.method == 'POST':
#         # Extract form data, such as delivery address, payment type, etc.
#         delivery_address_id = request.POST.get('default_address')  # Example, adjust this based on your form fields
#         payment_type = request.POST.get('payment_type')  # Example, adjust this based on your form fields

#         # Create a new order record in the database
#         order = Order.objects.create(
#             user=request.user,
#             delivery_address_id=delivery_address_id,
#             payment_type=payment_type,
#             total_price=request.POST.get('total_price'),  # You can extract this from the form
#             # Add other order details as needed
#         )


