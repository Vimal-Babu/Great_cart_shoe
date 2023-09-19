from django.urls import path
from . import views


urlpatterns = [
    path('user_address', views.user_address, name='user_address'),
]

