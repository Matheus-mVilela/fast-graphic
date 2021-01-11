from . import models


def get_sales_by_current_day():
    return models.Sale.objects.all()


def get_sale_by_id(_id):
    try:
        return models.Sale.objects.get(pk=_id)
    except models.Sale.DoesNotExist:
        return None
