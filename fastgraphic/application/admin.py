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
    list_display = ('code', 'name', 'price')
    search_filed = ['name', 'code']
    list_filter = ['is_high_demand']


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
        'created_at',
    ]
    search_fields = ['payment_method']

