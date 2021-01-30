from . import models, choices


def get_sales_by_current_day():
    # TODO arruma isso.
    return models.Sale.objects.all()


def get_sales_by_employee_id(employee_id):
    # TODO vendas diarias
    return models.Sale.objects.filter(employee_id=employee_id)


def get_sale_by_id(_id):
    try:
        return models.Sale.objects.get(pk=_id)
    except models.Sale.DoesNotExist:
        return None


def get_employee_by_id(_id):
    try:
        return models.Employee.objects.get(pk=_id)
    except models.Employee.DoesNotExist:
        return None


def get_products():
    return models.Product.objects.all().order_by('-id')


def get_products_with_high_demand():
    return models.Product.objects.filter(is_high_demand=True).order_by('-id')


def get_employees():
    return models.Employee.objects.filter(is_machine=False).order_by('-id')


def get_product_by_id(_id):
    try:
        return models.Product.objects.get(pk=_id)
    except models.Product.DoesNotExist:
        return None


def get_sale_product_by_id(_id):
    try:
        return models.SaleProduct.objects.get(pk=_id)
    except models.SaleProduct.DoesNotExist:
        return None


def delete_sale_product_by_id(_id):
    sale_product = get_sale_product_by_id(_id)
    if not sale_product:
        return None

    return sale_product.delete()


def filter_products_by_name_or_code(value):
    """Filter Products By Name Or Code

    Note: This function tries filter by name__startswith if can't find
      anything, tries filter by code__startswith. If can't find anything
      again tries filter by name__contains and if can't find anything,
      tries filter by code__contains.

    Args:
        value (str)

    Returns:
        typing.List[models.Product]
    """
    products = models.Product.objects.filter(name__startswith=value)

    if not products:
        products = models.Product.objects.filter(code__startswith=value)

    if not products:
        products = models.Product.objects.filter(name__contains=value)

    if not products:
        products = models.Product.objects.filter(code__contains=value)

    return products


def get_or_create_open_sale_by_employee(employee):
    _sale = models.Sale.objects.filter(employee=employee).last()

    if not _sale or _sale.status == 'finished':
        _sale = models.Sale.objects.create(employee=employee)

    return _sale


def add_products_to_sale(sale, data):
    item = models.SaleProduct.objects.create(sale=sale, **data)
    return item.sale


def get_last_sale_by_employee(employee):
    _sale = models.Sale.objects.last()

    if not _sale or _sale.status == 'finished':
        return None

    return _sale


def finish_sale(sale, employee):
    sale.employee = employee
    sale.status = choices.STATUS_FINISHED
    sale.save()
    return sale


def create_fast_sale(product, employee, quantity, unit_price):

    sale = models.Sale.objects.create(employee=employee)
    sale_product = models.SaleProduct.objects.create(
        sale=sale, product=product, quantity=quantity, unit_price=unit_price
    )
    sale.status = choices.STATUS_FINISHED
    sale.save()
    return sale


def check_employee_password(employee, password) -> bool:
    user = employee.user
    return user.check_password(password)
