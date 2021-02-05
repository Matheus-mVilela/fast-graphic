from django import forms

from . import choices


class FilterProductForm(forms.Form):
    value = forms.CharField(label='Buscar produto')


class SaleAddProductForm(forms.Form):
    quantity = forms.IntegerField(label='Quantidade')
    unit_price = forms.FloatField(label='Preço')
    product_id = forms.IntegerField()


class SaleFinishForm(forms.Form):
    payment_method = forms.ChoiceField(
        choices=choices.PAYMENT_METHOD_CHOICES, label='Métodos de Pagamento'
    )
    sale_id = forms.IntegerField()
    employee_id = forms.IntegerField()


class SaleFastCreateForm(forms.Form):
    product_id = forms.IntegerField()
    quantity = forms.IntegerField()
    unit_price = forms.FloatField()
    employee_id = forms.IntegerField()


class SelectEmployeeForm(forms.Form):
    employee_id = forms.IntegerField()


class EmployeePasswordForm(forms.Form):
    employee_password = forms.CharField()
    sale_id = forms.IntegerField()
