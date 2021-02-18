import datetime

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
    list_per_page = 15
    exclude = ('total',)
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
    change_list_template = 'admin/sales/sale_change_list.html'

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}

        now = datetime.datetime.now()
        labels_month, total_cost_list = self._mount_data(now.year, now.month)
        last_year_labels_month, last_year_total_cost_list = self._mount_data(
            now.year - 1, now.month
        )

        extra_context['current_revenues'] = {
            'labels': ','.join(['"{}"'.format(data) for data in labels_month]),
            'label': f'Receitas {now.year}',
            'data': ','.join(
                ['"{}"'.format(data) for data in total_cost_list]
            ),
        }
        extra_context['last_revenues'] = {
            'labels': ','.join(
                ['"{}"'.format(data) for data in last_year_labels_month]
            ),
            'label': f'Receitas {now.year - 1}',
            'data': ','.join(
                ['"{}"'.format(data) for data in last_year_total_cost_list]
            ),
        }
        return super(SaleAdmin, self).changelist_view(request, extra_context)

    def _mount_data(self, year, month):
        sales = models.Sale.get_by_year(year)

        data = {}
        for sale in sales:
            _month = sale.created_at.month

            if _month not in data.keys():
                data[_month] = sale.total_cost
            else:
                data[_month] += sale.total_cost

        labels_month = []
        total_cost_list = []
        months = [
            'Janeiro',
            'Fevereiro',
            'Março',
            'Abril',
            'Maio',
            'Junho',
            'Julho',
            'Agosto',
            'Setembro',
            'Outubro',
            'Novembro',
            'Dezembro',
        ]
        for idx, _month in enumerate(months):
            idx += 1

            if idx > month:
                continue

            if idx not in data.keys():
                data[idx] = 0

            total_cost_list.append(data[idx])
            labels_month.append(_month)

        return labels_month, total_cost_list
