from django.db import models
from django.contrib.auth.models import User
from django.core import exceptions
from django.db.models import Sum, F, FloatField, Aggregate
from . import choices
from datetime import datetime

import core.models


class Employee(core.models.BaseModel):
    ROLE_CHOICES = (
        ('seller', 'Vendedor(a)'),
        ('administrator', 'Administrador(a)'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    is_machine = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username}'


class Product(core.models.BaseModel):
    code = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=35)
    price = models.FloatField()
    description = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f'{self.name} - {self.price}'


class SaleProduct(core.models.BaseModel):
    sale = models.ForeignKey('Sale', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    unit_price = models.FloatField(null=True, blank=True)

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
    employee = models.ForeignKey('Employee', on_delete=models.CASCADE,)
    discount = models.FloatField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=choices.STATUS_CHOICES,
        null=False,
        blank=False,
        default=choices.STATUS_OPEN,
    )

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

