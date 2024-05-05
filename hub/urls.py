from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from hub import views

urlpatterns = [

    path('hub/dashboard/<hub>',views.hub_dashboard),
    path('hub/delivery_boy/<hub>',views.delivery_boy),
    path('hub/hub_product_arrive/<hub>',views.hub_product_arrive),
    path('hub/delivery/<hub>',views.delivery),
    path('hub/hub_other_region/<hub>',views.hub_other_region),
    path('hub/invoice/<id>',views.invoice),
    
    
    path('hub/hub_picked/<order_id>/<delivery_person>',views.hub_picked),
    path('hub/normal_delivery_get_product_order/<id>/<region>',views.normal_delivery_get_product_order),
    path('hub/shipped_delivery_product/<id>',views.shipped_delivery_product),
    path('hub/out_of_delivery/<order_id>',views.out_of_delivery),

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
