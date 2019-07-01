def cart_items_count(request):
    session = request.session

    count = 0
    if 'cart' in session:
        cart = session['cart']
        count = len(cart)

    context = dict()
    context['cart_items_count'] = count

    return context
