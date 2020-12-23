from django.contrib import admin
from .models import Employee, Product, SaleItem, Sale


admin.site.register(Employee)
admin.site.register(Product)
admin.site.register(SaleItem)
admin.site.register(Sale)
