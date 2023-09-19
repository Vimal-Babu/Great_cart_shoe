from django.urls import path
from . import views


urlpatterns = [
    path('store',views.store,name='store'),
    path('product_detail/<int:id>/',views.product_detail,name ='product_detail'), #single view of product

]

