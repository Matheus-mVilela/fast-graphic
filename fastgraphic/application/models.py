from django.db import models
from django.contrib.auth.models import User

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
    # TODO:
    # - criar validação de (quantidade e unit_price) < 0 == raise
    # - se não existir unit_price, deve preencher o campo com o valor de price de Product


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

        if not total_cost:
            return 0

        return total_cost - self.discount

    def __str__(self):
        return f'{self.pk}'
