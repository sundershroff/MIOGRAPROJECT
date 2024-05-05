"""
URL configuration for MIOGRA project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include,re_path
from django.conf import settings
from django.conf.urls.static import static
from api import business_views
from api import end_user_views,delivery_views
from web import end_usersview
from mio_admin import views
urlpatterns = [
    path('', include('mio_admin.urls')),
    path('', include('web.urls')),
    path('admin/', admin.site.urls),

    path('business_signup/',business_views.business_signup),
    path('business_otp/',business_views.business_otp),
    path('business_signin/',business_views.business_signin),
    path('my_accounts_data/<id>',business_views.my_accounts_data),
    path('forget_password/',business_views.forget_password),
    path('resend_otp/<id>',business_views.resend_otp),
    path('business_profile_picture/<id>',business_views.business_profile_picture),
    path('business_profile_update/<id>',business_views.business_profile_update),
    path('get_quickproduct_order/<id>/',business_views.get_quickproduct_order),
    path('get_normalproduct_order/<id>/',business_views.get_normalproduct_order),
    path('get_allproducts_order/<id>/<str:prostatus>/',business_views.get_allproducts_order),
    path('business_status_pickedUp/<order_id>',business_views.business_status_pickedUp),
    path('business_order_dispatch/<order_id>',business_views.business_order_dispatch),
    path('product_status_golivePause/<id>/<str:business_status>/',business_views.product_status_golivePause),
    path('businessnotify_status_true/<id>',business_views.businessnotify_status_true),
    path('business_notify_status_false/<id>',business_views.business_notify_status_false),
    path('get_notification_data/<id>/',business_views.get_notification_data),
    path('single_notify_delete/<id>/',business_views.single_notify_delete),
    path('business_delete_all_notification/<id>/',business_views.business_delete_all_notification),

# shopping
    path('shopping/<id>',business_views.shopping),
    path('shopping_alldata',business_views.shopping_alldata),
    path('my_shopping_data/<id>',business_views.my_shopping_data),
    path('shopping_update/<id>/shops/<shop_id>',business_views.shopping_update),
    path('business_shopping_data/<id>',business_views.business_shopping_data),
    # shopping dashboard
    path('shop_total_revenue/<id>',business_views.shop_total_revenue),
    path('shop_mon_revenue/<id>',business_views.shop_mon_revenue),
    path('shop_orderstatus/<id>',business_views.shop_orderstatus),
    path('update_product_order_status_reject/<id>/<product_id>/<order_id>/',business_views.update_product_order_status_reject),
    path('update_product_order_status_accept/<id>/<product_id>/<order_id>/',business_views.update_product_order_status_accept),
    
    # shop_product 


    path('shop_products/<id>',business_views.shop_products),
    path('shop_product_save/<id>',business_views.shop_product_save),
    path('shop_get_products/<id>',business_views.shop_get_products),
    path('shop_get_my_product/<id>/product/<product_id>',business_views.shop_get_my_product),
    path('shop_delete_product/<id>/product/<product_id>',business_views.shop_delete_product),
    path('shop_update_product/<id>/product/<product_id>',business_views.shop_update_product),
    path('shop_imgupdate_product/<id>/<product_id>/<index_value>',business_views.shop_imgupdate_product),
    path('shop_productorder_date/<id>',business_views.shop_productorder_date),
    path('shop_get_subcategoryproducts/<id>/<str:subcategory>/',business_views.shop_get_subcategoryproducts),
    path('dashboardproduct_count/<id>/',business_views.dashboardproduct_count),

# jewellery
    path('jewellery/<id>',business_views.jewellery),
    path('jewellery_alldata',business_views.jewellery_alldata),
    path('my_jewellery_data/<id>',business_views. my_jewellery_data),
    path('jewellery_update/<id>/jewels/<jewel_id>',business_views.jewellery_update),
    path('business_jewellery_data/<id>',business_views.business_jewellery_data),
    # dashboard
    path('jewel_total_revenue/<id>',business_views.jewel_total_revenue),
    path('jewel_mon_revenue/<id>',business_views.jewel_mon_revenue),
    path('jewel_orderstatus/<id>',business_views.jewel_orderstatus),
    # jewellery_product gold

    path('jewel_products/<id>',business_views.jewel_products),
    path('jewel_product_save/<id>',business_views.jewel_product_save),
    path('jewel_get_products/<id>',business_views.jewel_get_products),
    path('jewel_get_my_product/<id>/product/<product_id>',business_views.jewel_get_my_product),
    path('jewel_delete_product/<id>/product/<product_id>',business_views.jewel_delete_product),
    path('jewel_update_product/<id>/product/<product_id>',business_views.jewel_update_product),
    path('jewel_imgupdate_product/<id>/<product_id>/<index_value>',business_views.jewel_imgupdate_product),
    path('jewel_productorder_date/<id>',business_views.jewel_productorder_date),
    path('jewel_get_subcategoryproducts/<id>/<str:subcategory>/',business_views.jewel_get_subcategoryproducts),
    
# food
    path('food/<id>',business_views.food),
    path('food_alldata',business_views.food_alldata), 
    path('my_food_data/<id>',business_views. my_food_data),
    path('food_update/<id>/foods/<food_id>',business_views.food_update),
    path('business_food_data/<id>',business_views.business_food_data),
    # dashboard
    path('food_total_revenue/<id>',business_views.food_total_revenue),
    path('food_mon_revenue/<id>',business_views.food_mon_revenue),
    path('food_orderstatus/<id>',business_views.food_orderstatus),
    # food_product 
    path('food_add_products/<id>',business_views.food_products),
    path('food_product_save/<id>',business_views.food_product_save),
    path('food_get_products/<id>',business_views.food_get_products),
    path('food_get_my_product/<id>/product/<product_id>',business_views.food_get_my_product),
    path('food_delete_product/<id>/product/<product_id>',business_views.food_delete_product),
    path('food_update_product/<id>/product/<product_id>',business_views.food_update_product),
    path('food_imgupdate_product/<id>/<product_id>/<index_value>',business_views.food_imgupdate_product),
    path('food_productorder_date/<id>',business_views.food_productorder_date),
    path('food_get_subcategoryproducts/<id>/<str:subcategory>/',business_views.food_get_subcategoryproducts),
    path('restautant/review/<id>',business_views.add_review_restaurant),
# freshcuts
    path('freshcuts/<id>',business_views.freshcuts),
    path('freshcuts_alldata',business_views.freshcuts_alldata),
    path('my_freshcuts_data/<id>',business_views. my_freshcuts_data),
    path('freshcuts_update/<id>/freshcuts/<fresh_id>',business_views.freshcuts_update),
    path('business_freshcuts_data/<id>',business_views.business_freshcuts_data),
    # dashboard
    path('fresh_total_revenue/<id>',business_views.fresh_total_revenue),
    path('fresh_mon_revenue/<id>',business_views.fresh_mon_revenue),
    path('fresh_orderstatus/<id>',business_views.fresh_orderstatus),
    # fresh_product 
    path('fresh_products/<id>',business_views.fresh_products),
    path('fresh_product_save/<id>',business_views.fresh_product_save),
    path('fresh_get_products/<id>',business_views.fresh_get_products),
    path('fresh_get_my_product/<id>/product/<product_id>',business_views.fresh_get_my_product),
    path('fresh_delete_product/<id>/product/<product_id>',business_views.fresh_delete_product),
    path('fresh_update_product/<id>/product/<product_id>',business_views.fresh_update_product),
    path('fresh_imgupdate_product/<id>/<product_id>/<index_value>',business_views.fresh_imgupdate_product),
    path('fresh_productorder_date/<id>',business_views.fresh_productorder_date),
    path('fresh_get_subcategoryproducts/<id>/<str:subcategory>/',business_views.fresh_get_subcategoryproducts),
# dailymio
    path('dailymio/<id>',business_views.dailymio),
    path('dailymio_alldata',business_views.dailymio_alldata),
    path('my_dailymio_data/<id>',business_views. my_dailymio_data),
    path('dailymio_update/<id>/dailymio/<dmio_id>',business_views.dailymio_update),
    path('business_dailymio_data/<id>',business_views.business_dailymio_data),

    # dashboard
    path('dmio_total_revenue/<id>',business_views.dmio_total_revenue),
    path('dmio_mon_revenue/<id>',business_views.dmio_mon_revenue),
    path('dmio_orderstatus/<id>',business_views.dmio_orderstatus),
    # dailymio_products
    path('dmio_products/<id>',business_views.dmio_products),
    path('dmio_product_save/<id>',business_views.dmio_product_save),
    path('dmio_get_products/<id>',business_views.dmio_get_products),
    path('dmio_get_my_product/<id>/product/<product_id>',business_views.dmio_get_my_product),
    path('dmio_delete_product/<id>/product/<product_id>',business_views.dmio_delete_product),
    path('dmio_update_product/<id>/product/<product_id>',business_views.dmio_update_product),
    path('dmio_imgupdate_product/<id>/<product_id>/<index_value>',business_views.dmio_imgupdate_product),
    path('dmio_productorder_date/<id>',business_views.dmio_productorder_date),
    path('dmio_get_subcategoryproducts/<id>/<str:subcategory>/',business_views.dmio_get_subcategoryproducts),
# pharmacy
    path('pharmacy/<id>',business_views.pharmacy),
    path('pharmacy_alldata',business_views.pharmacy_alldata),
    path('my_pharmacy_data/<id>',business_views.my_pharmacy_data),
    path('pharmacy_update/<id>/pharmacy/<pharm_id>',business_views.pharmacy_update),
    path('business_pharmacy_data/<id>',business_views.business_pharmacy_data),
    # dashboard
    path('pharmacy_total_revenue/<id>',business_views.pharmacy_total_revenue),
    path('pharm_mon_revenue/<id>',business_views.pharm_mon_revenue),
    path('pharm_orderstatus/<id>',business_views.pharm_orderstatus),
    # pharmacy_ products 
    path('pharmacy_products/<id>',business_views.pharmacy_products),
    path('pharmacy_product_save/<id>',business_views.pharmacy_product_save),
    path('pharmacy_get_products/<id>',business_views.pharmacy_get_products),
    path('pharmacy_get_my_product/<id>/product/<product_id>',business_views.pharmacy_get_my_product),
    path('pharmacy_delete_product/<id>/product/<product_id>',business_views.pharmacy_delete_product),
    path('pharmacy_update_product/<id>/product/<product_id>',business_views.pharmacy_update_product),
    path('pharm_imgupdate_product/<id>/<product_id>/<index_value>',business_views.pharm_imgupdate_product),
    path('pharmacy_productorder_date/<id>',business_views.pharmacy_productorder_date),
    path('pharmacy_get_subcategoryproducts/<id>/<str:subcategory>/',business_views.pharmacy_get_subcategoryproducts),
# d_original
    path('d_original/<id>',business_views.d_original),
    path('d_original_alldata',business_views.d_original_alldata),
    path('my_d_original_data/<id>',business_views.my_d_original_data),
    path('d_original_update/<id>/d_original/<d_id>',business_views.d_original_update),
    path('business_d_original_data/<id>',business_views.business_d_original_data),
    # dashboard links
    path('d_origin_total_revenue/<id>',business_views.d_origin_total_revenue),
    path('d_origin_mon_revenue/<id>',business_views.d_origin_mon_revenue),
    path('d_origin_orderstatus/<id>',business_views.d_origin_orderstatus),
    # d_original_get_products
    path('d_original_products/<id>',business_views.d_original_products),
    path('d_original_product_save/<id>',business_views.d_original_product_save),
    path('d_original_get_products/<id>',business_views.d_original_get_products),
    path('d_original_get_district_products/<id>/<str:district>/',business_views.d_original_get_district_products),
    path('d_original_get_my_product/<id>/product/<product_id>',business_views.d_original_get_my_product),
    path('d_original_delete_product/<id>/product/<product_id>',business_views.d_original_delete_product),
    path('d_original_update_product/<id>/product/<product_id>',business_views.d_original_update_product),
    path('d_original_imgupdate_product/<id>/<product_id>/<index_value>',business_views.d_original_imgupdate_product),
    path('d_original_productorder_date/<id>',business_views.d_original_productorder_date),
    path('d_original_get_subcategoryproducts/<id>/<str:subcategory>/',business_views.d_original_get_subcategoryproducts),
    path('d_original_district_based_product/<str:district>/',business_views.dorigin_district_products_only),


# ..............end_user........

    path('end_user_signup/',end_user_views.end_user_signup),
    path('end_user_signin/',end_user_views.end_user_signin),
    path('all_users_data/',end_user_views.all_users_data),
    path('end_user_otp/<id>',end_user_views.end_user_otp),
    path('endresend_otp/<id>',end_user_views.endresend_otp),
    path('endforget_password/',end_user_views.endforget_password),
    path('end_profile_picture/<id>',end_user_views.end_profile_picture),
    path('enduser_profile_update/<id>',end_user_views.enduser_profile_update),
    path('end_user_address/<id>',end_user_views.end_user_address),
    path('update_end_user_address/<id>/',end_user_views.update_end_user_address),
    path('single_users_data/<id>',end_user_views.single_users_data),
    path('locationupdate/<id>',end_user_views.locationupdate),
    path('user_product_order_status_return/<id>/<order_id>/',end_user_views.user_product_order_status_return),


    # before login
    path('all_shopproducts/',end_user_views.all_shopproducts),
    path('category_based_shop/<str:subcategory>/',end_user_views.category_based_shop),
    path('get_single_shopproduct/<id>/<product_id>',end_user_views.get_single_shopproduct),
    # after login
    path('user_get_all_shopproducts/<id>/<user_id>',end_user_views.user_get_all_shopproducts),
    path('user_get_category_shop/<id>/<user_id>/<str:subcategory>/',end_user_views.user_get_category_shop),
    path('user_get_single_shopproduct/<id>/<user_id>/<product_id>',end_user_views.user_get_single_shopproduct),
    # before login
    path('all_jewelproducts/',end_user_views.all_jewelproducts),
    path('category_based_jewel/<str:subcategory>/',end_user_views.category_based_jewel),
    path('single_jewelproduct/<id>/<product_id>',end_user_views.get_single_jewelproduct),
    # after login
    path('user_get_all_jewelproducts/<id>/<user_id>',end_user_views.user_get_all_jewelproducts),
    path('user_get_category_jewel/<id>/<user_id>/<str:subcategory>/',end_user_views.user_get_category_jewel),
    path('user_get_single_jewelproduct/<id>/<user_id>/<product_id>',end_user_views.user_get_single_jewelproduct),
    # before login
    path('all_foodproducts/',end_user_views.all_foodproducts),
    path('category_based_food/<str:subcategory>/',end_user_views.category_based_food),
    path('single_foodproduct/<id>/<product_id>',end_user_views.get_single_foodproduct),
    #after login
    path('user_get_all_foodproducts/<id>/<user_id>',end_user_views.user_get_all_foodproducts),
    path('user_get_category_food/<id>/<user_id>/<str:subcategory>/',end_user_views.user_get_category_food),
    path('user_get_single_foodproduct/<id>/<user_id>/<product_id>',end_user_views.user_get_single_foodproduct),
    #before login
    path('all_freshcutproducts/',end_user_views.all_freshcutproducts),
    path('category_based_fresh/<str:subcategory>/',end_user_views.category_based_fresh),
    path('single_freshproduct/<id>/<product_id>',end_user_views.get_single_freshproduct),
    # after login
    path('user_get_all_freshproducts/<id>/<user_id>',end_user_views.user_get_all_freshproducts),
    path('user_get_category_fresh/<id>/<user_id>/<str:subcategory>/',end_user_views.user_get_category_fresh),
    path('user_get_single_freshproduct/<id>/<user_id>/<product_id>',end_user_views.user_get_single_freshproduct),
    # beforelogin
    path('all_dmioproducts/',end_user_views.all_dmioproducts),
    path('category_based_dmio/<str:subcategory>/',end_user_views.category_based_dmio),
    path('get_single_dmio_product/<id>/<product_id>',end_user_views.get_single_dmioproduct),
    # afterlogin
    path('user_get_all_dmioproducts/<id>/<user_id>',end_user_views.user_get_all_dmioproducts),
    path('user_get_category_d_original/<id>/<user_id>/<str:subcategory>/',end_user_views.user_get_category_d_original),
    path('user_get_single_d_originalproduct/<id>/<user_id>/<product_id>',end_user_views.user_get_single_d_originalproduct),
    # beforelogin
    path('all_pharmproducts/',end_user_views.all_pharmproducts),
    path('category_based_pharm/<str:subcategory>/',end_user_views.category_based_pharm),
    path('single_pharmproduct/<id>/<product_id>',end_user_views.get_single_pharmproduct),
    # afterlogin
    path('user_get_all_pharmproducts/<id>/<user_id>',end_user_views.user_get_all_pharmproducts),
    path('user_get_category_pharm/<id>/<user_id>/<str:subcategory>/',end_user_views.user_get_category_pharm),
    path('user_get_single_pharmproduct/<id>/<user_id>/<product_id>',end_user_views.user_get_single_pharmproduct),
    # beforelogin
    path('all_d_originalproducts/',end_user_views.all_d_originalproducts),
    path('category_based_d_original/<str:subcategory>/',end_user_views.category_based_d_original),
    path('single_d_originalproduct/<id>/<product_id>',end_user_views.get_single_d_originalproduct),
    path('d_original_district_products/<id>/<str:district>/',end_user_views.d_original_district_products),
    # afterlogin
    path('user_get_all_d_originalproducts/<id>/<user_id>',end_user_views.user_get_all_d_originalproducts),
    path('user_get_category_d_original/<id>/<user_id>/<str:subcategory>/',end_user_views.user_get_category_d_original),
    path('user_get_single_d_originalproduct/<id>/<user_id>/<product_id>',end_user_views.user_get_single_d_originalproduct),
    path('user_d_original_district_products/<id>/<user_id>/<str:district>/',end_user_views.user_d_original_district_products),

    # orderproducts
    
    path('enduser_order_create/<id>/<product_id>/<str:category>/',end_user_views.enduser_order_create),
    path('enduser_order_cancel/<id>/<order_id>',end_user_views.enduser_order_cancel),
    path('enduser_order_list/<id>/',end_user_views.enduser_order_list),
    path('enduser_single_order_list/<id>/<order_id>',end_user_views.enduser_single_order_list),


    # cart products
    path('cart_product/<id>/<product_id>/<str:category>/',end_user_views.cart_product),
    path('cartlist/<id>',end_user_views.cartlist),
    path('cartremove/<id>/<cart_id>/',end_user_views.cartremove),
    path('cartupdate/<id>',end_user_views.cartupdate),
    path('create_reviews_for_delivered_products/<id>/<product_id>/',end_user_views.create_reviews_for_delivered_products),
    path('get_all_reviews/',end_user_views.get_all_reviews),
    path('get_product_all_reviews/<product_id>',end_user_views.get_product_all_reviews),
    path('calculate_average_ratings/<str:category>',end_user_views.calculate_average_ratings),

    # whishlist
    path('whishlist_product/<id>/<product_id>/<str:category>/',end_user_views.whishlist_product),
    path('all_wishlist/<id>',end_user_views.all_wishlist),
    path('remove_wish/<id>/<product_id>/',end_user_views.remove_wish),

    # timeline
    path('user_product_timeline/<id>',end_user_views.user_product_timeline),


# usedproducts
    path('used_products/<id>',end_user_views.used_products),
    path('get_allused_products/',end_user_views.get_allused_products),
    path('get_used_products/<id>',end_user_views.get_used_products),
    path('get_single_used_products/<product_id>',end_user_views.get_single_used_products),
    path('get_used_products_category/<str:subcategory>/',end_user_views.get_used_products_category),
    path('user_single_used_products/<id>/<product_id>',end_user_views.user_single_used_products),
    path('used_update_product/<id>/<product_id>',end_user_views.used_update_product),


# # ..............enduser_web................


# .........................delivery...........................

    path('delivery_person_signup/<id>',delivery_views.delivery_person_signup),
    # path('delivery_person_signin/',delivery_views.delivery_person_signin),
    path('all_delivery_person_data/',delivery_views.all_delivery_person_data),
    path('single_delivery_person_data/<id>',delivery_views.single_delivery_person_data),
    path('delivery_person_update/<id>',delivery_views.delivery_person_update),
    # path('delivery_get_Normalproduct_order/<id>/<str:region>/',delivery_views.delivery_get_Normalproduct_order),
    path('delivery_get_product_order/<id>/<str:region>/',delivery_views.delivery_get_product_order),


    path('delivery_yourissue/<id>/',delivery_views.delivery_yourissue),
    path('delivery_login_table/<id>',delivery_views.delivery_login_table),
    path('delivery_send_otp/',delivery_views.delivery_send_otp),
    path('delivery_verify_otp/',delivery_views.delivery_verify_otp),

    path('product_status_delivered/<id>/<order_id>',delivery_views.product_status_delivered),
    path('delivery_product_order_status_accept/<id>/<product_id>/<order_id>/',delivery_views.delivery_product_order_status_accept),

    path('delivery_product_order_status_reject/<id>/<product_id>/<order_id>/',delivery_views.delivery_product_order_status_reject),
    path('delivery_produt_emergency/<id>/<order_id>',delivery_views.delivery_produt_emergency),
    path('delivery_signin_otp/<id>/',delivery_views.delivery_signin_otp),
    path('product_status/<id>/<order_id>/<str:orderstatus>/',delivery_views.product_status),
    path('delivered_productorder_date/<id>',delivery_views.delivered_productorder_date),
    path('todays_order/<id>/<str:delivery_date>',delivery_views.todays_order),
    path('todays_incencentiveorder/<id>/<str:delivery_date>',delivery_views.todays_incencentiveorder),
    path('delivery_payableamount/<id>',delivery_views.delivery_payableamount),
    path('delivery_withdraw_status/<id>',delivery_views.delivery_withdraw_status),
    path('deliverynotify_status_true/<id>',delivery_views.deliverynotify_status_true),
    path('delivery_notify_status_false/<id>',delivery_views.delivery_notify_status_false),
    path('delivery_floating_cash/<id>',delivery_views.delivery_floating_cash),
    path('delivery_floating_status/<id>',delivery_views.delivery_floating_status),


# notification
    path('delivery_notification/',delivery_views.delivery_notification),
    path('notification_data/<id>/',delivery_views.notification_data),
    path('delivery_person_notify_delete/<id>/',delivery_views.delivery_person_notify_delete),
    path('delete_all_notification/<id>/',delivery_views.delete_all_notification),




]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

