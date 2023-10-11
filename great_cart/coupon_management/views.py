from django.shortcuts import render,redirect
from .models import Coupon


# Create your views here.

def Gift_management(request):
    coupons = Coupon.objects.all()
    return render(request,'Admin/AdminFunctions/gift_management.html',{'coupons':coupons})

def add_coupon(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        discount = request.POST.get('discount')
        valid_from = request.POST.get('valid_from')
        valid_to = request.POST.get('valid_to')
        
        # Create a new Coupon instance with the form data
        coupon = Coupon(
            code=code,
            discount=discount,
            valid_from=valid_from,
            valid_to=valid_to
        )
        coupon.save()  # Save the new coupon to the database
        
        return redirect('Gift_management')    
    return render(request,'Admin/AdminFunctions/gift_management.html')

def remove_coupon(request,id):
    remove_coupon = Coupon.objects.get(id = id)
    remove_coupon.delete()
    return redirect('Gift_management')
