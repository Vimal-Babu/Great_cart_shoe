from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .models import Product,Category,Brand,Banner,SearchQuery,ProductImage
from authentication.models import *
from django.contrib.auth.decorators import login_required
from order.models import Orders
from wallet.models import Wallet
from django.db.models import Count,Sum
from django.db.models.functions import TruncMonth
from django.db.models import IntegerField
from django.db.models.expressions import F
from django.http import HttpResponse
from django.shortcuts import render
from io import BytesIO
from reportlab.pdfgen import canvas
from io import BytesIO
from reportlab.pdfgen import canvas
from order.models import Orders 
from reportlab.lib.pagesizes import letter
from decimal import Decimal
from django.db.models import Q



#............Admin...login...and....index....start...............#

def admin_login(request):
    if request.user.is_authenticated and  request.user.is_superuser==True:
        return redirect('admin_index')
    if request.method=="POST":
        email=request.POST.get("email")
        pass1=request.POST.get("password")
        my_user = authenticate(email=email,password=pass1)
        if my_user is not None:
            if my_user.is_superuser:
                login(request,my_user)
                messages.success(request,"Login Success!")
                return redirect('admin_index')
            elif my_user is not my_user.is_superuser:
                messages.error(request,"You are not an Admin")
                return redirect('admin_login')
        else:
            messages.error(request,"Invalid Credentials")
    return render(request,"Admin/AdminFunctions/admin_login.html")  


def handle_logout(request):
    logout(request)
    messages.info(request,"Logout Success")
    return redirect('handle_login') 


def admin_index(request):
    if not request.user.is_superuser:
        return redirect('admin_login')
    # Calculate labels (months) and data (number of orders) for the chart
    orders_by_month = Orders.objects.annotate(month=TruncMonth('order_date')).values('month').annotate(num_orders=Count('id'))
    labels = [order['month'].strftime('%B %Y') for order in orders_by_month]
    data = [order['num_orders'] for order in orders_by_month]
    total_price_sum = Orders.objects.aggregate(total_price_sum=Sum('total_price'))['total_price_sum']
    total_price_sum = total_price_sum  # Convert to integer
    orders = Orders.objects.all()
    print( total_price_sum)
    context = {
        'labels': labels,
        'data': data,
        'total_price_sum': total_price_sum,
        'orders':orders,
    }
    return render(request, 'Admin/admin_index.html', context)

def sales_and_revenue_chart(request):
    return render(request,'Admin/admin_index.html')
                    

def generate_sales_report_pdf(request):
    # Create a BytesIO buffer to receive the PDF data
    buffer = BytesIO()
    # Create the PDF object, using the BytesIO buffer as its "file"
    p = canvas.Canvas(buffer, pagesize=letter)
    y = 750  # Starting Y-coordinate
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
    p.drawString(100, y, "Sales Report")
    y -= 30  # Move down for spacing

    # Fetch all orders data from the database
    orders = Orders.objects.all()

    # Loop through orders and generate report for each
    for order in orders:
        # Order details
        p.setFont(content_style['fontName'], content_style['fontSize'])
        p.setFillColorRGB(*content_style['textColor'])  # Use setFillColorRGB
        p.drawString(100, y, f"Order ID: {order.id}")
        y -= 20
        p.drawString(100, y, f"Date: {order.order_date}")
        y -= 20
        p.drawString(100, y, f"Product Name: {order.product.product_name}")
        y -= 20
        p.drawString(100, y, f"Order Status: {order.order_status}")
        y -= 20
        p.drawString(100, y, f"Order Quantity: {order.quantity}")
        y -= 20
        p.drawString(100, y, f"Total Price: ${order.total_price}")
        y -= 40  # Move down for the next order

        if y < 50:
            p.showPage()
            y = 750  # Reset Y-coordinate

    # Close the PDF object cleanly
    p.showPage()
    p.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    response = HttpResponse(buffer.read(), content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="sales_report.pdf"'

    return response

#............Admin...login...and....index....end...............#


#.........All......about...Products....start............#
@login_required
def handle_product(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect('admin_login')
    products = Product.objects.all()
    categories = Category.objects.filter(is_available=True)
    brands = Brand.objects.all()
    # product_count = products.count()
    

    context = {
        "products" : products,
        "categories" : categories,
        "brands" : brands,
        # "product_count" : product_count,
        }
    return render(request, "Admin/AdminFunctions/product.html",context)


def add_product(request):
    if request.method == 'POST':
        product_name = request.POST.get('product_name')
        product_description = request.POST.get('description')
        product_price = request.POST.get('product_price')
        offer_percentage = request.POST.get('offer_percentage')
        product_image = request.FILES.get('product_image')
        category_id = request.POST.get('category')
        stock = request.POST.get('stock')
        new_arrival = request.POST.get('new_arrival')
        brand_id= request.POST.get('brand')
        category = get_object_or_404(Category, id=category_id)
        brand = get_object_or_404(Brand, id=brand_id)

        product = Product(
            product_name=product_name,
            description=product_description,
            price = product_price,
            offer_percentage = offer_percentage,
            category=category,
            stock = stock,
            new_arrivals=(new_arrival == '1'),  # Convert to boolean
            brand=brand,
            image=product_image
        )
        product.save()

        return redirect('handle_product')  
    # return render(request, 'Admin/AdminFunctions/product.html', {'categories': categories, 'brands': brands})
def add_multiple_image(request):
    image = ProductImage.objects.all()
    products = Product.objects.all()
    context = {
        'products':products,
        'image':image
    }
    return render(request,'Admin/AdminFunctions/product_multiple_image.html',context)
    

def edit_product(request,product_id):
    product = get_object_or_404(Product, id=product_id)
    categories = Category.objects.all()
    brands = Brand.objects.all()
    if request.method == 'POST':
        product_name = request.POST.get('product_name')
        product_description = request.POST.get('description')
        product_price = request.POST.get('product_price')
        offer_percentage_str = request.POST.get('offer_percentage')
        product_image = request.FILES.get('product_image')
        category_id = request.POST.get('category')
        stock = request.POST.get('stock')
        new_arrival = request.POST.get('new_arrival')
        brand_id = request.POST.get('brand')  
        category = get_object_or_404(Category, id=category_id)
        brand = get_object_or_404(Brand, id=brand_id)
        try:
            offer_percentage =Decimal(offer_percentage_str)
        except ValueError:
            offer_percentage = Decimal('0.00')

        # Update other product details
        product.product_name = product_name
        product.description = product_description
        product.price = product_price
        product.offer_percentage = offer_percentage
        if product_image:
            product.image = product_image
        product.category = category
        product.stock = stock
        product.new_arrivals = new_arrival
        product.brand = brand
        product.save()
    
        return redirect('handle_product')
    context ={
        'product':product,
        'categories':categories,
        'brands':brands
    }

    return render(request, 'Admin/AdminFunctions/product.html', context)


def product_block(request,id):
    block = Product.objects.filter(id=id).update(is_available=False)
    return redirect("handle_product")

def product_unblock(request, id):
    un_block = Product.objects.filter(id=id).update(is_available=True)
    return redirect('handle_product')



# All about Products END......................




#............................category.........................................#

def category_management(request):
    categories = Category.objects.all().order_by('id')
    return render(request,'Admin/AdminFunctions/category.html',{'categories': categories}) 



def category_block(request,id):
    block = Category.objects.filter(id=id).update(is_available = False)
    return redirect("category_management")

def category_unblock(request,id):
    un_block = Category.objects.filter(id=id).update(is_available = True)
    return redirect("category_management")



def add_category(request):
    if request.method == 'POST':
        category_name = request.POST.get('category_name')
        description = request.POST.get('category_description')
        Is_available = request.POST.get('Is_available')
        category = Category.objects.create(
            category_name=category_name,
            description=description,
            is_available=Is_available
        )
        return redirect('category_management')

    return render(request, "Admin/AdminFunctions/category.html")

def edit_category(request, id):
    category = get_object_or_404(Category,id=id)
    if request.method == 'POST':
        category_name = request.POST.get('category_name')
        category_description = request.POST.get('category_description')
        category.category_name = category_name
        category.description = category_description
        category.save()
        return redirect('category_management')    
    return render(request,"Admin/AdminFunctions/category.html")




#............................category...End.........................................#



#.............................USER.........start.........................#

def user(request):
    all_users = CustomUser.objects.filter(is_superuser = False).order_by('id')
    return render(request,'Admin/AdminFunctions/user.html',{'all_users': all_users})


def user_block(request,id):
    d = CustomUser.objects.get(id=id)
    d.is_active = False
    d.save()
    return redirect('user')

def user_unblock(request,id):
    d = CustomUser.objects.get(id=id)
    d.is_active = True
    d.save()
    return redirect('user')

#.............................USER.........end.........................#

#.............................Order.........start.........................#

def list_order(request):
    orders = Orders.objects.all().order_by('-order_date')
    context = {
        'orders':orders,
    }
    return render(request,'Admin/AdminFunctions/list_order.html',context)

def cancel_order(request,id):
    order = get_object_or_404(Orders, id=id)
    if order.order_status != 'Cancelled' and order.payment_type != 'COD':
        amount_to_return = order.total_price
        try:
            user_wallet = Wallet.objects.get(user=order.user)
            user_wallet.balance += amount_to_return
            user_wallet.save()
        except Wallet.DoesNotExist:
            user_wallet = Wallet.objects.create(user=order.user)

    # order = get_object_or_404(Orders, id=id)
    order.order_status = 'Cancelled'
    order.save()
    return redirect('list_order')
    # return render(request,'Admin/AdminFunctions/list_order.html')
    
    
def manage_status(request, order_id):
    if request.method == 'POST':
        new_status = request.POST.get('status')
        order = Orders.objects.get(id=order_id)
        order.order_status = new_status
        order.save()
    
    return redirect('list_order') 


#.............................Order.........End.........................#



#.............................Brand.........start.........................#



def brand(request):
    brands = Brand.objects.all()
    return render(request,'Admin/AdminFunctions/brand.html',{'brands':brands})

def add_brand(request):
    if request.method == 'POST':
        brand_name = request.POST.get('brand_name')
        brand_description = request.POST.get('description')
        Logo = request.FILES.get('logo')
        brands = Brand(
            name = brand_name,
            description = brand_description,
            logo = Logo
        )
        brands.save()
        return redirect('brand')
    return redirect('brand')

def edit_brand(request,id):
    brands = get_object_or_404(Brand,id=id)
    if request.method == 'POST':
        brand_name = request.POST.get('brand_name')
        brand_description = request.POST.get('description')
        Logo = request.FILES.get('logo')
        brands.brand_name = brand_name
        brands.brand_description = brand_description
        brands.Logo = Logo
        brands.save()
        return redirect('brand')

def delete_brand(request,id):
    brand = get_object_or_404(Brand, id=id)
    brand.delete()
    return redirect('brand')


#.............................Brand.........end.........................#



#.............................Banner Management.........start.........................#
# active = models.BooleanField(default=True)
# image = models.ImageField(upload_to='photo/banners/')

def add_banner(request):
    if request.method =='POST':
        banner_image = request.FILES.get('bannerImage')
        active = request.POST.get('active')
        # if active == True:
        #     active_bool = True
        # else:
        #     active_bool = False
                
        banner = Banner.objects.create(
            image = banner_image,
            active=active,
        )
        return redirect('Banner_management')
    return render(request,"Admin/AdminFunctions/banner_management.html")


def Banner_management(request):
    banners = Banner.objects.all()
    context = {
        'banners':banners,
    }
    return render(request,'Admin/AdminFunctions/banner_management.html',context)

# {% url 'remove_banner' banner.id %}

def remove_banner(request,id):
    banner = get_object_or_404(Banner,id = id)
    banner.delete()
    return redirect('Banner_management')


#.............................Banner Management.........End.........................#



# def search(request):
#     print('serch view works')
#     if 'keyword' in request.GET:
#         keyword = request.GET['keyword']
#         products = Product.objects.filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
#         context = {
#             'products': products,
#             'keyword': keyword,
#         }
    
    
#     return render(request, 'home/home.html', context)


def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        
        # Store the search query in your database using the SearchQuery model
        SearchQuery.objects.create(user=request.user,query=keyword)
        
        products = Product.objects.filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
        context = {
            'products': products,
            'keyword': keyword,
        }
    return render(request, 'home/home.html', context)


from django.http import JsonResponse

def search_suggestions(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        # Query your database for suggestions based on the keyword
        suggestions = Product.objects.filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword)).values('product_name')[:5]
        suggestion_list = [suggestion['product_name'] for suggestion in suggestions]
        return JsonResponse(suggestion_list, safe=False)

    return JsonResponse([], safe=False)
