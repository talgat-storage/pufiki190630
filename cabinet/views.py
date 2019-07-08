from django.shortcuts import render, redirect
from django.db.models import Prefetch

from orders.models import Order, OrderStatus
from support.models import Chat, Message
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

    orders = Order.objects.all() \
        .filter(user=user) \
        .order_by('-id') \
        .prefetch_related(Prefetch('orderstatus_set', OrderStatus.objects.order_by('-date')))

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

    order = Order.objects.all() \
        .filter(slug=order_slug, user=user) \
        .prefetch_related(Prefetch('orderstatus_set', OrderStatus.objects.order_by('-date'))) \
        .prefetch_related('products') \
        .prefetch_related('products__origin') \
        .prefetch_related('products__origin__name') \
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

    chats = Chat.objects.all() \
        .filter(user=user) \
        .order_by('-id') \
        .prefetch_related(Prefetch('message_set', Message.objects.order_by('-date')))

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

    chat = Chat.objects.all() \
        .filter(user=user, slug=chat_slug) \
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
            user = user_change_form.save()

    user_change_form = UserChangeForm(instance=user)

    context = dict()
    context['sections'] = SECTIONS
    context['section_name'] = 'settings'
    context['user_change_form'] = user_change_form

    return render(request, 'cabinet/settings.html', context=context)
