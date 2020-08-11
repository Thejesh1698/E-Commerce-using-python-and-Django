from django.contrib import admin
from .models import Product, ProductType, ProductBrand
# Register your models here.

admin.site.register(Product)
admin.site.register(ProductType)
admin.site.register(ProductBrand)


