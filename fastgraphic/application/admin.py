from django.contrib import admin
from .models import Employee, Product, SaleProduct, Sale


class EmployeeAdmin(admin.ModelAdmin):
    pass


class ProductAdmin(admin.ModelAdmin):
    pass


class SaleProductInline(admin.StackedInline):
    pass


class SaleProductAdmin(admin.ModelAdmin):
    pass


class SaleAdmin(admin.ModelAdmin):
    pass


admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(SaleProduct, SaleProductAdmin)
admin.site.register(Sale, SaleAdmin)

