from django.db import models
from django.contrib.auth.models import User
from django.core import exceptions
from django.db.models import Sum, F, FloatField, Aggregate

import core.models


class Employee(core.models.BaseModel):
    ROLE_CHOICES = (
        ('seller', 'Vendedor(a)'),
        ('administrator', 'Administrador(a)'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return f'{self.user.username}'


class Product(core.models.BaseModel):
    name = models.CharField(max_length=35)
    price = models.FloatField()
    description = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f'{self.name} - {self.price}'


class SaleProduct(core.models.BaseModel):
    sale = models.ForeignKey('Sale', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.FloatField()
    unit_price = models.FloatField(null=True, blank=True)

    def save(self, *args, **kwargs):

        if self.quantity <= 0:
            raise exceptions.ValidationError(
                'Quantity must be grather than zero'
            )

        if not self.unit_price:
            self.unit_price = self.product.price

        return super(SaleProduct, self).save(*args, **kwargs)


class Sale(core.models.BaseModel):
    employee = models.ForeignKey('Employee', on_delete=models.CASCADE)
    discount = models.FloatField(null=True, blank=True)

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

        return total_cost - self.discount

    def __str__(self):
        return f'{self.pk}'
