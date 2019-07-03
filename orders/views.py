from django.shortcuts import render, redirect
from django.core.cache import cache

from .models import Order
from .forms import AnonymousUserForm, OrderDetailsForm
from pufiki190630.utilities import get_form_input_value, is_recaptcha_valid
from accounts.utilities import get_existing_user
from shop.utilities import parse_cart


def order_user_view(request):
    user = request.user

    if user.is_authenticated:
        return redirect('orders:details')

    return render(request, 'orders/user.html')


def order_details_view(request):
    user = request.user
    session = request.session

    if 'cart' not in session or not session['cart']:
        return redirect('cart')

    if request.method == 'POST':
        order_user = None
        if user.is_anonymous:
            form_email = get_form_input_value(request, 'email')
            existing_nonactive_user = get_existing_user(form_email, False)
            anonymous_user_form = AnonymousUserForm(request.POST, instance=existing_nonactive_user)
            if anonymous_user_form.is_valid():
                order_user = anonymous_user_form.save(commit=False)
        else:
            order_user = user
            anonymous_user_form = None

        order_details_form = OrderDetailsForm(request.POST)

        if order_user and order_details_form.is_valid() and (user.is_authenticated or is_recaptcha_valid(request)):
            order = order_details_form.save(commit=False)
            if user.is_anonymous:
                order.is_fast_checkout = True
                session['anonymous_email'] = order_user.email

            if 'is_fast_delivery' in session and session['is_fast_delivery']:
                order.is_fast_delivery = True

            cache_context = cache.get(order_user.email)
            if cache_context is None:
                cache_context = dict()
            cache_context['order'] = order
            cache_context['order_user'] = order_user
            cache_context['order_next_step'] = 2
            cache.set(order_user.email, cache_context, 3600)  # One hour

            return redirect('orders:cart')
    else:
        anonymous_user_form = AnonymousUserForm() if user.is_anonymous else None
        initial = dict()
        if user.is_authenticated:
            last_nonfast_order = user.order_set.all().filter(is_fast_checkout=False, is_payment_done=True).last()
            if last_nonfast_order:
                initial = {
                    'phone': last_nonfast_order.phone,
                    'address': last_nonfast_order.address,
                    'payment_method': last_nonfast_order.payment_method,
                }
        order_details_form = OrderDetailsForm(initial=initial)

    context = dict()
    context['anonymous_user_form'] = anonymous_user_form
    context['order_details_form'] = order_details_form

    return render(request, 'orders/details.html', context=context)


def order_cart_view(request):
    user = request.user
    session = request.session

    if 'cart' not in session or not session['cart']:
        return redirect('cart')
    cart = session['cart']
    if len(cart) == 0:
        return redirect('cart')

    if user.is_anonymous:
        if 'anonymous_email' not in session:
            return redirect('orders:details')
        user_email = session['anonymous_email']
    else:
        user_email = user.email

    cache_context = cache.get(user_email)
    if cache_context is None or 'order_next_step' not in cache_context or cache_context['order_next_step'] != 2:
        return redirect('orders:details')

    if request.method == 'POST':
        form_cart = get_form_input_value(request, 'cart')
        if form_cart and form_cart == str(cart):
            cache_context['order_next_step'] = 3
            cache_context['order_cart'] = cart
            cache.set(user_email, cache_context, 3600)  # One hour

            return redirect('orders:payment')

    order_user = cache_context['order_user']
    order = cache_context['order']

    success, results, total = parse_cart(cart)
    total += 2900 if order.is_fast_delivery else 0

    order.payment_total = total
    cache_context['order'] = order
    cache.set(user_email, cache_context, 3600)  # One hour

    order_data = list()
    if user.is_anonymous:
        order_data.extend([
            ('Ваше имя', order_user.name),
            ('Ваш электронный адрес', order_user.email),
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
    context['delivery_cost'] = 2900 if order.is_fast_delivery else 0
    context['total'] = total
    context['order_data'] = order_data

    return render(request, 'orders/cart.html', context=context)


# success, results, total = parse_cart(cart)
# for product, _, quantity, product_total in results:
#     order_product_details = OrderProductDetails(
#         product=product,
#         order=order,
#         quantity=quantity,
#         total=product_total
#     )
# order.payment_total = total


def order_payment_view(request):
    user = request.user
    session = request.session

    if user.is_anonymous:
        if 'anonymous_email' not in session:
            return redirect('orders:details')
        user_email = session['anonymous_email']
    else:
        user_email = user.email

    cache_context = cache.get(user_email)
    if cache_context is None or 'order_next_step' not in cache_context or cache_context['order_next_step'] != 3:
        return redirect('orders:details')

    # Temp
    if request.method == 'POST':
        order = cache_context['order']
        order.slug = 12345
        order.is_payment_done = True
        if order.is_payment_done:
            order_slug = order.slug
            return redirect('orders:done', order_slug=order_slug)
    # Temp

    # Future: when saving user with already existing email, IntegrityError is raised
    # Clear cart from session and clear cache

    context = dict()
    # context['order'] = str(cache_context['order'])
    # context['order_user'] = str(cache_context['order_user'])
    # context['order_cart'] = str(cache_context['order_cart'])

    return render(request, 'orders/payment.html', context=context)


def order_done_view(request, **kwargs):
    user = request.user
    session = request.session

    if user.is_anonymous:
        if 'anonymous_email' not in session:
            return redirect('shop')
        user_email = session['anonymous_email']
    else:
        user_email = user.email

    # Clear anonymous_email from session

    order_slug = kwargs['order_slug']

    # order = Order.objects.all() \
    #     .filter(user__email=user_email, slug=order_slug) \
    #     .first()
    #
    # if not order:
    #     return redirect('shop')

    context = dict()
    context['order_slug'] = order_slug

    return render(request, 'orders/done.html', context=context)
