
'use strict';


var oWidth;
function change() {
    if (oWidth < 768) {
        $('.navbar-nav>li>a').click(function (e) {
            // console.log($(this).next('.submenu')[0]);
            e.preventDefault();
            if(typeof($(this).next('.submenu')[0]) != 'undefined') {
                e.preventDefault();
                $(this).next('.submenu').toggle();
            }
        });

        $('.navbar-nav>li>ul li>a').click(function (e) {
            // console.log($(this).next('.childmenu')[0]);
            // e.preventDefault();
            if(typeof($(this).next('.childmenu')[0]) != 'undefined') {
                e.preventDefault();
                $(this).next('.childmenu').toggle();
            }
        });

        // $('.submenu>li').click(function (e) {
        //     console.log($(this).next('ul')[0]);
        //     e.preventDefault();
        //     if(typeof($(this).next('ul')[0]) != 'undefined') {
        //         e.preventDefault();
        //         $(this).next('ul').toggle();
        //     }
        // })
    } else {
        $('.navbar-nav>li').hover(function () {
            $(this).find('.submenu').show();
        }, function () {
            $(this).find('.submenu').hide();
        });

        var showChild = function () {
            $(this).children('ul').show();
            $(this).siblings().children('ul').hide();
        };

        var hideChild = function () {
            $(this).find('ul').hide();
        };

        $('.submenu>li').hover(showChild, hideChild);

        $('.childmenu>li').hover(showChild, hideChild);
    }
}
$(function () {
    oWidth = document.body.clientWidth;
    change();
});

