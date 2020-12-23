from django.contrib import admin
from .models import Employee, Product, SaleProduct, Sale


admin.site.register(Employee)
admin.site.register(Product)
admin.site.register(SaleProduct)
admin.site.register(Sale)
