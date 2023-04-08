from django import forms

from orders.models import Order


class OrderForms(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('full_name', 'phone', 'email', 'type_delivery', 'city', 'address', 'type_payment')
        widgets = {
            'full_name': forms.TextInput(
                attrs={'class': 'form-input', 'data-validate': 'require', 'placeholder': 'ФИО'}),
            'phone': forms.TextInput(
                attrs={'class': 'form-input', 'data-validate': 'require', 'placeholder': 'Телефон'}),
            'email': forms.EmailInput(
                attrs={'class': 'form-input', 'data-validate': 'require', 'placeholder': 'Email'}),
            'type_delivery': forms.RadioSelect(),
            'city': forms.TextInput(attrs={'class': 'form-input', 'data-validate': 'require'}),
            'address': forms.TextInput(attrs={'class': 'form-textarea', 'data-validate': 'require'}),
            'type_payment': forms.RadioSelect()
        }


class NumberCard(forms.Form):
    number = forms.CharField(label='Номер карты',
                             widget=forms.TextInput(attrs={'class': 'form-input Payment-bill',
                                                           'placeholder': '9999 9999',
                                                           'data-mask': '9999 9999',
                                                           'data-validate': 'require pay'}))
