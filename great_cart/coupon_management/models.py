from django.db import models
from django.utils import timezone

class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2)  # Store discount as a decimal (e.g., 10% off)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    # Add more fields as needed, e.g., max_usage, product restrictions, etc.

    def is_valid(self):
        now = timezone.now()
        return self.valid_from <= now <= self.valid_to

    def __str__(self):
        return self.code


# Create your models here.
