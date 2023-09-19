from django.urls import path
from . import views
from django.contrib.auth.views import LoginView


urlpatterns = [
    # path('', views.homepage, name='homepage'),
    path('',views.home,name='home'),
    path('register',views.register,name='register'),
    path('login',views.handle_login,name='handle_login'),
    path('user_logout',views.user_logout,name ='user_logout'),
    path('forget_password',views.forget_password,name='forget_password'),
    path('change_password',views.change_password,name='change_password'),
    path('otp_verification/<str:phone>/',views.otp_verification,name='otp_verification'),
    path('resetting_password/<str:phone>/',views.resetting_password,name='resetting_password'),
    path('change_password_otp/<str:phone>/',views.change_password_otp,name='change_password_otp'),
]

