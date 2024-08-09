from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from api import business_views
from api import end_user_views,delivery_views
from web import end_usersview
from django.urls import path, include
from mio_admin import views
urlpatterns = [

# ..............enduser_web................
    path('enduser/usersignup',end_usersview.usersignup),
    path('enduser/usersignin',end_usersview.usersignin),
    path('enduser/logout/<id>',end_usersview.signout_view),
    path('enduser/end_user_otp/<id>',end_usersview.otp),
    path('enduser/profile_picture/<id>',end_usersview.profile_picture),
    path('enduser/dashboard/<id>',end_usersview.dashboard),

    path("shopproducts/shop/",end_usersview.shop), 
    path("shopproducts/shop_products/<str:category>",end_usersview.shop_products),
    path("shopproducts/shop_based/",end_usersview.shop_based_product),
    path("shopproducts/single_products/<id>/<product_id>",end_usersview.single_shopproducts),
    path("products/shopproducts/shop/<id>",end_usersview.dashboard),
    path('products/shopproduct_categorywise/<id>/<str:category>/',end_usersview.shopproduct_category),
    path('products/shops_based_product/<id>/<shop_id>/',end_usersview.user_shopbased_products),
    path('products/singleproduct/enduser/<id>/<shop_id>/<product_id>',end_usersview.user_single_products),
    
    path("",end_usersview.food),
    path('food_products/<str:category>',end_usersview.food_products),
    path('food_products/Shop_based/<id>',end_usersview.restaurant_based_products),
    path('food_products/single_food/<id>/<product_id>/',end_usersview.single_food_products),
    path("products/foodproducts/food/<id>",end_usersview.user_foodpage),
    path('products/food_products_category/<id>/<str:category>',end_usersview.food_products_category),
    path('products/food_restaurant/<id>/<food_id>/',end_usersview.user_restaurant_products), 
    path('products/food_products/single_food/<id>/<shop_id>/<product_id>/',end_usersview.user_singlefood_products),

    path("freshproducts/fresh_cuts",end_usersview.fresh_cuts),
    path("freshproducts/fresh_cuts/category/<str:category>/",end_usersview.fresh_cut_products),
    path("freshproducts/shop_based/<id>/",end_usersview.freshShop_based_products),
    path("freshproducts/fresh_single_product/<id>/<product_id>",end_usersview.fresh_cut_singel_products),
    path("products/freshproducts/fresh_cuts/<id>",end_usersview.user_fresh_cuts),
    path("products/freshproducts/fresh_cuts_category/<id>/<str:category>/",end_usersview.user_freshcut_products),
    path("products/fresh_cuts/shops_products/<id>/<fresh_id>/",end_usersview.user_freshcut_shop_products),
    path("products/freshproducts/single_product/<id>/<shop_id>/<product_id>",end_usersview.user_freshcut_single_products),

    path("doriginalproducts/doriginal",end_usersview.doriginal),
    path("doriginalproducts/district_based/<str:district>/",end_usersview.dorigin_district_based_products),
    path("doriginalproducts/doriginal/<d_id>/<product_id>",end_usersview.d_original_single_products),
    path("products/doriginalproducts/doriginal/<id>",end_usersview.user_doriginal),
    path("products/doriginal/district/<id>/<str:district>/",end_usersview.user_dorigin_district),
    path("products/doriginalproducts/doriginal/<id>/<shop_id>/<product_id>",end_usersview.user_doriginal_single_products),

    path("dailymioproducts/daily_mio",end_usersview.daily_mio),
    path("dailymioproducts/daily_mio/category/<str:category>/",end_usersview.daily_mio_products),
    path("dailymioproducts/shop_products/<id>/",end_usersview.dmioshop_based_products),
    path("dailymioproducts/dmio_singleproduct/<id>/<product_id>",end_usersview.daily_mio_single_products),
    path("products/dailymioproducts/daily_mio/<id>",end_usersview.user_daily_mio),
    path("products/dailymioproducts/daily_mio/<id>/<str:category>/",end_usersview.user_dmio_products),
    path("products/dailymio/shops/<id>/<dmio_id>/",end_usersview.user_dmioshops_products),
    path("products/dailymioproducts/dmio_singleproduct/<id>/<shop_id>/<product_id>",end_usersview.user_dailymio_single_products),

    path("jewelleryproducts/jewellery/",end_usersview.jewellery),
    path("jewelleryproducts/jewellery/<str:category>",end_usersview.jewellery_products),
    path("jewelleryproducts/shop_products/<id>",end_usersview.jewelshop_based_products),
    path("jewelleryproducts/jewellery/<id>/<product_id>",end_usersview.jewellery_single_products),
    path("products/jewelleryproducts/jewellery/<id>",end_usersview.user_jewellery),
    path("products/jewelleryproducts/jewellery/<id>/<str:category>",end_usersview.user_jewellery_products),
    path("products/jewellery/shops/<id>/<jewel_id>",end_usersview.user_jewellery_based_products),
    path("products/jewelleryproducts/jewellery/<id>/<shop_id>/<product_id>",end_usersview.user_jewel_single_product),

    path("pharmacyproducts/pharmacy/",end_usersview.pharmacy),
    path("pharmacyproducts/pharmacy/<str:category>",end_usersview.pharmac_products),
    path("pharmacyproducts/shop_products/<id>",end_usersview.medicalshop_products),
    path("pharmacyproducts/pharmacy_single/<id>/<product_id>",end_usersview.pharmac_single_products),
    path("products/pharmacyproducts/pharmacy/<id>",end_usersview.user_pharmacy),
    path("products/pharmacyproducts/pharmacy/<id>/<str:category>",end_usersview.user_pharm_products),
    path("products/pharmacy/shopbased/<id>/<pharm_id>",end_usersview.user_medical_pharmacy_product),
    path("products/pharmacyproducts/pharmacy_single/<id>/<shop_id>/<product_id>",end_usersview.user_pharmac_singleproduct),
    
    path('usedproducts/products/',end_usersview.used_product),
    path('usedproducts/products_with_category/<str:subcategory>',end_usersview.used_product_category),
    path('usedproducts/single_product/<product_id>',end_usersview.usedproduct_single_data),
    path('enduser/used_products/products/<id>',end_usersview.used_product_index),
    path('enduser/used_products/categorybased/<id>/<str:subcategory>',end_usersview.used_category_based),
    path('enduser/used_products/single_data/<id>/<product_id>',end_usersview.used_single_product),
    path('enduser/usedproduct/registration/<id>/',end_usersview.user_usedproduct_reg),
    
    path('search_view/', end_usersview.search_view, name='search_view'),
    # -----------------address change--------------------
    path('user/update_address/<id>',end_usersview. user_add_address_cart),
    path('user/addess_edit/<id>/<change>',end_usersview.user_address_cartchange),
   
    
    path('user_update_address/<id>',end_usersview. user_add_address_foodcart),
    path('user_addess_edit/<id>/<change>',end_usersview.user_address_foodchange),
    
    path('user/orders/<id>/<str:category>/products/<shop_id>/<product_id>/',end_usersview.user_checkout_page,name="checkout"),
    path('user_order_product_list/<id>',end_usersview.user_order_data),
    path('user/product/order/tracking/<id>/<order_id>',end_usersview.tracking_order),
    path('user_payment/<id>/option/<str:category>/<shop_id>/product/<product_id>/with/<qty>/<d_a>',end_usersview.user_payment_option,name="payment"),
    # --------------------cart-------------------------
    path('user/shopping_add_to_cart/<id>/<str:category>/products/<shop_id>/<product_id>/',end_usersview.add_to_cart),
    path('user/shopping_cart_products/<id>/',end_usersview.user_shopping_cart),
    path('user_cart_to_checkout/<id>',end_usersview.cart_to_checkout,name="cart_checkout"),
    path('user_cart_payment/<id>/<add>',end_usersview.user_cart_payment,name="cart_payment"),
    
    # ------------food cart-----------------------
    path('user/food_cart/<id>/',end_usersview.user_food_cart),
    path('user/food_cart/checkout/<id>',end_usersview.foods_cart_checkout),
    path('user/foodcart/payment/<id>/<add1>',end_usersview.user_foods_cart_payment),

    # ------------wishlist--------------------------
    path('user/shopping_add_to_wishlist/<id>/products/<str:category>/<product_id>/',end_usersview.add_to_wishlist),
    path('user/shopping_wishlist_products/<id>/',end_usersview.user_wish_list_data),
    
    # ------------RETURN--------------------------
    path('product_order_status_return/<id>/<order_id>/',end_usersview.user_product_return),

    # -------------------- Checking web--------------------------
    path('success_page/<id>/',end_usersview.success),
    path('single/',end_usersview.single),
    
    path('comming/<id>',end_usersview.comming_soon),
    path('soon/',end_usersview.com_soon),

    path('about_miogra/',end_usersview.about_miogra),
    path('aboutUs_miogra/<id>',end_usersview.aboutus_miogra),

    path('miogra/contact/',end_usersview.contact),
    path('enduser/contact/<id>',end_usersview.contact_details),

    path('terms_condition/',end_usersview.terms_condition),
    path('terms_and_condition/<id>',end_usersview.mio_terms_condition),
    
    path('privacy_policy/',end_usersview.privacypolicy),
    path('miogra_privacy_policy/<id>',end_usersview.miogra_privacypolicy),

    path('services/',end_usersview.mio_services),
    path('miogra_services/<id>',end_usersview.miogra_services),

     path('dummy/',end_usersview.dummy),
    
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)