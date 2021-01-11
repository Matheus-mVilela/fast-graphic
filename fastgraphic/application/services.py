from . import models


def get_sales_by_current_day():
    return models.Sale.objects.all()


def get_sale_by_id(_id):
    try:
        return models.Sale.objects.get(pk=_id)
    except models.Sale.DoesNotExist:
        return None


def get_products():
    return models.Product.objects.all().order_by('-id')


def filter_products_by_name_or_code(value):
    # TODO: add validation to filter by name and code
    return models.Product.objects.filter(name__startswith=value)
