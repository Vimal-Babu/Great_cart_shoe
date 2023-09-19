from django.shortcuts import render,redirect
from authentication.models import Address,CustomUser
# Create your views here.

def user_profile(request):
    return render(request,'user/user_profile.html')


def user_addAddress(request):
    if request.method == "POST":
        full_name = request.POST.get('full_name')
        phone = request.POST.get('phone')
        address_line_1 = request.POST.get('address_line_1')
        zipcode = request.POST.get('zipcode')
        state = request.POST.get('state')
        city = request.POST.get('city')
        landmark = request.POST.get('landmark')
        set_default = request.POST.get('set_default')  # Check if set_default is checked
        # Create an Address object and save it to the database
        address = Address(
            full_name=full_name,
            user = request.user,
            phone=phone,
            address_line_1=address_line_1,
            Zipcode=zipcode,
            state=state,
            city=city,
            landmark=landmark,
            set_default=bool(set_default),  # Convert 'on' to True, 'None' to False
        )
        address.save()
        # Redirect to a success page or return a response as needed
        return redirect('user_address')  # Replace 'success_page_name' with your actual success page
    return render(request, 'user/user_addAddress.html')


def remove_address(request,id):
    address = Address.objects.get(id = id)
    address.delete()
    return redirect('user_address')


def edit_address(request,id):
    address = Address.objects.get(id = id)
    if request.method == "POST":
        # Retrieve and update address details from the POST data
        address.full_name = request.POST.get('full_name')
        address.phone = request.POST.get('phone')
        address.address_line_1 = request.POST.get('address_line_1')
        address.Zipcode = request.POST.get('zipcode')
        address.state = request.POST.get('state')
        address.city = request.POST.get('city')
        address.landmark = request.POST.get('landmark')
        address.set_default = request.POST.get('set_default')
        address.save()  
        return redirect('user_address')
    return render(request, 'user/edit_address.html',{'address': address})
    
    