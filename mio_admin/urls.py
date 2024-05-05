"""inventory URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path, include
from mio_admin import views

urlpatterns = [
    path('admin/',views.login_hub),
    path('logout/',views.logout),
    path('admin_index/<access_priveleges>',views.index),
    path('admin_dashboard/<access_priveleges>',views.dashboard),
    path('admin_product_details/<access_priveleges>',views.product_details),
    path('admin_single_store_details/<category>/<id>/<access_priveleges>',views.single_store_details),
    path('admin_order_details/<access_priveleges>',views.order_details),
    path('admin_banner/<access_priveleges>',views.bannerr),
    path('admin_customer_service/<access_priveleges>',views.customer_service),
    path('admin_product_appaoval/<access_priveleges>',views.product_appaoval),
    path('admin/edit_product/<product_id>/<category>/<access_priveleges>',views.edit_product),
    path('admin_hub_details/<access_priveleges>',views.hub_details),
    path('admin_hub_menu1/<access_priveleges>',views.hub_menu1),
    path('admin_hub_update/<id>/<access_priveleges>',views.hub_update),
    path('admin_user_add/<access_priveleges>',views.user_add),
    path('admin_user_menu/<access_priveleges>',views.user_menu),
    path('admin_user_update/<id>/<access_priveleges>',views.user_update),
    path('admin/customer/<access_priveleges>',views.customer),
    path('admin/delivery_boy_add/<add>/<access_priveleges>',views.delivery_boy_add),
    path('admin/delivery_boy_otp/<access_priveleges>',views.delivery_otp),
    path('admin/delivery_boy_manage/<access_priveleges>',views.delivery_boy_manage),
    path('admin/delivery_boy_single/<id>/<access_priveleges>',views.delivery_boy_single),
    path('admin/delivery_Commision/<access_priveleges>',views.delivery_Commision),
    path('admin/business_Commision/<access_priveleges>',views.business_Commision),
    path('admin/shutdown/<access_priveleges>',views.shutdownnn),
    path('admin/zone/<access_priveleges>',views.zonee),
    path('admin/get_shutdown',views.get_shutdown),
    path('admin/hsn/<access_priveleges>',views.hsn),
    path('admin/hsn_verification/<hsn_codee>',views.hsn_verification),
    path('delete_other_image/<product_id>/<position>/<access_priveleges>',views.delete_other_image),
    path('admin/emergency/<uid>',views.emergency),

]


# if settings.DEBUG:
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

