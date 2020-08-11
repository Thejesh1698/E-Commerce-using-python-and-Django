from django.urls import path, re_path
from . import views

app_name = 'billing'

urlpatterns = [
    path('address_page', views.address_page, name='address_page'),
    re_path('address/address_page$', views.address_page, name='address_page'),
    path('proceed_to_payment', views.proceed_to_payment, name='proceed_to_payment'),
    re_path(r'proceed_to_payment$', views.proceed_to_payment, name='proceed_to_payment'),
    path('pay', views.pay, name='pay'),
    re_path(r'pay$', views.pay, name='pay'),
]