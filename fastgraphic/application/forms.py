from django import forms


class FilterProductForm(forms.Form):
    value = forms.CharField(label='Buscar produto')


class SaleAddProductForm(forms.Form):
    quantity = forms.IntegerField(label='Quantidade')
    unit_price = forms.FloatField(label='Preço')
    product_id = forms.IntegerField()


class SaleFinishForm(forms.Form):
    sale_id = forms.IntegerField()
    employee_id = forms.IntegerField()


class SaleFastCreateForm(forms.Form):
    product_id = forms.IntegerField()
    quantity = forms.IntegerField()
    unit_price = forms.FloatField()
    employee_id = forms.IntegerField()
