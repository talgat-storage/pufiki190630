module.exports = function () {
    $('.js-card-more-colors').click(function () {
        var target = $(this);
        var hidden_color_boxes = target.parent().find('.js-card-color.d-none');
        hidden_color_boxes.addClass('d-inline-block');
        target.addClass('d-none');
        hidden_color_boxes.removeClass('d-none');
        target.removeClass('d-inline-flex');
    });

    $('.js-card-color').click(function () {
        var target = $(this);
        var product_slug = target.attr('data-product-slug');
        var product_color = target.attr('data-product-color');
        
        // Select color icon and unselect others
        var prev_selected_color_icons = target.parent().find('.css-icon.border-color-2');
        prev_selected_color_icons.removeClass('border-color-2').addClass('border-color-gray-300');
        var current_selected_color_icon = target.find('.css-icon');
        current_selected_color_icon.removeClass('border-color-gray-300').addClass('border-color-2');

        var wrapper = target.parent().parent().find('.js-carousel-wrapper');

        // Save old
        var previous_product_slug = wrapper.attr('data-product-slug');
        carousels[previous_product_slug] = wrapper.html();

        // Set old height
        wrapper.css('height', wrapper.height());
        wrapper.empty();

        // Set new product slug
        wrapper.attr('data-product-slug', product_slug);

        // Set new product link
        var product_link = target.parent().parent().find('.js-card-product-link');
        var origin_url = product_link.attr('data-origin-url');
        product_link.attr('href', origin_url + '?color=' + product_color);

        // Get new if exists
        if (product_slug in carousels) {
            wrapper.html(carousels[product_slug]);
            var carousel = wrapper.find('.carousel');
            carousel.carousel();
            wrapper.imagesLoaded(function () {
                // Unset old height
                wrapper.css('height', '');
            });
        }
        // Load new
        else {
            $.ajax({
                url: api_shop_card_carousel_url + '?' + $.param({
                    'product_slug': product_slug
                }),
                success: function (new_content) {
                    wrapper.html(new_content);
                    var carousel = wrapper.find('.carousel');
                    carousel.carousel();

                    wrapper.imagesLoaded(function () {
                        // Unset old height
                        wrapper.css('height', '');

                        var controls = wrapper.find('.js-carousel-control');
                        controls.removeClass('css-display-none');
                    });
                }
            });
        }
    });
};
