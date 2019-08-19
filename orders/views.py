from django.shortcuts import render, redirect
from django.db.models import Count
from django.urls import reverse
from django.conf import settings
from django.db import IntegrityError

from pufiki190630.utilities import get_form_input_value, is_recaptcha_valid, get_domain
from shop.utilities import parse_cart
from .models import Order, OrderProduct
from .forms import NameForm, AddressForm, OrderDetailsForm
from .utilities import bank_register_order, bank_order_status, send_order_confirmation, delete_key_from_session


ORDER_STEPS = [
    'Доставка',
    'Подтверждение',
    'Оплата',
    'Готово',
]


def order_user_view(request):
    user = request.user

    if user.is_authenticated:
        return redirect('orders:details')

    context = dict()
    context['order_steps'] = ORDER_STEPS
    context['current_order_step_number'] = 0

    return render(request, 'orders/user.html', context=context)


def order_details_view(request):
    user = request.user
    session = request.session
    # print('Session:', [item for item in session.items()])

    if request.method == 'POST':
        name_form = NameForm(request.POST)
        address_form = AddressForm(request.POST)
        order_details_form = OrderDetailsForm(request.POST)

        if (user.is_authenticated or (name_form.is_valid() and is_recaptcha_valid(request))) \
                and address_form.is_valid() \
                and order_details_form.is_valid():
            order_name = name_form.save(commit=False) if not user.is_authenticated else None
            address = address_form.save(commit=False)
            order = order_details_form.save(commit=False)

            # Depending on anonymity, set name or user
            if user.is_authenticated:
                order.user = user
            else:
                order.name = order_name.name

            # Save address and set address in order
            address.save()
            order.address = address

            # Set is_fast_delivery flag using data from session
            if 'is_fast_delivery' in session and session['is_fast_delivery'] is True:
                order.is_fast_delivery = True

            # Delete invalid old order using order slug from session
            if 'order_slug' in session:
                old_order_slug = session['order_slug']
                old_order = Order.objects.all().filter(slug=old_order_slug, is_valid=False).first()
                if old_order:
                    old_order.delete()
                    # print('Delete order', old_order_slug)
                try:
                    del session['order_slug']
                    # print('Delete order_slug from session')
                except KeyError:
                    pass

            # Save new order and set new order slug in session
            try:
                order.save()
            except IntegrityError:
                pass
            else:
                session['order_slug'] = order.slug
                # print('Order slug:', order.slug)
                return redirect('orders:cart')
        else:
            address_form.add_error('another_city', 'Необходимо для заполнения')
    else:
        name_form = None if user.is_authenticated else NameForm()
        # Get initial data from valid old order
        address_initial = dict()
        details_initial = dict()
        if user.is_authenticated:
            last_order = user.order_set.all().filter(is_valid=True).order_by('date_created').last()
            if last_order:
                address = last_order.address
                address_initial = {
                    'city': address.city,
                    'street': address.street,
                    'house': address.house,
                    'flat': address.flat,
                    'phone': address.phone,
                }
                details_initial = {
                    'payment_method': last_order.payment_method,
                }
        address_form = AddressForm(initial=address_initial)
        order_details_form = OrderDetailsForm(initial=details_initial)

    context = dict()
    context['name_form'] = name_form
    context['address_form'] = address_form
    context['address_form_city_datalist'] = AddressForm.CITY_DATALIST
    context['order_details_form'] = order_details_form
    context['order_steps'] = ORDER_STEPS
    context['current_order_step_number'] = 1
    # Recaptcha for anonymous users

    return render(request, 'orders/details.html', context=context)


def order_cart_view(request):
    session = request.session
    # print('Session:', [item for item in session.items()])

    if 'cart' not in session:
        return redirect('cart')
    if 'order_slug' not in session:
        return redirect('orders:details')

    cart = session['cart']
    order_slug = session['order_slug']
    order = Order.objects.all().filter(slug=order_slug, is_valid=False).first()
    if len(cart) == 0:
        return redirect('cart')
    if order is None:
        return redirect('orders:details')
    
    success, results, total = parse_cart(cart)
    total += settings.FAST_DELIVERY_COST if order.is_fast_delivery else settings.DELIVERY_COST

    if request.method == 'POST':
        if str(cart) == get_form_input_value(request, 'cart'):
            # Delete any existing order_product objects (in case of resubmission)
            order.orderproduct_set.all().delete()
            # Save new order_product objects
            OrderProduct.objects.bulk_create([
                OrderProduct(
                    order=order,
                    product=product,
                    current_price=origin.price,
                    quantity=quantity,
                )
                for product, origin, quantity, _ in results
            ])

            # Calculate total sum to pay
            # total = order.orderproduct_set.all() \
            #     .aggregate(
            #     total=Sum(F('current_price') * F('quantity'), output_field=PositiveIntegerField())
            # )['total']
            # total += settings.FAST_DELIVERY_COST if order.is_fast_delivery else 0
            order.total_to_pay = total
            try:
                order.save()
            except IntegrityError:
                pass
            else:
                return redirect('orders:payment')

    order_data = list()
    # Show user name if anonymous
    if order.user is None:
        order_data.extend([
            ('Ваше имя', order.name),
        ])
    order_data.extend([
        ('Ваш телефон', order.address.phone),
        ('Адрес доставки', ', '.join([
            'г. ' + order.address.city,
            'ул. ' + order.address.street,
            'д. ' + order.address.house,
            'кв./оф. ' + order.address.flat,
        ])),
        ('Быстрая доставка', 'Да' if order.is_fast_delivery else 'Нет'),
        ('Способ оплаты', order.get_payment_method_display())
    ])

    context = dict()
    context['cart'] = str(cart)
    context['results'] = results
    context['delivery_cost'] = settings.FAST_DELIVERY_COST if order.is_fast_delivery else settings.DELIVERY_COST
    context['total'] = total
    context['order_data'] = order_data
    context['order_steps'] = ORDER_STEPS
    context['current_order_step_number'] = 2

    return render(request, 'orders/cart.html', context=context)


def order_payment_view(request):
    session = request.session
    # print('Session:', [item for item in session.items()])

    if 'order_slug' not in session:
        # print('No order slug')
        return redirect('cart')

    order_slug = session['order_slug']
    order = Order.objects.all() \
        .prefetch_related('orderproduct_set').annotate(products_count=Count('orderproduct')) \
        .filter(slug=order_slug, is_valid=False, products_count__gt=0, total_to_pay__gt=0) \
        .first()
    if order is None:
        # print('No order or order products')
        return redirect('cart')

    # Redirect to 'done' if payment method is cash
    if order.payment_method == 1:
        # Make order valid and save
        order.is_valid = True
        order.save()
        return redirect('orders:done')

    # Redirect to form URL if any
    if 'bank_form_url' in session:
        return redirect(session['bank_form_url'])

    # Register a new bank order
    bank_result = bank_register_order(
        order_slug,
        order.total_to_pay,
        request.build_absolute_uri(reverse('orders:payment-check'))
    )

    # If success, save order ID and form URL in session and redirect to bank form url
    if 'orderId' in bank_result and 'formUrl' in bank_result:
        session['bank_order_id'] = bank_result['orderId']
        session['bank_form_url'] = bank_result['formUrl']
        # print('Bank Order ID:', session['bank_order_id'])
        # print('Bank Form URL:', session['bank_form_url'])
        return redirect(session['bank_form_url'])

    # Else, render payment-registration-error with specified error and suggest going to details
    if 'errorCode' in bank_result and 'errorMessage' in bank_result:
        return render(request, 'orders/payment-error.html', context={
            'error_code': bank_result['errorCode'],
            'error_message': bank_result['errorMessage'],
            'order_steps': ORDER_STEPS,
            'current_order_step_number': 3,
        })

    return redirect('orders:details')


def order_payment_check_view(request):
    session = request.session
    # print('Session:', [item for item in session.items()])

    if 'order_slug' not in session or 'bank_order_id' not in session:
        # print('No order slug or bank_order_id')
        return redirect('orders:details')

    order_slug = session['order_slug']
    order = Order.objects.all().filter(slug=order_slug, is_valid=False).first()
    if order is None:
        # print('No order')
        return redirect('orders:details')

    # Get payment results using order ID
    bank_result = bank_order_status(session['bank_order_id'])

    context = dict()
    context['order_steps'] = ORDER_STEPS
    context['current_order_step_number'] = 3

    # If error, render payment-check-error with specified error and suggest going to details
    if 'OrderStatus' not in bank_result or bank_result['OrderStatus'] != 2:
        if 'bank_error_count' not in session:
            session['bank_error_count'] = 0

        bank_error_count = session['bank_error_count']
        bank_error_count += 1
        session['bank_error_count'] = bank_error_count

        if bank_error_count < 3:
            return redirect('orders:payment')
        else:
            delete_key_from_session(session, 'bank_error_count')
            delete_key_from_session(session, 'bank_order_id')
            delete_key_from_session(session, 'bank_form_url')
            context['error_code'] = bank_result['ErrorCode'] if 'ErrorCode' in bank_result else None
            context['error_message'] = bank_result['ErrorMessage'] if 'ErrorMessage' in bank_result else None
            return render(request, 'orders/payment-error.html', context=context)

    delete_key_from_session(session, 'bank_error_count')
    delete_key_from_session(session, 'bank_form_url')

    # Check bank order slug
    if 'OrderNumber' not in bank_result or bank_result['OrderNumber'] != order_slug:
        # print('No bank order slug or bank order slug is different')
        context['error_message'] = 'Номер заказа в системе магазина отличается от номера заказа в банке'
        return render(request, 'orders/payment-error.html', context=context)

    # Check bank amount
    if 'Amount' not in bank_result or bank_result['Amount'] != order.total_to_pay * 100:
        # print('No bank ammount or bank amount is different')
        context['error_message'] = 'Сумма платежа в системе магазина отличается от суммы платежа в банке'
        return render(request, 'orders/payment-error.html', context=context)

    # Check bank currency
    if 'currency' not in bank_result or bank_result['currency'] != settings.BANK_CURRENCY:
        # print('No currency or bank currency is different')
        context['error_message'] = 'Код валюты платежа в системе магазина отличается от кода валюты платежа в банке'
        return render(request, 'orders/payment-error.html', context=context)

    # If success, save bank order id, make order valid, save it and redirect to done
    order.bank_id = session['bank_order_id']
    order.is_valid = True
    order.save()
    delete_key_from_session(session, 'bank_order_id')
    return redirect('orders:done')


def order_done_view(request):
    session = request.session
    # print('Session:', [item for item in session.items()])

    if 'order_slug' not in session:
        return redirect('cart')

    # Order should be valid
    order_slug = session['order_slug']
    order = Order.objects.all().filter(slug=order_slug, is_valid=True).first()
    if order is None:
        return redirect('orders:details')

    # Clear session
    try:
        if 'cart' in session:
            del session['cart']
        if 'is_fast_delivery' in session:
            del session['is_fast_delivery']
        if 'order_slug' in session:
            del session['order_slug']
    except KeyError:
        pass

    # print('Session:', [item for item in session.items()])

    # Send email to user
    if order.user:
        send_order_confirmation.delay(
            order.user.email,
            order_slug,
            get_domain(request)
        )

    context = dict()
    context['order_slug'] = order.slug
    context['order_steps'] = ORDER_STEPS
    context['current_order_step_number'] = 4

    return render(request, 'orders/done.html', context=context)
