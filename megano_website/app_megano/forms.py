from django import forms

from .models import Comment


class CartAddProductForm(forms.Form):
    quantity = forms.CharField(widget=forms.TextInput(attrs={'class': 'Amount-input form-input',
                                                             'type': 'text'}))


class ReviewsForm(forms.ModelForm):
    """Форма для добавления комментариев"""

    class Meta:
        model = Comment
        fields = ['comment', 'name', 'email']
        widgets = {
            'comment': forms.Textarea(attrs={'class': 'form-textarea', 'placeholder': 'Отзыв'}),
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Имя'}),
            'email': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Email'}),
        }
