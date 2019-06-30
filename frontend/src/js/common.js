module.exports = function () {
    var icon_angle_down_parent = 'css-icon-angle-down-parent';
    var icon_angle_down = 'css-icon-angle-down';
    var icon_angle_up_parent = 'css-icon-angle-up-parent';
    var icon_angle_up = 'css-icon-angle-up';
    function changeAngleIcon(collapsible) {
        var field = $(collapsible).parent();
        var icon_parent = field.find('.js-icon-parent');
        var icon = field.find('.css-icon');

        var remove_parent = icon_parent.hasClass(icon_angle_down_parent) ? icon_angle_down_parent : icon_angle_up_parent;
        var add_parent = icon_parent.hasClass(icon_angle_down_parent) ? icon_angle_up_parent : icon_angle_down_parent;
        icon_parent.removeClass(remove_parent);
        icon_parent.addClass(add_parent);

        var remove_icon = icon.hasClass(icon_angle_down) ? icon_angle_down : icon_angle_up;
        var add_icon = icon.hasClass(icon_angle_down) ? icon_angle_up : icon_angle_down;
        icon.removeClass(remove_icon);
        icon.addClass(add_icon);
    }

    var collapsibles = $('.js-collapsible');
    collapsibles.on('show.bs.collapse', function () {
        changeAngleIcon(this);
    });

    collapsibles.on('hide.bs.collapse', function () {
        changeAngleIcon(this);
    });
};
