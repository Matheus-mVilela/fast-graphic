from datetime import datetime

from django.contrib.auth.models import User
from django.core import exceptions
from django.db import models
from django.db.models import Aggregate, F, FloatField, Sum

import core.models

from . import choices


class Employee(core.models.BaseModel):
    ROLE_CHOICES = (
        ('seller', 'Vendedor(a)'),
        ('administrator', 'Administrador(a)'),
    )

    user = models.OneToOneField(
        User, verbose_name='Funcionario', on_delete=models.CASCADE
    )
    phone = models.CharField(max_length=20, verbose_name='Contato')
    role = models.CharField(
        max_length=20, choices=ROLE_CHOICES, verbose_name='Cargo'
    )
    is_machine = models.BooleanField(default=False, verbose_name='Máquina')

    class Meta:
        verbose_name = 'Funcionario'
        verbose_name_plural = 'Funcionarios'

    def __str__(self):
        return f'{self.user.username}'


class Product(core.models.BaseModel):
    code = models.CharField(max_length=30, unique=True, verbose_name='Código')
    name = models.CharField(max_length=35, verbose_name='Nome')
    price = models.FloatField(verbose_name='Preço')
    description = models.CharField(
        max_length=50, null=True, blank=True, verbose_name='Descrição'
    )
    is_high_demand = models.BooleanField(
        default=False, verbose_name='Alta de demanda'
    )

    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'

    def __str__(self):
        return f'{self.name} - {self.price}'


class SaleProduct(core.models.BaseModel):
    sale = models.ForeignKey(
        'Sale', on_delete=models.CASCADE, verbose_name='Venda'
    )
    product = models.ForeignKey(
        'Product', on_delete=models.CASCADE, verbose_name='Produto'
    )
    quantity = models.PositiveIntegerField(verbose_name='Quantidade')
    unit_price = models.FloatField(
        null=True, blank=True, verbose_name='Preço unitário'
    )

    class Meta:
        verbose_name = 'Item da Venda'
        verbose_name_plural = 'Itens da Venda'

    @property
    def total_cost(self):
        return round(self.unit_price * self.quantity, 2)

    def save(self, *args, **kwargs):

        if self.quantity <= 0:
            raise exceptions.ValidationError(
                'Quantity must be grather than zero'
            )

        if not self.unit_price:
            self.unit_price = self.product.price

        return super(SaleProduct, self).save(*args, **kwargs)


class Sale(core.models.BaseModel):
    employee = models.ForeignKey(
        'Employee', on_delete=models.CASCADE, verbose_name='Funcionario'
    )
    discount = models.FloatField(
        null=True, blank=True, verbose_name='Desconto'
    )
    payment_method = models.CharField(
        max_length=20,
        choices=choices.PAYMENT_METHOD_CHOICES,
        null=False,
        blank=False,
        default=choices.MONEY,
        verbose_name='Forma de pagamento',
    )
    status = models.CharField(
        max_length=20,
        choices=choices.STATUS_CHOICES,
        null=False,
        blank=False,
        default=choices.STATUS_OPEN,
    )

    class Meta:
        verbose_name = 'Venda'
        verbose_name_plural = 'Vendas'

    @property
    def total_cost(self):

        total_cost = self.saleproduct_set.all().aggregate(
            total_cost=Sum(
                (F('quantity') * F('unit_price')), output_field=FloatField(),
            )
        )['total_cost']

        if not self.discount:
            self.discount = 0

        if not total_cost:
            return 0

        return round(total_cost - self.discount, 2)

    def __str__(self):
        return f'{self.pk}'

    @property
    def payment_method_display(self):
        _dict = dict(choices.PAYMENT_METHOD_CHOICES)
        return _dict[self.payment_method]

    @classmethod
    def get_by_year(cls, year):
        return Sale.objects.filter(created_at__year=year).order_by(
            '-created_at'
        )

    @classmethod
    def get_by_year_and_month(cls, year, month):
        return Sale.objects.filter(
            created_at__year=year, created_at__month=month
        ).order_by('-created_at')
