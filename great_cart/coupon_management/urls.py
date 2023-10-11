from coupon_management import views
from django.urls import path


urlpatterns = [
    path('Gift_management',views.Gift_management,name='Gift_management'),
    path('add_coupon',views.add_coupon,name='add_coupon'),
    path('remove_coupon/<int:id>/',views.remove_coupon,name='remove_coupon'),
]
