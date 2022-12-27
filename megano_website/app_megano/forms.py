from django import forms

from .models import Comment


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
