from django import shortcuts, views

from . import services


class DashboardView(views.View):
    def get(self, request):
        sales = services.get_sales_by_current_day()
        return shortcuts.render(
            request, 'dashboard/mainpage.html', context={'sales': sales}
        )


class SaleDetailView(views.View):
    def get(self, request, id_sale):
        # products = get_products_by_sale_id(id_sale)
        sale = services.get_sale_by_id(id_sale)
        return shortcuts.render(
            request, 'sales/detail.html', context={'sale': sale}
        )

