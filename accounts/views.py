from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, SetPasswordForm, PasswordChangeForm
from django.contrib.auth import login
from django.core.cache import cache
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.db import IntegrityError


from .forms import UserCreationForm, UserPasswordResetForm
from .utilities import get_existing_user
from .tokens import user_token_generator
from .tasks import send_async_email
from pufiki190630.utilities import get_form_input_value, is_recaptcha_valid, get_domain


def signup_view(request):
    user = request.user

    if user.is_authenticated:
        return redirect('shop')

    if request.method == 'POST':
        form_email = get_form_input_value(request, 'email')
        existing_nonactive_user = get_existing_user(form_email, False)
        form = UserCreationForm(data=request.POST, instance=existing_nonactive_user)

        if form.is_valid() and is_recaptcha_valid(request):
            # Process data
            user = form.save(commit=False)
            user_email = user.email

            # Get cache context
            cache_context = cache.get(user_email)
            if cache_context is None:
                cache_context = dict()

            # Check if already processed
            if 'signup_user' not in cache_context:
                token = user_token_generator.make_token(user)
                domain = get_domain(request)

                # Modify context and save in cache
                cache_context['signup_user'] = user
                cache.set(user_email, cache_context, 3600)  # One hour

                # Send email to user using Celery
                send_async_email.delay(
                    user_email,
                    'accounts:activate',
                    token,
                    domain,
                    'Подтверждение Вашего электронного адреса',
                    'Для подтверждения Вашего электронного адреса на сайте Pufiki.kz перейдите по ссылке ',
                    'email/activation.html',
                    'Failed sending account activation email to {}'.format(user_email)
                )

            return render(request, 'accounts/success.html', context={
                'title': 'Подтверждение электронного адреса',
                'lines': [
                    'Письмо для подтвеждения Вашего электронного адреса было отправлено на почту '
                    '<strong>{}</strong>.'.format(user_email),
                    'Пожалуйста, проверьте Вашу почту и следуйте инструкциям в письме.',
                    'Если почта пуста, то проверьте спам.',
                ],
            })
    else:
        form = UserCreationForm()

    context = dict()
    context['title'] = 'Создание аккаунта'
    context['form'] = form

    return render(request, 'accounts/signup/signup.html', context)


def activate_view(request, **kwargs):
    user = request.user

    if user.is_authenticated:
        return redirect('shop')

    user_email_b64 = kwargs['user_email_b64']
    token = kwargs['token']

    # Process data
    try:
        user_email = force_text(urlsafe_base64_decode(user_email_b64))
    except(TypeError, ValueError, OverflowError):
        return redirect('accounts:signup')

    # Get user from cache context
    user = None
    cache_context = cache.get(user_email)
    if cache_context and 'signup_user' in cache_context:
        user = cache_context['signup_user']
        cache_context.pop('signup_user')
        if not cache_context:
            cache.set(user_email, cache_context)
        else:
            cache.delete(user_email)

    # Save user
    if user is not None and user_token_generator.check_token(user, token):
        user.is_active = True
        try:
            user.save()
        except IntegrityError:
            return redirect('accounts:signup')
        else:
            login(request, user)

        return render(request, 'accounts/success.html', context={
            'title': 'Готово',
            'lines': [
                'Подтверждение Вашего электронного адреса '
                '<strong>{}</strong> прошло успешно.'.format(user_email),
            ],
        })

    return redirect('accounts:signup')


def login_view(request):
    user = request.user

    if user.is_authenticated:
        return redirect('shop')

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            login(request, form.get_user())
            return redirect('shop')
    else:
        form = AuthenticationForm()

    context = dict()
    context['title'] = 'Войти / Регистрация'
    context['form'] = form

    return render(request, 'accounts/login/login.html', context)


def password_reset_view(request):
    user = request.user

    if user.is_authenticated:
        return redirect('shop')

    if request.method == 'POST':
        form = UserPasswordResetForm(data=request.POST)

        if form.is_valid():
            user_email = form.cleaned_data['email']

            user = get_existing_user(user_email, True)

            # Check cache and send email if not already sent
            cache_context = cache.get(user_email)
            if cache_context is None:
                cache_context = dict()

            if user and 'password_reset_user' not in cache_context:
                cache_context['password_reset_user'] = user
                cache.set(user_email, cache_context, 3600)  # one hour
                form.save(domain_override=get_domain(request))  # Validate form and send email

            return render(request, 'accounts/success.html', context={
                'title': 'Восстановление пароля',
                'lines': [
                    'Письмо для восстановления Вашего пароля было отправлено на почту '
                    '<strong>{}</strong>.'.format(user_email),
                    'Пожалуйста, проверьте Вашу почту и следуйте инструкциям в письме.',
                    'Если почта пуста, то проверьте спам.',
                ]
            })

    else:
        form = UserPasswordResetForm()

    context = dict()
    context['title'] = 'Восстановление пароля'
    context['form'] = form

    return render(request, 'accounts/password/reset.html', context)


def password_set_view(request, **kwargs):
    user = request.user

    if user.is_authenticated:
        return redirect('shop')

    user_email_b64 = kwargs['user_email_b64']
    token = kwargs['token']

    # Process data
    try:
        user_email = force_text(urlsafe_base64_decode(user_email_b64))
    except(TypeError, ValueError, OverflowError):
        return redirect('accounts:password-reset')

    # Find user
    user = get_existing_user(user_email, True)

    if user is None or not user_token_generator.check_token(user, token):
        return redirect('accounts:password-reset')

    if request.method == 'POST':
        form = SetPasswordForm(user, data=request.POST)

        if form.is_valid():
            user = form.save()

            # Clear cache
            cache_context = cache.get(user_email)
            if 'password_reset_user' in cache_context:
                cache_context.pop('password_reset_user')
                if cache_context:
                    cache.set(user_email, cache_context)
                else:
                    cache.delete(user_email)

            login(request, user)
            return render(request, 'accounts/success.html', context={
                'title': 'Готово',
                'lines': [
                    'Вы успешно изменили пароль от своего аккаунта.',
                ]
            })
    else:
        form = SetPasswordForm(user)

    context = dict()
    context['title'] = 'Новый пароль'
    context['form'] = form

    return render(request, 'accounts/password/set.html', context)


def password_change_view(request):
    user = request.user

    if not user.is_authenticated:
        return redirect('accounts:login')

    if request.method == 'POST':
        form = PasswordChangeForm(user, data=request.POST)

        if form.is_valid():
            form.save()
            login(request, user)
            return render(request, 'accounts/success.html', context={
                'title': 'Готово',
                'lines': [
                    'Вы успешно изменили пароль от своего аккаунта.',
                ],
            })
    else:
        form = PasswordChangeForm(user)

    context = dict()
    context['title'] = 'Изменение пароля'
    context['form'] = form

    return render(request, 'accounts/password/change.html', context)
