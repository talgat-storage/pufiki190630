from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.http import Http404
from django.db.models import Prefetch
from django.db import connection

from shop.forms import ShopSearchForm, ShopSortForm, CartAddForm, CartDeleteForm
from pufiki190630.utilities import get_form_input_value
from .models import Origin, Product, Picture
from .utilities import parse_cart


HOME_ADVANTAGES = [
    ('Доставка', 'Бесплатная доставка по Казахстану в течение <span class="text-nowrap">1-2 недель</span>', 'img/delivery_125px.png'),
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

        # queries_count = 0

        origins = \
            Origin.objects.all()\
            .filter(is_active=True)\
            .order_by('-popularity')\
            .select_related('name') \
            .prefetch_related(Prefetch('product_set', Product.objects.order_by('id'))) \
            .prefetch_related(Prefetch('product_set__picture_set', Picture.objects.order_by('id'))) \

        origins = origins[:self.CARDS_COUNT]

        # print('Origins:', len(origins), 'queries:', len(connection.queries) - queries_count)
        # queries_count = len(connection.queries)

        popular_results = list()
        for origin in origins:
            products = origin.product_set.all()
            number_of_products = len(products)
            selected_product = products[0]
            pictures = selected_product.picture_set.all()
            popular_results.append((origin, selected_product, number_of_products, pictures))

        # print(results)
        # print('Results:', len(results), 'queries:', len(connection.queries) - queries_count)
        # queries_count = len(connection.queries)

        # print('Total queries:', queries_count)

        context['advantages'] = HOME_ADVANTAGES
        context['popular_results'] = popular_results
        context['steps'] = HOME_STEPS

        return context


class ShopView(TemplateView):
    template_name = 'shop/shop.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # queries_count = 0

        search_form = ShopSearchForm(self.request.GET)
        sort_form = ShopSortForm(self.request.GET)

        origins = Origin.objects.all()
        origins = origins.filter(is_active=True)
        if search_form.is_valid():
            sizes = search_form.cleaned_data['size']
            materials = search_form.cleaned_data['material']
            colors = search_form.cleaned_data['color']

            if sizes:
                origins = origins.filter(size__in=sizes)
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
            else:
                sort_form = ShopSortForm()
        sort = ShopSortForm.SORT_CHOICE_QUERY_MAP[sort_choice]

        origins = \
            origins.distinct() \
            .select_related('name') \
            .prefetch_related(Prefetch('product_set', Product.objects.order_by('id'))) \
            .prefetch_related(Prefetch('product_set__picture_set', Picture.objects.order_by('id'))) \
            .order_by(sort)
        origins = list(origins)

        # print('Origins:', len(origins), 'queries:', len(connection.queries) - queries_count)
        # queries_count = len(connection.queries)

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

        # print(results)
        # print('Results:', len(results), 'queries:', len(connection.queries) - queries_count)
        # queries_count = len(connection.queries)

        # print('Total queries:', queries_count)

        context['search_form'] = search_form
        context['sort_form'] = sort_form
        context['results'] = results
        return context


class OriginView(TemplateView):
    template_name = 'origin/origin.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        origin_slug = context['origin_slug']

        product_color = None
        if 'color' in self.request.GET:
            product_color = self.request.GET['color']

        # queries_count = 0

        origin = Origin.objects.all() \
            .filter(is_active=True, slug=origin_slug) \
            .select_related('name') \
            .prefetch_related(Prefetch('product_set', Product.objects.order_by('id'))) \
            .prefetch_related(Prefetch('product_set__picture_set', Picture.objects.order_by('id'))) \
            .first()

        if not origin:
            raise Http404

        products = origin.product_set.all()
        selected_product = products[0]
        if product_color:
            for product in products:
                if str(product.color) == product_color:
                    selected_product = product
        selected_product_pictures = selected_product.picture_set.all()

        # print('Queries:', len(connection.queries) - queries_count)
        # queries_count = len(connection.queries)

        # print('Total queries:', queries_count)

        quantity = 1
        if 'cart' in self.request.session:
            cart = self.request.session['cart']
            selected_product_slug = selected_product.slug
            if selected_product_slug in cart:
                quantity = cart[selected_product_slug]
        cart_add_form = CartAddForm(initial={'product_slug': selected_product.slug, 'quantity': quantity})

        context['origin'] = origin
        context['products'] = products
        context['product'] = selected_product
        context['pictures'] = selected_product_pictures
        context['cart_add_form'] = cart_add_form
        return context


def cart_view(request):
    session = request.session
    print('Session:', [item for item in session.items()])

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
