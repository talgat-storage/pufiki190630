from django import forms

from .models import Chat, Message


class ChatForm(forms.ModelForm):
    class Meta:
        model = Chat
        fields = ['title']
        widgets = {
            'title': forms.TextInput(attrs={
                'autofocus': True,
            }),
        }


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={
                'rows': '5',
            }),
        }
