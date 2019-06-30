module.exports = function () {
    var checked_border_color = 'border-color-2';

    $('.js-payment-method-input').change(function() {
        var inputs = $('.js-payment-method-input');
        inputs.each(function() {
            var input = $(this);
            var label = input.closest('label');

            if (input.prop('checked')) {
                label.addClass(checked_border_color);
            }
            else {
                label.removeClass(checked_border_color);
            }
        });
    });
};
