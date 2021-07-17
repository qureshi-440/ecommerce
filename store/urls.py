from . import views
from django.urls import path

app_name = 'store'

urlpatterns = [
    path("",views.home,name='home'),
    path('cart/',views.cart,name='cart'),
    path('checkout/',views.checkout,name='checkout'),
    path('update-cart/',views.updatacart,name='update_cart'),
    path('contact-us/',views.contact_us,name='contact'),
    path('about-us/',views.about_us,name='about'),
    path('process_order/',views.orderprocess,name='process_order'),
]