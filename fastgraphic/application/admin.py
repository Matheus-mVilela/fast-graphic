from django.contrib import admin
from .models import Employee, Product, SaleProduct, Sale


class EmployeeAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            'Dados Pessoais',
            {'fields': ('username', 'password', 'first_name', 'last_name',)},
        ),
        ('Dados Complementares', {'fields': ('email', 'phone', 'role')}),
        (
            'Permissoes do usuario',
            {
                'fields': (
                    'user_permissions',
                    'is_staff',
                    'is_active',
                    'is_superuser',
                )
            },
        ),
    )
    filter_horizontal = [
        'user_permissions',
    ]
    list_display = ('username', 'email', 'phone', 'role')


class ProductAdmin(admin.ModelAdmin):
    pass


class SaleProductInline(admin.StackedInline):
    pass


class SaleProductAdmin(admin.ModelAdmin):
    pass


class SaleAdmin(admin.ModelAdmin):
    def __str__(self):
        pass


admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(SaleProduct, SaleProductAdmin)
admin.site.register(Sale, SaleAdmin)

