from django.shortcuts import render, redirect, get_object_or_404
from admin_panel.models import Product,Banner
from . models import CustomUser
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from twilio.rest import Client
from django.conf import settings
import random
from decouple import config
from pyotp import TOTP
import secrets
import pyotp
import os
from django.contrib.auth import get_user_model
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.hashers import make_password
from twilio.base.exceptions import TwilioRestException
from dotenv import load_dotenv
import os
from twilio.rest import Client

load_dotenv()


client = Client(os.environ['TWILIO_ACCOUNT_SID'], os.environ['TWILIO_AUTH_TOKEN'])
verify = client.verify.services(os.environ['TWILIO_VERIFY_SERVICE_SID'])



def send(phone):
    verify.verifications.create(to=phone, channel='sms')


def check(phone, code):
    try:
        result = verify.verification_checks.create(to=phone, code=code)
        print("settttttt")
    except TwilioRestException:
        print('no')
        return False
    return result.status == 'approved'



def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        first_name = request.POST["first_name"]
        
        email = request.POST["email"]
        phone = "+91"+request.POST["phone_number"]
        pass1 = request.POST["pass1"]
        pass2 = request.POST["pass2"]
        
        if pass1 != pass2:
            messages.error(request, 'Passwords do not match.')
            return redirect('register')
        
        if len(pass1) < 6:
            messages.error(request, 'Password should be at least 6 characters long.')
            return redirect('register')
        
        if not any(char.isdigit() for char in pass1):
            messages.error(request, 'Password should contain at least one digit.')
            return redirect('register')
        
        if not any(char.isalpha() for char in pass1):
            messages.error(request, 'Password should contain at least one letter.')
            return redirect('register')
    
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return redirect('register')
        
        if CustomUser.objects.filter(phone=phone).exists():
            messages.error(request, 'Phone number already exists.')
            return redirect('register')
        # Generate OTP and store it temporarily in session
        otp = send(phone)
        print(otp,"otprecived")
        request.session['otp'] = otp

        hashed_password = make_password(pass1) 
        my_user = CustomUser.objects.create(
            first_name=first_name,
            email=email,
            phone=phone,
            password=hashed_password)
        my_user.save()
        print(phone,"mmmmmmmmmmm")
        phone = my_user.phone
        print(phone,"kkkkkkkkkkkkkkk")
        return render(request, "authentication/otp_verification.html", {'phone': phone})
    return render(request, "authentication/register.html")



def handle_login(request):
    customuser = None
    if request.method == 'POST':
        email = request.POST.get('email')
        print(email,"tttttttttttttt")
        password = request.POST.get('pass1')
        try:
            customuser = CustomUser.objects.get(email = email)
            phone = str(customuser.phone)

        except:
            messages.info(request,"Invalid Credentials")
            return redirect('handle_login')

        if customuser.is_verified == False and customuser.is_superuser == False:
            send(phone)
            return render(request, "authentication/otp_verification.html", {'phone': phone})
        elif customuser.is_superuser == True:
            return redirect('admin_login')
        else:
            pass

        print(request)
        my_user = authenticate(email=email, password=password)
        print(my_user)
        if my_user is not None:
            if my_user.is_superuser==True:
                return redirect('admin_index')

            else:
                login(request,my_user)
                messages.success(request, "Login successful.")
                return redirect('home')  # Correct the URL pattern here
        else:
            messages.success(request, "Invalid email or password. Please try again")
    return render(request, 'authentication/login.html')

def user_logout(request):
    messages.success(request, "Logout successful.")
    logout(request)
    return redirect('home')



def forget_password(request):
    if request.method == 'POST':
        phone_number = "+91"+ request.POST.get('phone_number')
        try:
            user = CustomUser.objects.get(phone=phone_number)
            if user:
                send(phone_number)
                return render(request,"authentication/changepassword_otp.html",{'phone':phone_number})
                
            # return redirect('resetting_password')
        except CustomUser.DoesNotExist:
            messages.error(request, "User with the provided phone number does not exist.")
            
    return render(request,'authentication/forget_password.html')

def change_password_otp(request,phone):
    customuser = CustomUser.objects.get(phone = phone)
    if request.method == 'POST':
        code = request.POST.get('otp')


        if check(phone,code):
            return redirect('resetting_password',phone)
        else:
            messages.info(request,"Enter the correct otp")

    return render(request, 'authentication/changepassword_otp.html')


def resetting_password(request,phone):
    user = CustomUser.objects.get(phone = phone)
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        if new_password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('resetting_password',phone)
        
        hashed_password = make_password(new_password) 
        user.password = hashed_password
        user.save()
        return redirect('handle_login')
        
        
    return render(request,'authentication/resetting_password.html',{'phone':phone})

    
@login_required
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        user = request.user  # Get the currently logged-in user

        # Check if the current password matches the user's actual password
        if not user.check_password(current_password):
            messages.error(request, 'Current password is incorrect.')
            return redirect('change_password')

        # Check if the new password and confirm password match
        if new_password != confirm_password:
            messages.error(request, 'New password and confirm password do not match.')
            return redirect('change_password')

        # Check if the new password meets your criteria (e.g., length, contains digits, contains letters)
        if len(new_password) < 6:
            messages.error(request, 'Password should be at least 6 characters long.')
            return redirect('change_password')

        if not any(char.isdigit() for char in new_password):
            messages.error(request, 'Password should contain at least one digit.')
            return redirect('change_password')

        if not any(char.isalpha() for char in new_password):
            messages.error(request, 'Password should contain at least one letter.')
            return redirect('change_password')

        # Hash the new password and update it for the user
        hashed_password = make_password(new_password)
        user.password = hashed_password
        user.save()

        # Update the user's session to keep them logged in
        update_session_auth_hash(request, user)

        messages.success(request, 'Password has been successfully changed.')
        return redirect('change_password')
    return render(request, 'authentication/change_password.html')


def home(request):
    if request.user.is_superuser:
        return redirect('admin_index')
    banners = Banner.objects.all()
    products = Product.objects.all()
    context={
        'products':products,
        'banners':banners,
    }
    return render(request,'home/home.html',context)


def otp_verification(request,phone):
    customuser = CustomUser.objects.get(phone = phone)
    if request.method == "POST":
        code = request.POST.get('otp')
        
        if check(phone,code):
            messages.info(request,"successfully signup please login")
            customuser.is_verified = True
            customuser.save()
            print(customuser,"custommmmmmmmmmmmmmm")
            return redirect('handle_login')
        else:
            pass
    return render(request, 'authentication/otp_verification.html')

