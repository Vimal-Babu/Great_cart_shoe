from django.urls import path
from . import views


urlpatterns = [
    path('admin_login',views.admin_login,name = 'admin_login'),
    path('admin_index',views.admin_index,name='admin_index'), 
    
    
    path('handle_product',views.handle_product,name ='handle_product'),
    path('add_product',views.add_product,name = 'add_product'),
    path('product_block/<int:id>/', views.product_block, name='product_block'),
    path('product_unblock/<int:id>/',views.product_unblock,name = 'product_unblock'),
    path('edit_product/<int:product_id>/', views.edit_product, name='edit_product'),
    
    #category..........
    path('category',views.category_management,name='category_management'),
    path('add_category',views.add_category,name = 'add_category'),
    path('category_block/<id>',views. category_block,name="category_block"),
    path('category_unblock/<id>',views. category_unblock,name="category_unblock"),
    path('category/edit/<int:id>',views.edit_category,name="edit_category"),
    
    path('handle_logout',views.handle_logout,name = 'handle_logout'),
    
    path('user',views.user,name = 'user'),
    path('user_block/<id>',views.user_block,name = 'user_block'),
    path('user_unblock/<id>',views.user_unblock,name = 'user_unblock'),
    
    
    path('brand',views.brand,name = 'brand'),
    path('add_brand',views.add_brand,name = 'add_brand'),
    path('edit_brand/<int:id>',views.edit_brand,name = 'edit_brand'),
    path('delete_brand/<int:id>',views.delete_brand,name = 'delete_brand'),
    
    path('list_order',views.list_order,name = 'list_order'),
    path('cancel_order/<id>',views.cancel_order,name = 'cancel_order'),
    path('manage_status/<int:order_id>/', views.manage_status, name='manage_status'),
    
    
    path('Banner_management',views.Banner_management,name = 'Banner_management'),
    path('add_banner',views.add_banner,name = 'add_banner'),
    path('remove_banner/<int:id>',views.remove_banner,name = 'remove_banner'),
    path('generate_sales_report_pdf', views.generate_sales_report_pdf, name='generate_sales_report_pdf'),
    
    path('add_multiple_image',views.add_multiple_image,name ='add_multiple_image'),
    
    path('search',views.search,name = 'search'),
    path('search_suggestions',views.search_suggestions,name = 'search_suggestions'),
]
