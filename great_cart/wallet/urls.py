from django.urls import path
from wallet import views

urlpatterns = [
    path('my_wallet',views.my_wallet,name = "my_wallet")
]
