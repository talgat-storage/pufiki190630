module.exports = function () {
    $('.js-cart-product-trash').click(function () {
        var trash = $(this);
        var product_slug = trash.attr('data-product-slug');

        var delete_form = $('.js-cart-delete-form');
        var delete_form_product_slug_input = delete_form.find('input[name="product_slug"]');
        delete_form_product_slug_input.val(product_slug);

        delete_form.submit();
    });

    $('.js-cart-is-fast-delivery-input').change(function () {
        var input = $(this);

        var next_state = input.attr('data-next-state');
        if (next_state === 'true') {
            input.prop('checked', true);
        }
        else if (next_state === 'false') {
            input.prop('checked', false);
        }
        else {
            return;
        }

        var delivery_price = $('.js-cart-delivery-price');
        delivery_price.html(next_state === 'true' ? '2900' : '0');

        var summary_total = $('.js-cart-summary-total');
        var total = parseInt(summary_total.attr('data-total'));
        summary_total.html(next_state === 'true' ? total + 2900 : total);

        $.post(api_cart_delivery, {
            'checked': next_state
        })
        .done(function() {
            input.attr('data-next-state', next_state === 'true' ? 'false': 'true');
        });
    });
};
