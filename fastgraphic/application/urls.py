from django.urls import path
from django.contrib.auth import decorators

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
]

