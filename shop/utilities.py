from .models import Product


def parse_cart(cart):
    success = False
    results = None
    total = None

    items = sorted(list(cart.items()))
    if items:
        product_slugs, quantities = map(list, zip(*items))
        products = \
            Product.objects.all() \
            .filter(origin__is_active=True, slug__in=product_slugs) \
            .select_related('origin') \
            .order_by('slug')
        origins = [product.origin for product in products]
        totals = [origin.price * quantity for origin, quantity in zip(origins, quantities)]
        results = zip(products, origins, quantities, totals)
        total = sum(totals)
        success = True

    return success, results, total
