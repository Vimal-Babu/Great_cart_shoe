from django.urls import path
from . import views
from admin_panel.models import Product


urlpatterns = [
    path('store',views.store,name='store'),
    path('product_detail/<int:id>/',views.product_detail,name ='product_detail'), #single view of product
    path('men',views.men,name='men'),
    path('Woman',views.Woman,name='Woman'),
    path('kids',views.kids,name='kids'),
    path('adidas',views.adidas,name='adidas'),
    path('puma',views.puma,name='puma'),
    path('nike',views.nike,name='nike'),
    path('vance',views.vance,name='vance'),
    path('filter_products',views.filter_products,name='filter_products'),

]

