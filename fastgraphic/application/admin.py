from django.contrib import admin
from . import models


@admin.register(models.Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'phone',
        'role',
    )


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    pass


class SaleProductInline(admin.StackedInline):
    model = models.SaleProduct
    extra = 1


@admin.register(models.Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'employee',
        'total_cost',
    )
    inlines = [SaleProductInline]
    list_filter = [
        'payment_method',
    ]

