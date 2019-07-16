module.exports = function () {
    function changeActiveIndicator(wrapper, from_index, to_index) {
        var indicators = wrapper.find('.js-carousel-indicators').children();

        var active_indicator_class = 'css-carousel-indicator-active';
        $(indicators).removeClass(active_indicator_class);
        // $(indicators[from_index]).removeClass(active_indicator_class);
        $(indicators[to_index]).addClass(active_indicator_class);
    }

    function loadImage(wrapper, to_index) {
        // Set src from data-src
        var inner = wrapper.find('.carousel-inner');
        var item = $(inner.children()[to_index]);
        var source = item.find('source');
        var img = item.find('img');

        var source_src_attr = 'srcset';
        var source_data_src_attr = 'data-srcset';
        var img_src_attr = 'src';
        var img_data_src_attr = 'data-src';

        var source_url = null;
        if (source.length !== 0) {
            source_url = source.attr(source_data_src_attr);
        }
        var img_url = img.attr(img_data_src_attr);

        if (img_url) {
            // Hide controls
            var controls = wrapper.find('.js-carousel-control');
            controls.addClass('css-display-none');

            img.attr(img_src_attr, img_url);
            img.removeAttr(img_data_src_attr);

            if (source_url) {
                source.attr(source_src_attr, source_url);
                source.removeAttr(source_data_src_attr);
            }
        }
    }

    var carousel_wrapper = $('.js-carousel-wrapper');

    carousel_wrapper.on('slide.bs.carousel', '.carousel', function (e) {
        var carousel = $(this);
        var wrapper = $(e.target).closest('.js-carousel-wrapper');
        var from_index = e.from;
        var to_index = e.to;

        changeActiveIndicator(wrapper, from_index, to_index);
        loadImage(wrapper, to_index);

        // Save old width and height
        var width_css = 'width';
        var height_css = 'height';
        var parent = carousel.closest('.js-carousel-parent');
        parent.css(width_css, parent.width());
        parent.css(height_css, parent.height());

        carousel.on('slid.bs.carousel', function () {
            var inner = carousel.find('.carousel-inner');
            inner.imagesLoaded(function () {
                var controls = wrapper.find('.js-carousel-control');
                controls.removeClass('css-display-none');

                parent.css(width_css, '');
                parent.css(height_css, '');
            });
        });
    });

    carousel_wrapper.on('click', '.js-carousel-img-link', function () {
        var img = $(this);
        img.addClass('border border-color-gray-400 rounded css-border-thick');
    });
};
