from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.db.models import Prefetch
from django.urls import reverse

from shop.forms import ShopSearchForm, ShopSortForm, CartAddForm, CartDeleteForm
from .models import Origin, Product, Picture
from .utilities import parse_cart


COMMON_META_DESCRIPTION = '{} качественных и комфортных кресло-мешков, бинбэгов и пуфиков. '\
                        'Доставка по Казахстану. '\
                        'Оплата банковской картой или наличными курьеру.'

HOME_META_DESCRIPTION = COMMON_META_DESCRIPTION.format('Интернет-магазин')

SHOP_META_DESCRIPTION = COMMON_META_DESCRIPTION.format('Каталог')

HOME_ADVANTAGES = [
    ('Доставка', 'Доставка по Казахстану в течение <span class="text-nowrap">1-2 недель</span>', 'img/delivery_125px.png'),
    ('Способ оплаты', 'Вы можете оплатить покупку наличными, а также банковской картой через интернет', 'img/wallet_125px.png'),
    ('Замена или возврат', 'Вы легко можете заменить или вернуть товар в течение 14 дней после получения товара', 'img/refresh_125px.png'),
    ('Поддержка', 'Помощь покупателям в выборе и оформлении заказа', 'img/support_125px.png'),
]

HOME_STEPS = [
    ('Выберите товары, которые Вам понравились, и добавьте их в <strong>корзину</strong>.', 'img/1_circle_125px.png'),
    ('Проверьте <strong>корзину</strong> и перейдите к <strong>оформлению заказа</strong>.', 'img/2_circle_125px.png'),
    ('Укажите <strong>адрес доставки</strong> и удобный <strong>способ оплаты</strong>.', 'img/3_circle_125px.png'),
    ('<strong>Готово!</strong> Ваш заказ оформлен и находится в обработке.', 'img/checked_circle_125px.png'),
]


class HomeView(TemplateView):
    template_name = 'home/home.html'
    CARDS_COUNT = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        origins = \
            Origin.objects.all() \
            .filter(is_active=True) \
            .order_by('-popularity') \
            .prefetch_related(Prefetch('product_set', Product.objects.order_by('id'))) \
            .prefetch_related(Prefetch('product_set__picture_set', Picture.objects.order_by('id'))) \

        origins = origins[:self.CARDS_COUNT]

        popular_results = list()
        for origin in origins:
            products = origin.product_set.all()
            number_of_products = len(products)
            selected_product = products[0]
            pictures = selected_product.picture_set.all()
            popular_results.append((origin, selected_product, number_of_products, pictures))

        context['meta_description'] = HOME_META_DESCRIPTION
        context['indexed'] = True
        context['advantages'] = HOME_ADVANTAGES
        context['steps'] = HOME_STEPS
        context['popular_results'] = popular_results

        return context


class ShopView(TemplateView):
    template_name = 'shop/shop.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        search_form = ShopSearchForm(self.request.GET)
        sort_form = ShopSortForm(self.request.GET)

        origins = Origin.objects.all()
        origins = origins.filter(is_active=True)
        if search_form.is_valid():
            # sizes = search_form.cleaned_data['size']
            materials = search_form.cleaned_data['material']
            colors = search_form.cleaned_data['color']

            # if sizes:
            #     origins = origins.filter(size__in=sizes)
            if materials:
                origins = origins.filter(material__in=materials)
            if colors:
                origins = origins.filter(product__color__in=colors)
        else:
            colors = list()

        sort_choice = '3'
        if sort_form.is_valid():
            sort_form_choice = sort_form.cleaned_data['sort']
            if sort_form_choice:
                sort_choice = sort_form_choice
                context['canonical_link'] = reverse('shop')
            else:
                sort_form = ShopSortForm()
        sort = ShopSortForm.SORT_CHOICE_QUERY_MAP[sort_choice]

        origins = \
            origins.distinct() \
            .prefetch_related(Prefetch('product_set', Product.objects.order_by('id'))) \
            .prefetch_related(Prefetch('product_set__picture_set', Picture.objects.order_by('id'))) \
            .order_by(sort)
        origins = list(origins)

        results = list()
        for origin in origins:
            products = origin.product_set.all()
            selected_product = products[0]
            if colors:
                for product in products:
                    if str(product.color) in colors:
                        selected_product = product
                        break

            selected_product_pictures = selected_product.picture_set.all()
            results.append((origin, products, selected_product, selected_product_pictures))

        context['meta_description'] = SHOP_META_DESCRIPTION
        context['indexed'] = True
        context['search_form'] = search_form
        context['sort_form'] = sort_form
        context['results'] = results
        return context


def origin_view(request, *args, **kwargs):
    origin_slug = kwargs['origin_slug']

    product_color = None
    if 'color' in request.GET:
        product_color = request.GET['color']

    origin = Origin.objects.all() \
        .filter(is_active=True, slug=origin_slug) \
        .prefetch_related(Prefetch('product_set', Product.objects.order_by('id'))) \
        .prefetch_related(Prefetch('product_set__picture_set', Picture.objects.order_by('id'))) \
        .first()

    if not origin:
        return redirect('shop')

    products = origin.product_set.all()
    selected_product = products[0]
    if product_color:
        for product in products:
            if str(product.color) == product_color:
                selected_product = product
                break
    selected_product_pictures = selected_product.picture_set.all()

    quantity = 1
    if 'cart' in request.session:
        cart = request.session['cart']
        selected_product_slug = selected_product.slug
        if selected_product_slug in cart:
            quantity = cart[selected_product_slug]
    cart_add_form = CartAddForm(initial={'product_slug': selected_product.slug, 'quantity': quantity})

    context = dict()
    if product_color:
        context['canonical_link'] = origin.get_absolute_url()

    context['meta_description'] = '{} {}'.format(origin.description, HOME_META_DESCRIPTION)
    context['indexed'] = True
    context['origin'] = origin
    context['products'] = products
    context['product'] = selected_product
    context['pictures'] = selected_product_pictures
    context['cart_add_form'] = cart_add_form

    return render(request, 'origin/origin.html', context=context)


def cart_view(request):
    session = request.session
    # print('Session:', [item for item in session.items()])

    results = None
    total = None
    cart_delete_form = None

    if 'cart' in session:
        cart = session['cart']
        success, results, total = parse_cart(cart)
        if success:
            cart_delete_form = CartDeleteForm()

    is_fast_delivery = False
    if 'is_fast_delivery' in session:
        is_fast_delivery = session['is_fast_delivery']

    context = dict()
    context['results'] = results
    context['total'] = total
    context['cart_delete_form'] = cart_delete_form
    context['is_fast_delivery'] = is_fast_delivery

    return render(request, 'cart/cart.html', context=context)
