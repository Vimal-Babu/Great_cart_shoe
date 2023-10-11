from django.db import models
from authentication.models import CustomUser

# Create your models here.

# class ProductImage(models.Model):
#     product = models.ForeignKey('admin_panel.Product', on_delete=models.CASCADE)
#     image = models.ImageField(upload_to='photo/product_multiple_img')

#     def __str__(self):
#         return self.product.product_name + " Image"
    




class Brand(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='photo/brand', blank=True, null=True)
    description = models.TextField(blank=True, null=True)


    def __str__(self):
        return self.name

class Category(models.Model):
    category_name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.category_name
    


class Product(models.Model):
    product_name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    offer_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0, blank=True, null=True)  # Default to 0 for no initial discount
    image = models.ImageField(upload_to='photo/product', blank=True, null=True)
    stock = models.PositiveIntegerField()
    is_available = models.BooleanField(default=True)
    new_arrivals = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.product_name

    def offer_price(self):
        # Calculate the offer price based on the product's price and offer percentage
        offer_price = self.price - (self.price * (self.offer_percentage / 100))
        return round(offer_price)
        # Round the offer price to the nearest whole number
        
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to='photos/product_multiple_img')

    def __str__(self):
        return f"Image of {self.product.product_name}"
        



    
class Banner(models.Model):
    image = models.ImageField(upload_to='photo/banners/')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True, default=None)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True, default=None)
    active = models.BooleanField(default=True)


    def __str__(self):
        return self.image.name
    
    
class SearchQuery(models.Model):
    # product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Link the search query to a product
    query = models.CharField(max_length=255)  # Store the search query text
    timestamp = models.DateTimeField(auto_now_add=True)  # Store the date and time of the search
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    def __str__(self):
        return f'Search Query: {self.query} for Product: {self.product} on {self.timestamp}'

