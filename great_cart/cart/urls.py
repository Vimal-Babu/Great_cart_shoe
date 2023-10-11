from django.urls import path
from . import views


urlpatterns = [
    path('cart', views.cart, name='cart'),
    path('add_to_cart/<int:id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update_cart/<int:cart_item_id>/', views.update_cart, name='update_cart'),
    path('checkout', views.checkout, name='checkout'),
    path('place_order', views.place_order, name='place_order'),
    # path('place_order/<float:total_price>/', views.place_order, name='place_order'),
    path('order_details', views.order_details, name='order_details'),
    path('order_success/<uuid:order_id>/',views.order_success, name="order_success"),
    path('your_orders_page', views.your_orders_page, name='your_orders_page'),
    path('cancel_order_button/<int:order_id>/', views.cancel_order_button, name='cancel_order_button'),
    path('generate_pdf/<int:order_id>/', views.generate_pdf, name='generate_pdf'),
    path('apply_coupon',views.apply_coupon,name = 'apply_coupon'),
    #path('razorpay_payment_view', views.razorpay_payment_view, name='razorpay_payment_view'),
    #path('pay_by_wallet', views.pay_by_wallet, name='pay_by_wallet'),
]

#path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add-to-cart'),
# path('add_cart/<int:product_id>/', views.add_cart, name='add_cart'),
# path('view_cart', views.view_cart, name='view_cart'),
