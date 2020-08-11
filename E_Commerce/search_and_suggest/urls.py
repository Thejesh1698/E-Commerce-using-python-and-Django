from django.urls import path, re_path
from . import views

app_name = 'search_and_suggest'

urlpatterns = [
    path('search/', views.search, name='search'),
    re_path(r'search$', views.search, name='search'),
    path('SearchRelatedProducts/<slug>/<value>', views.SearchRelatedProducts.as_view(), name='SearchRelatedProducts'),
]