from django.views.generic import View, TemplateView
from django.template.response import HttpResponse
from django.http import JsonResponse
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.db.models import Prefetch

from shop.models import Product, Picture
from shop.forms import CartAddForm
from pufiki190630.utilities import get_form_input_value


class ShopCardCarouselView(TemplateView):
    template_name = 'card/card-carousel.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        product = None
        origin = None
        pictures = list()

        if 'product_slug' in self.request.GET:
            product_slug = self.request.GET['product_slug']

            product = \
                Product.objects.all() \
                .filter(origin__is_active=True, slug=product_slug) \
                .select_related('origin') \
                .prefetch_related(Prefetch('picture_set', Picture.objects.order_by('id'))) \
                .first()

            if product:
                origin = product.origin
                pictures = product.picture_set.all()

        context['product'] = product
        context['origin'] = origin
        context['pictures'] = pictures
        context['controls_hidden'] = True
        return context


class CartAddView(View):
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        success = False

        form_product_slug = None
        if 'product_slug' in request.POST:
            form_product_slug = request.POST['product_slug']

        form_quantity = None
        if 'quantity' in request.POST:
            form_quantity = request.POST['quantity']

        product = None
        if form_product_slug:
            product = \
                Product.objects.all() \
                .filter(origin__is_active=True, slug=form_product_slug) \
                .first()

        quantity = None
        if form_quantity:
            quantity_integers, quantity_strings = map(list, zip(*CartAddForm.QUANTITY_CHOICES))
            if form_quantity in quantity_strings:
                quantity = int(form_quantity)

        session = request.session
        if 'cart' not in session:
            session['cart'] = dict()
        cart = session['cart']

        if product and quantity:
            cart[product.slug] = quantity

            session['cart'] = cart
            success = True

        cart_items_count = len(cart)

        context = dict()
        context['success'] = success
        if success:
            context['product'] = product

        alert = render_to_string('api/api-cart-add.html', context)

        return JsonResponse({
            'alert': alert,
            'cart_items_count': cart_items_count,
        })


class CartDeleteView(View):
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        form_product_slug = None
        if 'product_slug' in request.POST:
            form_product_slug = request.POST['product_slug']

        product = None
        if form_product_slug:
            product = \
                Product.objects.all() \
                .filter(origin__is_active=True, slug=form_product_slug) \
                .first()

        if product:
            session = request.session
            if 'cart' not in session:
                session['cart'] = dict()

            cart = session['cart']
            if product.slug in cart:
                cart.pop(product.slug)
                session['cart'] = cart

        return redirect('cart')


class CartDeliveryView(View):
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        session = request.session

        checked = get_form_input_value(request, 'checked')
        if checked == 'true':
            session['is_fast_delivery'] = True
        else:
            session['is_fast_delivery'] = False

        return HttpResponse(status=200)
