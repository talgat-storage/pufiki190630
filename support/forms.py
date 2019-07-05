from django import forms

from .models import Message


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['title', 'body']
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Например: "Доставка за пределы Казахстана"',
            }),
            'body': forms.Textarea(attrs={
                'rows': '5',
                # 'placeholder': '',
            }),
        }
