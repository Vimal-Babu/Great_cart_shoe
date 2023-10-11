from django.contrib import admin
from .models import Coupon


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount', 'valid_from', 'valid_to')
    list_filter = ('valid_from', 'valid_to')
    search_fields = ('code',)

# Register your models here.
