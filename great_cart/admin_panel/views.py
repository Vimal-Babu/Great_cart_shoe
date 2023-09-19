from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .models import Product,Category,Brand,Banner
from authentication.models import *
from django.contrib.auth.decorators import login_required
from order.models import Orders


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
    return render(request,'Admin/admin_index.html')

#............Admin...login...and....index....end...............#






#.........All......about...Products....start............#

def handle_product(request):
    products = Product.objects.all()
    categories = Category.objects.filter(is_available=True)
    brands = Brand.objects.all()
    # product_count = products.count()
    print(products,"gfrhngiiiiiiiiiiiuj")

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
            category=category,
            stock = stock,
            new_arrivals=(new_arrival == '1'),  # Convert to boolean
            brand=brand,
            image=product_image
        )
        product.save()

        return redirect('handle_product')  # Replace 'product' with the name of the view that displays the list of products
    # categories = Category.objects.all()
    # brands = Brand.objects.all()
    # return render(request, 'Admin/AdminFunctions/product.html', {'categories': categories, 'brands': brands})
    

def edit_product(request,product_id):
    product = get_object_or_404(Product, id=product_id)
    categories = Category.objects.all()
    brands = Brand.objects.all()
    if request.method == 'POST':
        product_name = request.POST.get('product_name')
        product_description = request.POST.get('description')
        product_price = request.POST.get('product_price')
        product_image = request.FILES.get('product_image')
        category_id = request.POST.get('category')
        stock = request.POST.get('stock')
        new_arrival = request.POST.get('new_arrival')
        brand_id = request.POST.get('brand')  
        category = get_object_or_404(Category, id=category_id)
        brand = get_object_or_404(Brand, id=brand_id)

        # Update other product details
        product.product_name = product_name
        product.description = product_description
        product.price = product_price
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
#******************************************************************************************currentley workin on*******************
def list_order(request):
    orders = Orders.objects.all().order_by('id')
    context = {
        'orders':orders,
    }
    return render(request,'Admin/AdminFunctions/list_order.html',context)

def cancel_order(request,id):
    order = get_object_or_404(Orders, id=id)
    # o = Orders.objects.get(id = id)
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

def Banner_management(request):
    banners = Banner.objects.all()
    active = models.BooleanField(default=True)
    image = models.ImageField(upload_to='photo/banners/')
    context = {
        'banners':banners,
        'active':active,
        'image':image,
        
    }
    return render(request,'Admin/AdminFunctions/banner_management.html',context)


    

#.............................Banner Management.........End.........................#
