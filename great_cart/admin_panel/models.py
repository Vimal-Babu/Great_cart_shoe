from django.db import models

# Create your models here.

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
    image = models.ImageField(upload_to='photo/product', blank=True, null=True)
    stock = models.PositiveIntegerField()
    is_available = models.BooleanField(default=True)
    new_arrivals = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.product_name


class Banner(models.Model):
    image = models.ImageField(upload_to='photo/banners/')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    active = models.BooleanField(default=True)


    def __str__(self):
        return self.image.name

