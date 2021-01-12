from django import shortcuts, views

from . import services, forms


class DashboardView(views.View):
    def get(self, request):
        sales = services.get_sales_by_current_day()
        return shortcuts.render(
            request, 'dashboard/mainpage.html', context={'sales': sales}
        )


class SaleDetailView(views.View):
    def get(self, request, id_sale):
        sale = services.get_sale_by_id(id_sale)
        return shortcuts.render(
            request, 'sales/detail.html', context={'sale': sale}
        )


class SaleCreateView(views.View):
    def get(self, request):
        form = forms.FilterProductForm()
        products = services.get_products()
        return shortcuts.render(
            request,
            'sales/create.html',
            context={'products': products, 'form': form},
        )

    def post(self, request):
        form = forms.FilterProductForm(request.POST)
        if not form.is_valid():
            return shortcuts.redirect('application:sale-create')

        products = services.filter_products_by_name_or_code(form.data['value'])
        form = forms.FilterProductForm()
        return shortcuts.render(
            request,
            'sales/create.html',
            context={'products': products, 'form': form},
        )
