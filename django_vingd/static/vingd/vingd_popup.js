// Uses variables from global js context:
// var vingdFrontendURL = 'https://www.vingd.com';       # vingd home
// var vingdSiteURL = 'http://localhost:8000';           # consumer site url
// var vingdStaticURL = '/static/vingd/';                # consumer vingd specific static files
// var vingdVerifyURL = '/vgd/verify/';                  # consumer url for vingd verification

function vingdPopupPurchase(fn, success_callback, fail_callback, form, orderURL) {
    var params = {
        popupURL: knopso.buildURL(vingdSiteURL + vingdStaticURL + "popup.html", {href: orderURL}),
        frontendURL: vingdFrontendURL,
        siteURL: vingdSiteURL,
        onSuccess: function(hwnd, args) {
            fn && fn(success_callback, fail_callback, form, JSON.parse(args.token), args.context);
        }
    }
    var orderOpener = new knopso.popupOpener(params);
    return orderOpener();
}

function verify_callback(success_callback, fail_callback, form, args, context){
    args.context = context;
    var url = vingdVerifyURL;
    $.ajax({  
        type: "GET",
        url: url,
        dataType: "json",
        data: args,
        success: function(data) {
            if (data.ok) success_callback.call(form, data);
            else fail_callback.call(form, data);
        }
    });
}

(function($) {
    $.fn.vingd_popup = function(success_callback, fail_callback) {
        $(this).each(function() {
            $(this).submit(function(){
                var form = $(this);
                var action = form.attr("action");
                var data = form.serialize();
                var success = false; 
                var ajax_data;
                $.ajax({  
                    type: "POST",
                    async: false,
                    url: action,
                    data: data,
                    cache: false,
                    dataType: "json",  
                    success: function(data) {
                        ajax_data = data;
                        success = true;
                    }
                });
                if(success&&ajax_data.ok) {
                    if (ajax_data.vingd_url) {
                        vingdPopupPurchase(verify_callback, success_callback, fail_callback, form, ajax_data.vingd_url);
                    }
                    else {
                        success_callback.call(form, ajax_data);
                    }
                    return false;
                }
                if (fail_callback) fail_callback.call(form, ajax_data);
                return false;
            });
        });
        return this;
    }
})(jQuery);
