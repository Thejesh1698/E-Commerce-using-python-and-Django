from django.urls import path, re_path
from . import views

app_name = 'cart'

urlpatterns=[
    path('add_to_cart/<slug>/', views.add_to_cart, name='add_to_cart'),
    path('decrease_cart/<slug>/', views.decrease_cart, name='decrease_cart'),
    path('cart_page/',views.cart_page,name="cart_page"),
    path('remove_cart/<slug>/', views.remove_cart, name='remove_cart'),
    re_path(r'cart_page$', views.cart_page, name="cart_page"),
    path('my_orders/', views.my_orders, name='my_orders'),
    re_path(r'orders/my_orders$', views.my_orders, name="my_orders"),
]