from django.urls import path
from django.contrib.auth import decorators

from . import views


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
]
