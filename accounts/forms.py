from django.contrib.auth.forms import \
    UserCreationForm as BaseUserCreationForm, \
    UserChangeForm as BaseUserChangeForm, \
    PasswordResetForm

from .models import User
from .tokens import user_token_generator
from .tasks import send_async_email


class UserCreationForm(BaseUserCreationForm):
    class Meta(BaseUserCreationForm.Meta):
        model = User
        fields = ('name', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'autofocus': True,
                                                 'placeholder': 'Например, Дамир Ануарович или Дамир'})
        self.fields['email'].widget.attrs.update({'autofocus': False,
                                                  'placeholder': 'Например, damir@mail.ru'})


class UserChangeForm(BaseUserChangeForm):
    class Meta(BaseUserChangeForm.Meta):
        model = User


class UserPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'autofocus': True})

    def save(self, domain_override=None,
             subject_template_name='registration/password_reset_subject.txt',
             email_template_name='registration/password_reset_email.html',
             use_https=False, token_generator=user_token_generator,
             from_email=None, request=None, html_email_template_name=None,
             extra_email_context=None):

        user_email = self.cleaned_data["email"]
        domain = domain_override

        for user in self.get_users(user_email):
            token = token_generator.make_token(user)
            # Send email to user using Celery
            send_async_email.delay(
                user_email,
                'accounts:password-set',
                token,
                domain,
                'Восстановление пароля',
                'Для восстановления пароля от Вашего аккаунта на сайте Pufiki.kz перейдите по ссылке ',
                'email/password-reset.html',
                'Failed sending password reset email to {}'.format(user_email)
            )
