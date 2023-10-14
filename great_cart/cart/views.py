from django.shortcuts import get_object_or_404, redirect, render
from admin_panel.models import Product
from .models import  CartItem
from django.contrib.auth.decorators import login_required
from authentication.models import Address
from order.models import Orders
from django.shortcuts import get_object_or_404
import uuid
from wallet.models import Wallet
from django.http import FileResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from io import BytesIO
import reportlab
from coupon_management.models import Coupon
from django.utils import timezone
from django.contrib import messages
from django.http import JsonResponse
import razorpay
from wallet.models import Wallet


# client = razorpay.Client(auth=('settings.razor_pay_key_id', 'settings.key_secret'))

# data = { 
#     "amount": 500, 
#     "currency": "INR", 
#     "receipt": "order_rcptid_11" }
#         payment = client.order.create(data=data)
        
# client = razorpay.Client(auth=('settings.razor_pay_key_id', 'settings.key_secret'))

# DATA = {
#     "amount": 100,
#     "currency": "INR",
#     "receipt": "receipt#1",
#     "notes": {
#         "key1": "value3",
#         "key2": "value2"
#     }
# }
# client.order.create(data=DATA)




@login_required(login_url='handle_login')
def cart(request, total_price = 0):
    cart_item = CartItem.objects.filter(user = request.user).order_by('id')
    for cart in cart_item:
        total_price += cart.cart_price
    
    context = {
        'cart_item': cart_item,
        'total_price':total_price
    }
    return render(request,'cart/cart.html',context)


def add_to_cart(request, id):
    if not request.user.is_authenticated:
        return redirect('handle_login')
    try:
        cart_item = CartItem.objects.get(user=request.user, product_id=id)
        cart_item.quantity += 1
        cart_item.cart_price = cart_item.product.offer_price() * cart_item.quantity
        # id = cart_item
        cart_item.save()
    except CartItem.DoesNotExist:
        # If the cart item doesn't exist, create a new one
        product = get_object_or_404(Product, id=id)
        offer_price = product.offer_price()
        
        CartItem.objects.create(
            quantity=1,
            product=product,
            cart_price=offer_price,
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
            cart_item.cart_price = cart_item.product.offer_price() * cart_item.quantity
            # net_price.total_price = net_price.
        elif action == 'decrease': 
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.cart_price = cart_item.product.offer_price() * cart_item.quantity
                # cart_item.cart_price -= cart_item.product.price
            else:
                cart_item.delete()

        cart_item.save()
    return redirect('cart')

    
def checkout(request,total_price = 0):
    try:
        addresses = Address.objects.filter(user=request.user)
    except:
        return redirect('user_address')
    cart_item = CartItem.objects.filter(user = request.user).order_by('id')
    # total_price = sum(cart_item.cart_price for cart_item in cart_item)
    try:
        addresses = Address.objects.get(set_default=True)  
    except:
        if not addresses:
            return redirect('user_address')
        else:
            set_default_address = Address.objects.filter(user = request.user).first()
            set_default_address.set_default = True
            set_default_address.save()
    for cart in cart_item:
        total_price += cart.cart_price
    print(total_price,'total price in checkout function')
    context = {
        'cart_item': cart_item,
        'total_price':total_price,
        'addresses':addresses,
    }
    return render(request,'cart/checkout.html',context)


def generate_uuid():
    # Generate a random UUID (version 4)
    uuid_obj = uuid.uuid4()
    
    # Convert the UUID to a string
    uuid_str = str(uuid_obj)
    
    return uuid_str

def apply_coupon(request,total_price = 0):
    print(total_price,'total price in apply coupon function')
    coupon_code = request.POST.get('coupon_code')
    addresses = Address.objects.filter(user=request.user)
    cart_item = CartItem.objects.filter(user = request.user).order_by('id')
    total_price = sum(cart_item.cart_price for cart_item in cart_item)
    print(total_price,'total price at apply coupon after the calculations')
    try:
        if coupon_code:
            coupon = Coupon.objects.get(code=coupon_code, valid_from__lte=timezone.now(), valid_to__gte=timezone.now())
            total_price -= coupon.discount
            messages.success(request, f'Coupon "{coupon.code}" applied successfully. Discount: ₹{coupon.discount}')
    except Coupon.DoesNotExist:
        messages.error(request, 'Enter A Valid Code or Expired code')
    total_price = float(total_price)
    print(total_price,'total price at session')
    context={
        'total_price':total_price,
        'addresses':addresses,
        'cart_item': cart_item
    }
    request.session['total_price'] = total_price
    print(total_price,'after assign to the session')
    
    return render(request,'cart/checkout.html',context)   

def place_order(request, address=0, total_price=0, context=None):
    total_price = request.session.get('total_price', 0)
    print(total_price,'total price on the top of the place order function ')
    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')
        address_id = request.POST.get('selected_address')
        try:
            address = Address.objects.get(id=address_id)
        except Address.DoesNotExist:
            pass
        cart_items = CartItem.objects.filter(user=request.user).order_by('id')
        order_id = generate_uuid()
        
        if payment_method == "COD":
            print('cod fuction wortksssssssssssssss')
            for cart_item in cart_items:
                order = Orders(
                    user=request.user,
                    product=cart_item.product,
                    total_price=cart_item.cart_price,
                    quantity=cart_item.quantity,
                    delivery_address=address,  
                    payment_type=payment_method,
                    order_id=order_id,
                )
                order.save()
                cart_item.delete()
            return redirect('order_success',order_id)
        elif payment_method == "wallet":
            # total_price = sum(cart_item.cart_price for cart in cart_item)
            wallet = Wallet.objects.get(user=request.user)
            print(wallet,'wallet outside the if ')
            if wallet.balance >= total_price:
                wallet.balance -= int(total_price)
                wallet.save()
                print("wallet balance ", wallet.balance)
                print('total price ',total_price)
                print("8888888888888888888888888888888")
                order_id = generate_uuid()
                for cart_item in cart_items:
                    order = Orders(
                        user=request.user,
                        product=cart_item.product,
                        total_price=cart_item.cart_price,
                        quantity=cart_item.quantity,
                        delivery_address=address, 
                        payment_type=payment_method,
                        order_id=order_id,
                    )
                    order.save()
                    cart_item.delete()
                return redirect('order_success',order_id)
            else:
                messages.error(request, 'Insufficient valet amount')
                return redirect('checkout')
        elif payment_method == 'razor':
            for cart_item in cart_items:
                order = Orders(
                    user=request.user,
                    product=cart_item.product,
                    total_price=cart_item.cart_price,
                    quantity=cart_item.quantity,
                    delivery_address=address,
                    payment_type=payment_method, 
                    order_id=order_id,
                )
                order.save()
                cart_item.delete()
            return redirect('order_success', order.order_id)
    context = {
        'total_price': total_price
    }
    return render(request, 'cart/checkout.html', context)


def order_success(request,order_id,total_price = 0):
    total_price = request.session.get('total_price', 0) 
    user = request.user
    orders = Orders.objects.filter(order_id=order_id).order_by('order_id')
    grand_total = total_price
    # grand_total = sum(order.total_price for order in orders)
    context = {
        'orders':orders, 
        'grand_total':grand_total,     
    }
    return render(request,"order/order_success.html",context)
    # return render(request,'order/order_details.html')

    
def your_orders_page(request):
    user = request.user
    orders = Orders.objects.filter(user_id=user.id).order_by('-order_date')
    grand_total = sum(order.total_price for order in orders)
    context={
        'orders':orders,
        'grand_total':grand_total
    }
    return render(request,'order/your_orders_page.html',context)


def generate_pdf(request, order_id):
    # Create a BytesIO buffer to receive the PDF data
    order = get_object_or_404(Orders, id=order_id)
    buffer = BytesIO()

    # Create the PDF object, using the BytesIO buffer as its "file"
    p = canvas.Canvas(buffer, pagesize=letter)
    y = 750

    # Set up styles for the heading and content
    heading_style = {
        'fontName': 'Helvetica-Bold',
        'fontSize': 16,
        'alignment': 1,  # Center-aligned text
        'textColor': (0, 0, 0)  # Black color
    }

    content_style = {
        'fontName': 'Helvetica',
        'fontSize': 12,
        'textColor': (0, 0, 0)  # Black color
    }

    # Heading
    p.setFont(heading_style['fontName'], heading_style['fontSize'])
    p.setFillColorRGB(*heading_style['textColor'])  # Use setFillColorRGB
    p.drawString(100, y, f"Invoice ")
    y -= 30  # Move down for spacing

    # Order details
    p.setFont(content_style['fontName'], content_style['fontSize'])
    p.setFillColorRGB(*content_style['textColor'])  # Use setFillColorRGB
    p.drawString(100, y, f"invoice number: {order.id}")
    y -= 20
    p.drawString(100, y, f"Date: {order.order_date}")
    y -= 20
    p.drawString(100, y, f"Product Name: {order.product.product_name}")
    y -= 20
    p.drawString(100, y, f"Order Status: {order.order_status}")
    y -= 20
    p.drawString(100, y, f"Order Quantity: {order.quantity}")
    y -= 20
    p.drawString(100, y, f"Delivery Address: {order.delivery_address.address_line_1}")
    y -= 20
    p.drawString(100, y, f"City: {order.delivery_address.city}")
    y -= 20
    p.drawString(100, y, f"State: {order.delivery_address.state}")
    y -= 20
    p.drawString(100, y, f"Zip Code: {order.delivery_address.Zipcode}")
    y -= 20
    p.drawString(100, y, f"Landmark: {order.delivery_address.landmark}")
    y -= 20
    p.drawString(100, y, f"Total Price: ${order.total_price}")
    
    # Close the PDF object cleanly
    p.showPage()
    p.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    response = HttpResponse(buffer.read(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="order_{order.id}.pdf"'

    return response

def cancel_order_button(request, order_id):
    user_wallet = None
    order = Orders.objects.get(id=order_id)
    if order.payment_type != 'COD':
        amount_to_return = order.total_price
        print(order.total_price)
        print(amount_to_return)
        try:
            user_wallet  = Wallet.objects.get(user=order.user)
            user_wallet.balance += amount_to_return 
            user_wallet.save()
        except Wallet.DoesNotExist:
            user_wallet = Wallet.objects.create(user=order.user)
            
    order.order_status = 'Canceled'
    order.save()
    return redirect('your_orders_page')  


def order_details(request):
    return render(request,'order/order_details.html')

def payment_page(request):
    # NOWWWWWWWWWWW after payment???
    return render(request,'cart/payment_page.html')





# coupon_code = request.POST.get('coupon_code')
    #     print(coupon_code,'inside the if coupon code works or not check')
    #     if coupon_code:
    #         try:
    #             applied_coupon = Coupon.objects.get(code=coupon_code, valid_from__lte=timezone.now(), valid_to__gte=timezone.now())
    #         except Coupon.DoesNotExist:
    #             messages.error(request, 'Invalid or expired coupon code.')

    #     # Calculate the discounted total price if a valid coupon is applied
    #     if applied_coupon:
    #         total_price -= (total_price * (applied_coupon.discount / 100))


# @transaction.atomic
# def confirm_razorpay_payment(request, order_id):
#     current_user = request.user
#     try:
#         order = Order.objects.get(order_id=order_id, user=current_user, is_ordered=False)
#     except Order.DoesNotExist:
#         return redirect('order_confirmed')
    
#     total_amount = order.order_total 

#     payment = Payment(
#         user=current_user,
#         payment_method="Razorpay",
#         status="Paid",
#         amount_paid=total_amount,
#     )
#     payment.save()

#     order.is_ordered = True
#     order.order_id = order_id
#     order.payment = payment
#     order.save()

#     cart_items = CartItem.objects.filter(user=current_user)
#     for cart_item in cart_items:
#         product=cart_item.product
#         stock=product.quantity-cart_item.quantity
#         product.quantity=stock
#         product.save()
#         order_product = OrderProduct(
#             order=order,
#             payment=payment,
#             user=current_user,
#             product=cart_item.product,
#             quantity=cart_item.quantity,
#             product_price=cart_item.product.price,
#             ordered=True,
#         )
#         order_product.save()

#     cart_items.delete()

#     context = {'order': order}

#     return render(request, 'userapp/order_confirmed.html', context)

# def pay_by_wallet(request,address=0,total_price = 0,context=None):
#     print("working pay by wallet")
#     try:
#         addresses = Address.objects.filter(user=request.user)
#     except:
#         return redirect('user_address')
#     print(addresses,"addressssssssssssssssss")
    
#     total_price = request.session.get('total_price', 0)
#     cart_item = CartItem.objects.filter(user=request.user)
#     if request.method == 'POST':
#         print("if working pay by wallet")
#         payment_method = request.POST.get('payment_method')
#         address_id = request.POST.get('selected_address')
#         try:
#             addresses = Address.objects.get(id = address_id)
#         except:
#             pass
#         # cart_item = CartItem.objects.filter(user=request.user)
#         total_price = sum(cart_item.cart_price for cart in cart_item)
#         wallet = Wallet.objects.get(user=request.user)
#         if wallet.balance >= total_price:
#             wallet.balance -= total_price
#             wallet.save()
#             order_id = generate_uuid()
#             for cart_item in cart_item:
#                 order = Orders(
#                     user=request.user,
#                     product=cart_item.product,
#                     total_price=cart_item.cart_price,
#                     quantity=cart_item.quantity,
#                     delivery_address=addresses,
#                     payment_type=payment_method, 
#                     order_id = order_id,
#                 )
#                 order.save()
#             cart_item.delete()
#             return redirect('order_success')
#         else:
#             pass
#     context = {
#         'total_price': total_price,
#         'addresses':addresses,
#         'cart_item': cart_item
#     }
#     return render(request, 'cart/checkout.html', context)



# if request.method == 'POST':
    #     payment_method = request.POST.get('payment_method')
    #     cart_items = CartItem.objects.filter(user = request.user)
    #     total_quantity = len(cart_items)
    #     for cart_item in cart_items:
    #         order = Orders(
    #             user = request.user,
    #             total_price=total_price,
    #             quantity=total_quantity,
    #             order_status='Pending', 
    #             payment_type=payment_method,
    #             delivery_address=address,
    #             product_id = cart_item.product.id,
    #         )
    #     order.save()
    
    
# def razorpay_payment_view(request):
#     user_id = request.GET.get('user_id')
#     payment_status = request.GET.get('payment_status')

#     if payment_status == 'success':
#         # Handle payment success
#         total_price = request.session.get('total_price', 0)
#         try:
#             address_id = request.GET.get('selected_address')
#             address = Address.objects.get(id=address_id)
#         except:
#             address = None

#         cart_items = CartItem.objects.filter(user=request.user).order_by('id')
#         order_id = generate_uuid()
        
#            else:
#         # Handle payment failure or cancellation
#         return HttpResponse('Payment failed or was canceled.')



# def razorpay_payment_view(request):
#     user_id = request.GET.get('user_id')
#     print('resorepay workinggggggggggggggggggggggggggggggggggggggggggggggggggggggg')
#     total_price = request.session.get('total_price', 0) 
#     print('total_price','total_priceeeeeeeeeeeeeeeeeeeeeeeeeeeeee')
#     address_id = request.POST.get('selected_address')
#     print(address_id,'addresssssssssss iddddddddddddddddddddddddddd')
#     try:
#         address = Address.objects.get(id=address_id)
#     except:
#         pass
#     cart_items = CartItem.objects.filter(user=request.user).order_by('id')
#     order_id = generate_uuid()
#     for cart_item in cart_items:
#         order = Orders(
#             user=request.user,
#             product=cart_item.product,
#             total_price=cart_item.cart_price,
#             quantity=cart_item.quantity,
#             delivery_address=address,
#             payment_type="Razorpay", 
#             order_id=order_id,
#         )
#         order.save()
#         cart_item.delete()
#     return redirect('order_success', order.order_id)



    

