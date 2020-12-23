from django.db import models
from django.contrib.auth.models import User

import core


class Employee(User):
    ROLE_CHOICES = (
        ('seller', 'Vendedor(a)'),
        ('administrator', 'Administrador(a)'),
    )

    phone = models.CharField(max_length=20)
    role = models.CharField(choices=ROLE_CHOICES)


class Product(core.models.BaseModel):
    # name str
    # price float
    # description str
    pass


class SaleItem(core.models.BaseModel):
    # product = FK to Product
    # unit_price = float
    pass


class Sale(core.models.BaseModel):
    # item = FK to SaleItem
    # employee = FK to Employee
    # total_cost vai ser uma property da soma dos precos dos items
    # discount
    pass

