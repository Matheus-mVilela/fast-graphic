from django.db import models
from django.contrib.auth.models import User

import core


class Employee(User):
    ROLE_CHOICES = (
        ('seller', 'Vendedor(a)'),
        ('administrator', 'Administrador(a)'),
    )

    phone = models.CharField(max_length=20)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)


class Product(core.models.BaseModel):
    name = models.CharField(max_length=35)
    price = models.FloatField()
    description = models.CharField(max_length=50)


class SaleItem(core.models.BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    qantity = models.FloatField()
    unit_price = models.FloatField()


class Sale(core.models.BaseModel):
    item = models.ForeignKey(SaleItem, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    discount = models.FloatField()

    @property
    def total_cost(self):

        tot = self.saleitem_set.all().aggregate(
            tot_ped=Sum(
                (F('quantity') * F('price')) - F('discount'),
                output_field=FloatField(),
            )
        )['tot_ped']

        if tot:
            return tot - self.discount
        else:
            return 0

    def __str__(self):

        return f'{self.pk}'

