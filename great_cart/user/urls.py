from django.urls import path
from . import views


urlpatterns = [
    path('user_profile', views.user_profile, name='user_profile'),
    path('user_addAddress',views.user_addAddress,name='user_addAddress'),
    path('remove_address/<int:id>/',views.remove_address,name='remove_address'),
    path('edit_address/<int:id>/', views.edit_address, name='edit_address'),

]

