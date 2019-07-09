from django.shortcuts import render, redirect
from django.conf import settings
from django.db import IntegrityError

from pufiki190630.utilities import is_recaptcha_valid, get_form_input_value
from shop.utilities import parse_cart
from .models import Order, OrderProduct, OrderStatus
from .forms import NameForm, OrderDetailsForm
from .utilities import bank_register_order


def order_user_view(request):
    user = request.user

    if user.is_authenticated:
        return redirect('orders:details')

    return render(request, 'orders/user.html')


def order_details_view(request):
    user = request.user
    session = request.session

    if request.method == 'POST':
        name_form = NameForm(request.POST)
        order_details_form = OrderDetailsForm(request.POST)

        if (user.is_authenticated or (name_form.is_valid() and is_recaptcha_valid(request))) and order_details_form.is_valid():
            order_name = name_form.save(commit=False)
            order = order_details_form.save(commit=False)

            if user.is_authenticated:
                order.user = user
            else:
                order.name = order_name.name

            if 'is_fast_delivery' in session and session['is_fast_delivery'] is True:
                order.is_fast_delivery = True

            try:
                order.save()
            except IntegrityError:
                pass
            else:
                session['order_slug'] = order.slug
                return redirect('orders:cart')
    else:
        name_form = None if user.is_authenticated else NameForm()
        initial = dict()
        if user.is_authenticated:
            last_order = user.order_set.all().order_by('-id').first()
            if last_order:
                initial = {
                    'phone': last_order.phone,
                    'address': last_order.address,
                    'payment_method': last_order.payment_method,
                }
        order_details_form = OrderDetailsForm(initial=initial)

    context = dict()
    context['name_form'] = name_form
    context['order_details_form'] = order_details_form
    # Recaptcha for anonymous users

    return render(request, 'orders/details.html', context=context)


def order_cart_view(request):
    session = request.session

    if 'cart' not in session or 'order_slug' not in session:
        return redirect('cart')

    cart = session['cart']
    order_slug = session['order_slug']
    order = Order.objects.all().filter(slug=order_slug).first()
    if len(cart) == 0:
        return redirect('cart')
    if order is None:
        return redirect('orders:details')
    
    success, results, total = parse_cart(cart)
    total += settings.FAST_DELIVERY_COST if order.is_fast_delivery else 0

    if request.method == 'POST':
        if str(cart) == get_form_input_value(request, 'cart'):
            for product, origin, quantity, _ in results:
                OrderProduct.objects.create(
                    order=order,
                    product=product,
                    current_price=origin.price,
                    quantity=quantity,
                )

            return redirect('orders:payment')

    order_data = list()
    if order.user is None:
        order_data.extend([
            ('Ваше имя', order.name),
        ])
    order_data.extend([
        ('Ваш телефон', order.phone),
        ('Адрес доставки', order.address),
        ('Быстрая доставка', 'Да' if order.is_fast_delivery else 'Нет'),
        ('Способ оплаты', order.get_payment_method_display())
    ])

    context = dict()
    context['cart'] = str(cart)
    context['results'] = results
    context['delivery_cost'] = settings.FAST_DELIVERY_COST if order.is_fast_delivery else 0
    context['total'] = total
    context['order_data'] = order_data

    return render(request, 'orders/cart.html', context=context)


def order_payment_view(request):
    session = request.session

    if 'order_slug' not in session:
        return redirect('cart')

    order_slug = session['order_slug']
    order = Order.objects.all().filter(slug=order_slug).first()
    if order is None:
        return redirect('cart')

    if order.payment_method == 1:
        OrderStatus.objects.create(order=order, status=1)
        return redirect('orders:done')

    bank_register_order(order_slug)

    return redirect('orders:done')


def order_done_view(request):
    session = request.session

    if 'order_slug' not in session:
        return redirect('cart')

    order_slug = session['order_slug']
    order = Order.objects.all().filter(slug=order_slug).first()
    if order is None:
        return redirect('cart')

    print('Old session')
    for key, value in session.items():
        print(key, value)

    try:
        del session['cart']
        del session['is_fast_delivery']
        del session['order_slug']
    except KeyError:
        pass

    print('Session')
    for key, value in session.items():
        print(key, value)

    context = dict()
    context['order_slug'] = order_slug

    return render(request, 'orders/done.html', context=context)
