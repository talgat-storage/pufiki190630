module.exports = function () {
    var html = $('html');
    var body = $('.js-body');
    var position = null;

    var filter = $('.js-shop-filter');
    $('.js-shop-filter-open-toggler').click(function () {
        position= $(window).scrollTop();
        html.addClass('overflow-hidden');
        body.addClass('overflow-hidden');
        filter.show(0);
    });
    $('.js-shop-filter-close-toggler').click(function () {
        body.removeClass('overflow-hidden');
        html.removeClass('overflow-hidden');
        if (position) {
            $(window).scrollTop(position);
        }
        filter.hide(0);
    });

    var unchecked_border_color = 'border-color-gray-300';
    var checked_border_color = 'border-color-2';
    $('.js-shop-filter-size-input').change(function () {
        var input = $(this);
        var label = input.parent().parent();

        if (input.is(':checked')) {
            label.removeClass(unchecked_border_color);
            label.addClass(checked_border_color);
        }
        else {
            label.removeClass(checked_border_color);
            label.addClass(unchecked_border_color);
        }
    });
};
