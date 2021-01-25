from django.contrib.auth.models import User
from django import shortcuts, views
from django.contrib import messages

from . import services, forms, models, choices


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
        employees = services.get_employees()

        try:
            employee = request.user.employee
        except User.employee.RelatedObjectDoesNotExist:
            messages.error(
                request, 'O usuario não tem permição para executar essa ação!',
            )
            return shortcuts.redirect('application:dashboard')

        sale = services.get_last_sale_by_employee(employee)

        return shortcuts.render(
            request,
            'sales/create.html',
            context={
                'products': products,
                'form': form,
                'employees': employees,
                'sale': sale,
                'form_finish_sale': forms.SaleFinishForm(),
            },
        )

    def post(self, request):
        form = forms.FilterProductForm(request.POST)
        if not form.is_valid():
            return shortcuts.redirect('application:sale-create')

        products = services.filter_products_by_name_or_code(form.data['value'])
        form = forms.FilterProductForm()

        try:
            employee = request.user.employee
        except User.employee.RelatedObjectDoesNotExist:
            messages.error(
                request,
                'O usuario logado nao pode adicionar produtos pois nao e funcionario.',
            )
            return shortcuts.redirect('application:sale-create')

        sale = services.get_last_sale_by_employee(employee)
        employees = services.get_employees()

        return shortcuts.render(
            request,
            'sales/create.html',
            context={
                'products': products,
                'form': form,
                'sale': sale,
                'employees': employees,
                'form_finish_sale': forms.SaleFinishForm(),
            },
        )


class SaleAddProductView(views.View):
    def post(self, request):
        form = forms.SaleAddProductForm(request.POST)
        if not form.is_valid():
            return shortcuts.redirect('application:sale-create')

        try:
            employee = request.user.employee
        except User.employee.RelatedObjectDoesNotExist:
            messages.error(
                request,
                'O usuario logado nao pode adicionar produtos pois nao e funcionario.',
            )
            return shortcuts.redirect('application:sale-create')

        product = services.get_product_by_id(form.data['product_id'])
        data = {
            'product': product,
            'quantity': int(form.data['quantity']),
            'unit_price': float(form.data['unit_price']),
        }

        sale = services.get_or_create_open_sale_by_employee(employee)
        sale = services.add_products_to_sale(sale, data)

        return shortcuts.redirect('application:sale-create')


class SaleDeleteProductView(views.View):
    def get(self, request, id_sale_product):
        sale_product_deleted = services.delete_sale_product_by_id(
            id_sale_product
        )

        if not sale_product_deleted:
            messages.warning(
                request, f'O item de id {id_sale_product} não existe.',
            )

        return shortcuts.redirect('application:sale-create')


class SaleFinishView(views.View):
    def post(self, request):
        form = forms.SaleFinishForm(request.POST)
        if not form.is_valid():
            messages.error(
                request,
                'Não foi possivel finalizar a venda. Verifique se o funcionario foi selecionado!',
            )
            return shortcuts.redirect('application:sale-create')

        employee = services.get_employee_by_id(form.data['employee_id'])
        if not employee:
            messages.warning(
                request,
                f'O empregado com id {form.data["employee_id"]} não existe.',
            )
            return shortcuts.redirect('application:sale-create')

        sale = services.get_sale_by_id(form.data['sale_id'])
        if not sale:
            messages.warning(
                request, f'A vendo com id {form.data["sale_id"]} não existe.',
            )
            return shortcuts.redirect('application:sale-create')

        sale_finished = services.finish_sale(sale, employee)
        if sale_finished.status == choices.STATUS_OPEN:
            messages.warning(
                request, f'Falha ao finalizar a venda.',
            )
            return shortcuts.redirect('application:sale-create')

        messages.success(
            request, f'A venda foi finalizada com sucesso!!!',
        )
        return shortcuts.redirect('application:dashboard')


class SaleFastView(views.View):
    def get(self, request):
        form = forms.FilterProductForm()
        products = services.get_products_with_high_demand()
        employees = services.get_employees()

        try:
            employee = request.user.employee
        except User.employee.RelatedObjectDoesNotExist:
            messages.error(
                request, 'O usuario não tem permição para executar essa ação!',
            )
            return shortcuts.redirect('application:dashboard')

        return shortcuts.render(
            request,
            'sales/create-fast-sale.html',
            context={
                'products': products,
                'form': form,
                'employees': employees,
                'form_sale': forms.SaleFastCreateForm(),
            },
        )

    def post(self, request):
        form = forms.FilterProductForm(request.POST)
        if not form.is_valid():
            return shortcuts.redirect('application:sale-fast')

        products = services.filter_products_by_name_or_code(form.data['value'])
        form = forms.FilterProductForm()

        try:
            employee = request.user.employee
        except User.employee.RelatedObjectDoesNotExist:
            messages.error(
                request,
                'O usuario logado nao pode adicionar produtos pois nao e funcionario.',
            )
            return shortcuts.redirect('application:sale-fast')

        employees = services.get_employees()

        return shortcuts.render(
            request,
            'sales/create-fast-sale.html',
            context={
                'products': products,
                'form': form,
                'employees': employees,
                'form_sale': forms.SaleFastCreateForm(),
            },
        )


class SaleFastCreateView(views.View):
    def post(self, request):
        form = forms.SaleFastCreateForm(request.POST)
        if not form.is_valid():
            messages.error(request, 'Não foi possivel efetuar a venda')
            return shortcuts.redirect('application:sale-fast')

        employee = services.get_employee_by_id(form.data['employee_id'])

        if not employee:
            messages.warning(
                request,
                f'O empregado com id {form.data["employee_id"]} não existe.',
            )
            return shortcuts.redirect('application:sale-fast')

        product = services.get_product_by_id(form.data['product_id'])
        quantity = form.cleaned_data['quantity']
        unit_price = form.cleaned_data['unit_price']

        services.create_fast_sale(product, employee, quantity, unit_price)

        messages.success(
            request, f'A venda foi finalizada com sucesso!!!',
        )
        return shortcuts.redirect('application:dashboard')

