from django import forms

from orders.models import Order


class OrderForms(forms.ModelForm):
    password = forms.CharField(max_length=30, required=False, label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    passwordReplay = forms.CharField(max_length=30, required=False, label='Повторите пароль',
                                     widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = Order
        fields = ('full_name', 'phone', 'email', 'type_delivery', 'city', 'address', 'type_payment')
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'ФИО'}),
            'phone': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Телефон'}),
            'email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Email'}),
            'type_delivery': forms.RadioSelect(),
            'city': forms.TextInput(attrs={'class': 'form-input'}),
            'address': forms.TextInput(attrs={'class': 'form-textarea'}),
            'type_payment': forms.RadioSelect()
        }
