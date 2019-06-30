module.exports = function () {
    $('.js-origin-carousel-control').click(function () {
        var target = $(this);
        var wrapper = target.closest('.js-origin-carousel-wrapper');
        var carousel = wrapper.find('.carousel');

        // Save old width and height
        var carousel_parent = carousel.closest('.js-origin-carousel-parent');
        // wrapper.css('width', wrapper.width());
        // wrapper.css('height', wrapper.height());
        carousel_parent.css('width', carousel_parent.width());
        carousel_parent.css('height', carousel_parent.height());

        // Get direction
        var direction = target.attr('data-direction');

        // Get target carousel inner item
        var current_index = 0;
        var current_index_str = carousel.attr('data-current-index');
        if (current_index_str) {
            current_index = parseInt(current_index_str);
        }
        // var carousel_inner = carousel.find('.carousel-inner');
        var carousel_inner = carousel.find('.carousel-inner');
        var carousel_inner_items = carousel_inner.children();
        var number_of_carousel_inner_items = carousel_inner_items.length;
        var target_index = current_index;
        if (direction === 'next') {
            if (target_index === number_of_carousel_inner_items - 1) {
                target_index = 0;
            }
            else {
                target_index += 1;
            }
        }
        else if (direction === 'prev') {
            if (target_index === 0) {
                target_index = number_of_carousel_inner_items - 1;
            }
            else {
                target_index -= 1;
            }
        }
        var target_carousel_inner_item = $(carousel_inner_items[target_index]);

        // Load image
        var img = target_carousel_inner_item.find('img');
        var source = target_carousel_inner_item.find('source');
        if (source.length === 1) {
            var source_url = source.attr('data-srcset');
            if (source_url) {
                source.attr('srcset', source_url);
                source.removeAttr('data-srcset');
            }
        }
        if (img.length === 1) {
            var img_url = img.attr('data-src');
            if (img_url) {
                img.attr('src', img_url);
                img.removeAttr('data-src');
            }
        }

        // Load zoom image
        target_carousel_inner_item.zoom();

        // Change indicator
        var indicators = wrapper.find('.js-origin-carousel-indicators').children();
        // var prev_indicator = $(indicators[current_index]);
        var target_indicator = $(indicators[target_index]);

        $(indicators).removeClass('css-carousel-indicator-active');
        // prev_indicator.removeClass('css-carousel-indicator-active');
        target_indicator.addClass('css-carousel-indicator-active');

        // Roll carousel and change indicator once image is loaded
        target_carousel_inner_item.imagesLoaded(function () {
            carousel.attr('data-current-index', target_index);

            // wrapper.css('width', '');
            // wrapper.css('height', '');

            // Hide zoom
            var carousel_zoom = wrapper.find('.js-origin-carousel-zoom');
            carousel_zoom.hide(0);


            carousel.on('slid.bs.carousel', function () {
                // Show zoom
                carousel_zoom.show(0);

                // Unset old width and height
                carousel_parent.css('width', '');
                carousel_parent.css('height', '');
            });

            // Roll carousel
            carousel.carousel(target_index);
        });
    });

    var first_zoom = $('.js-origin-carousel-first-zoom');
    first_zoom.zoom();

    $('.js-cart-add-form').submit(function (e) {
        e.preventDefault();

        var form = $(this);

        // Disable button
        var button = form.find('.js-cart-add-button');
        var spinner = button.find('.js-spinner');
        spinner.removeClass('d-none');
        button.attr('disabled', 'disabled');
        button.attr('tabindex', -1);

        // Submit form
        var data = $(this).serialize();
        var url = $(this).attr("action");
        $.post(url, data).done(function (result) {
            setTimeout(function () {
                if ('alert' in result) {
                    // Show alert
                    var isMobile = true;
                    // var width = $(window).width();
                    // if (width > 768) {
                    //     isMobile = false;
                    // }

                    var alert_class = isMobile === true ? '.js-origin-cart-add-mobile-alert' : '.js-origin-cart-add-desktop-alert';
                    var alert = $('.js-body').find(alert_class);
                    alert.html(result['alert']);
                    alert.alert();
                }

                if ('cart_items_count' in result) {
                    var header_cart_items_count = $('.js-header-cart-items-count');
                    header_cart_items_count.html(result['cart_items_count']);
                }

                // Enable button
                button.removeAttr('tabindex');
                button.removeAttr('disabled');
                spinner.addClass('d-none');
            }, 500);
        });
    });
};
