from django import forms


class FilterProductForm(forms.Form):
    value = forms.CharField(label='Buscar produto')

