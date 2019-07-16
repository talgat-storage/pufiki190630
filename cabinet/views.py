from django.shortcuts import render, redirect
from django.db.models import Prefetch
from django.db import IntegrityError

from orders.models import OrderStatus
from support.models import Message
from .forms import UserChangeForm


SECTIONS = [
    ('orders', 'Мои заказы', 'profile:orders'),
    ('chats', 'Мои сообщения', 'profile:chats'),
    ('settings', 'Мои настройки', 'profile:settings'),
]


def profile_orders_view(request):
    user = request.user

    if user.is_anonymous:
        return redirect('accounts:login')

    orders = user.order_set.all() \
        .filter(is_valid=True) \
        .order_by('-id') \
        .prefetch_related(Prefetch('orderstatus_set', OrderStatus.objects.order_by('date')))

    context = dict()
    context['sections'] = SECTIONS
    context['section_name'] = 'orders'
    context['orders'] = orders

    return render(request, 'cabinet/orders.html', context=context)


def profile_order_view(request, **kwargs):
    user = request.user

    if user.is_anonymous:
        return redirect('accounts:login')

    order_slug = kwargs['order_slug']

    order = user.order_set.all() \
        .filter(slug=order_slug, is_valid=True) \
        .prefetch_related(Prefetch('orderstatus_set', OrderStatus.objects.order_by('date'))) \
        .prefetch_related('orderproduct_set') \
        .prefetch_related('orderproduct_set__product') \
        .prefetch_related('orderproduct_set__product__origin') \
        .prefetch_related('orderproduct_set__product__origin__name') \
        .prefetch_related('orderstatus_set') \
        .select_related('user') \
        .first()

    if not order:
        return redirect('profile:orders')

    context = dict()
    context['sections'] = SECTIONS
    context['order'] = order

    return render(request, 'cabinet/order.html', context=context)


def profile_chats_view(request):
    user = request.user

    if user.is_anonymous:
        return redirect('accounts:login')

    chats = user.chat_set.all() \
        .order_by('-id') \
        .prefetch_related(Prefetch('message_set', Message.objects.order_by('date')))

    context = dict()
    context['sections'] = SECTIONS
    context['section_name'] = 'chats'
    context['chats'] = chats

    return render(request, 'cabinet/chats.html', context=context)


def profile_chat_view(request, **kwargs):
    user = request.user

    if user.is_anonymous:
        return redirect('accounts:login')

    chat_slug = kwargs['chat_slug']

    chat = user.chat_set.all() \
        .filter(slug=chat_slug) \
        .prefetch_related(Prefetch('message_set', Message.objects.order_by('date'))) \
        .first()

    if not chat:
        return redirect('profile:chats')

    context = dict()
    context['sections'] = SECTIONS
    context['chat'] = chat

    return render(request, 'cabinet/chat.html', context=context)


def profile_settings_view(request):
    user = request.user

    if user.is_anonymous:
        return redirect('accounts:login')

    if request.method == 'POST':
        user_change_form = UserChangeForm(request.POST, instance=user)

        if user_change_form.is_valid():
            try:
                user_change_form.save()
            except IntegrityError:
                pass
    else:
        user_change_form = UserChangeForm(instance=user)

    context = dict()
    context['sections'] = SECTIONS
    context['section_name'] = 'settings'
    context['user_change_form'] = user_change_form

    return render(request, 'cabinet/settings.html', context=context)
