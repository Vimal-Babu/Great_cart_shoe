from django.shortcuts import get_object_or_404, render
from admin_panel.models import Product


# Create your views here.


def store(request):
    products = Product.objects.all()
    context={
        'products':products
    }
    return render(request,'store/store.html',context)



def product_detail(request, id):
    product = get_object_or_404(Product,id=id)
    context={
        'product':product
    }
    return render(request,'store/product_detail.html',context)