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
            cart_item.delete()
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

