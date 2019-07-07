module.exports = function () {
    var html = $('html');
    var body = $('.js-body');
    var position = null;

    var header = $('.js-header');

    header.find('.js-header-menu-open-toggler').click(function () {
        position= $(window).scrollTop();
        html.addClass('overflow-hidden');
        body.addClass('overflow-hidden');
        header.find('.js-header-menu').show(0);
    });

    header.find('.js-header-menu-close-toggler').click(function () {
        body.removeClass('overflow-hidden');
        html.removeClass('overflow-hidden');
        if (position) {
            $(window).scrollTop(position);
        }
        header.find('.js-header-menu').hide(0);
    });
};
