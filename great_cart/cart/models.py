from django.db import models
from authentication.models import CustomUser
from admin_panel.models import Product

# Create your models here.



class CartItem(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    cart_price = models.PositiveIntegerField(default=0)

    
    def __str__(self):
        return self.user
    

