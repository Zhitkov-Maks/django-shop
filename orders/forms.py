from django import forms
from django.forms import CharField, RadioSelect, TextInput, EmailInput

from orders.models import Order


class OrderForms(forms.ModelForm):
    class Meta:
        model = Order
        fields: tuple = (
            "full_name",
            "phone",
            "email",
            "type_delivery",
            "city",
            "address",
            "type_payment",
        )
        widgets: dict[str, RadioSelect | TextInput | EmailInput] = {
            "full_name": forms.TextInput(
                attrs={
                    "class": "form-input",
                    "data-validate": "require",
                    "placeholder": "ФИО",
                }
            ),
            "phone": forms.TextInput(
                attrs={
                    "class": "form-input",
                    "data-validate": "require",
                    "placeholder": "Телефон",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "form-input",
                    "data-validate": "require",
                    "placeholder": "Email",
                }
            ),
            "type_delivery": forms.RadioSelect(),
            "city": forms.TextInput(
                attrs={"class": "form-input", "data-validate": "require"}
            ),
            "address": forms.TextInput(
                attrs={"class": "form-textarea", "data-validate": "require"}
            ),
            "type_payment": forms.RadioSelect(),
        }


class NumberCard(forms.Form):
    number: CharField = forms.CharField(
        label="Номер карты",
        widget=forms.TextInput(
            attrs={
                "class": "form-input Payment-bill",
                "placeholder": "9999 9999",
                "data-mask": "9999 9999",
                "data-validate": "require pay",
            }
        ),
    )
