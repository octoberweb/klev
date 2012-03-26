# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from apps.orders.views import *


urlpatterns = patterns('',

    (r'^cart/$',view_cart),

    (r'^add_product_to_cart/$',add_product_to_cart),
    (r'^delete_product_from_cart/$',delete_product_from_cart),

)

'''
    (r'^add_to_cart_personal_photo/$',add_to_cart_personal_photo),
    (r'^get_photo_total/$',get_photo_total),
    (r'^add_to_cart_stock_photo/$',add_to_cart_stock_photo),

    (r'^get_total_photo_from_cart/$',get_total_photo_from_cart),
    (r'^update_cart/$',update_cart),

    (r'^add_to_cart_collage_personal/$',add_to_cart_collage_personal),

    (r'^get_cart_total_summary/$',get_cart_total_summary),

    (r'^edit_cart_collage_personal/$',edit_cart_collage_personal),

    (r'^update_cart_collage_personal/$',update_cart_collage_personal),

    (r'^delete_photo_from_cart/$',delete_photo_from_cart),


    (r'^order/confirmed/$',order_confirmed),
    (r'^order/$',view_cart),

    (r'^confirm_order/$',confirm_order),

    (r'^get_order_rules/$',get_order_rules),


'''