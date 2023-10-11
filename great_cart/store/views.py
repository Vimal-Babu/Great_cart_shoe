from django.shortcuts import get_object_or_404, render
from admin_panel.models import Product,ProductImage
from django.db.models import Min, Max, Q


# Create your views here.


def store(request):
    products = Product.objects.all()
    context={
        'products':products
    }
    return render(request,'store/store.html',context)



def product_detail(request, id):
    product = get_object_or_404(Product,id=id)
    product_images = ProductImage.objects.filter(product=product)
    context={
        'product':product,
        'product_images':product_images
    }
    return render(request,'store/product_detail.html',context)


def men(request):
    products_in_mens_category = Product.objects.filter(category__category_name='mens')
    
    print(len(products_in_mens_category))  
    if not products_in_mens_category:
        pass
    context={
        'products_in_mens_category':products_in_mens_category
    }
    return render(request,'store/men.html',context)


def Woman(request):
    products_in_women_category = Product.objects.filter(category__category_name='women')
    
    print(len(products_in_women_category))  
    if not products_in_women_category:
        pass
    context={
        'products_in_women_category':products_in_women_category
    }
    return render(request,'store/woman.html',context)

def kids(request):
    products_in_kids_category = Product.objects.filter(category__category_name='Kids')
    
    print(len(products_in_kids_category))  
    if not products_in_kids_category:
        pass
    context={
        'products_in_kids_category':products_in_kids_category
    }
    return render(request,'store/kids.html',context)

def adidas(request):
    products_by_adidas = Product.objects.filter(brand__name__iexact='adidas')
    context={
        'products_by_adidas':products_by_adidas
    }
    return render(request,'store/brand/adidas.html',context)

def puma(request):
    products_by_puma = Product.objects.filter(brand__name__iexact='Puma')
    context={
        'products_by_puma':products_by_puma
    }
    return render(request,'store/brand/puma.html',context)

def nike(request):
    products_by_nike = Product.objects.filter(brand__name__iexact='Nike')
    context={
        'products_by_nike':products_by_nike
    }
    return render(request,'store/brand/nike.html',context)

def vance(request):
    products_by_vance = Product.objects.filter(brand__name__iexact='Vance')
    context={
        'products_by_vance':products_by_vance
    }
    return render(request,'store/brand/vance.html',context)



def filter_products(request):
    print("working or not")
    # Get the minimum and maximum prices from your Product model
    min_price = Product.objects.aggregate(Min('price'))['price__min']
    max_price = Product.objects.aggregate(Max('price'))['price__max']
    price_ranges = Product.objects.values_list('price', flat=True).distinct()

    # Rest of your view logic remains the same


    # Initialize default min and max values
    selected_min = min_price
    selected_max = max_price
    print(selected_min,'minimum amount')
    print(selected_max,'maximum amount')


    # Filter products based on the selected price range
    filtered_products = Product.objects.filter(price__range=(selected_min, selected_max))

    context = {
        'min_price': min_price,
        'max_price': max_price,
        'selected_min': selected_min,
        'selected_max': selected_max,
        'filtered_products': filtered_products,
        'price_ranges':price_ranges,
    }

    return render(request, 'store/store.html', context)
