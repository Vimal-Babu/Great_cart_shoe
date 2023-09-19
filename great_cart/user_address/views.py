from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from authentication.models import Address 
# Create your views here.
def user_address(request):
    user = request.user  # Get the logged-in user
    # Retrieve the addresses associated with the user
    addresses = Address.objects.filter(user=user)
    return render(request,'user/user_address.html', {'addresses': addresses})
