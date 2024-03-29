from django.contrib.auth import decorators
from django.urls import path

from . import views

app_name = 'application'


urlpatterns = [
    path(
        '',
        decorators.login_required(views.DashboardView.as_view()),
        name='dashboard',
    ),
    path(
        'sales/<str:id_sale>/',
        decorators.login_required(views.SaleDetailView.as_view()),
        name='sale-detail',
    ),
    path(
        'sales/',
        decorators.login_required(views.SaleCreateView.as_view()),
        name='sale-create',
    ),
    path(
        'sales/add/product',
        decorators.login_required(views.SaleAddProductView.as_view()),
        name='sale-add-product',
    ),
    path(
        'sales/delete/product/<str:id_sale_product>/',
        decorators.login_required(views.SaleDeleteProductView.as_view()),
        name='sale-delete-product',
    ),
    path(
        'sales/finish',
        decorators.login_required(views.SaleFinishView.as_view()),
        name='sale-finish',
    ),
    path(
        'sales/fast',
        decorators.login_required(views.SaleFastView.as_view()),
        name='sale-fast',
    ),
    path(
        'sales/fast/create',
        decorators.login_required(views.SaleFastCreateView.as_view()),
        name='sale-fast-create',
    ),
    path(
        'sales/delete/select/employee',
        decorators.login_required(views.SaleDeleteSelecEmployeeView.as_view()),
        name='sale-delete-select-employee',
    ),
    path(
        'sales/delete/<str:employee_id>/',
        decorators.login_required(views.SaleDeleteView.as_view()),
        name='sale-delete',
    ),
]
