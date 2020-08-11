from django.urls import path, re_path
from . import views

app_name = 'product_detail'

urlpatterns = [
    path('DescribeProduct/<slug>/', views.DescribeProduct.as_view(), name='DescribeProduct'),
    path('DisplayTypeProducts/<slug>/<value>', views.DisplayTypeProducts.as_view(), name='DisplayTypeProducts'),
    path('DisplayBrandProducts/<slug>/<value>', views.DisplayBrandProducts.as_view(), name='DisplayBrandProducts'),
]