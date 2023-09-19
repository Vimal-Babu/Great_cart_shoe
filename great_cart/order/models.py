from django.db import models
from authentication.models import CustomUser, Address
from admin_panel.models import Product

# Create your models here..

class Orders(models.Model):
    order_status_choices = [
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled')
    ]
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    order_status = models.CharField(max_length=20, choices=order_status_choices, default='Pending')
    delivery_address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)
    order_date = models.DateTimeField(auto_now_add=True)
    payment_type = models.CharField(max_length=100)
    order_id = models.CharField()
    
    
    def __str__(self):
        return f"Order #{self.id} for {self.user}"
