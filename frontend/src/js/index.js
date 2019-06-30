window.$ = require('jquery');
require('popper.js');
// require('bootstrap');
require('bootstrap/js/dist/alert');
require('bootstrap/js/dist/button');
require('bootstrap/js/dist/carousel');
require('bootstrap/js/dist/collapse');
require('bootstrap/js/dist/dropdown');
require('bootstrap/js/dist/util');
var imagesLoaded = require('imagesloaded');

imagesLoaded.makeJQueryPlugin(window.$);

var apps = [
    require('./zoom'),
    require('./common'),
    // require('./spinner'),
    require('./header'),
    require('./carousel'),
    require('./shop'),
    require('./card'),
    require('./origin'),
    require('./cart'),
    require('./order')
];

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

$(document).ready(function () {
    apps.forEach(function (app) {
        app();
    });
});
