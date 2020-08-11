from django.urls import path, re_path
from . import views

app_name = 'home_page'

urlpatterns=[
    path('', views.home, name='home'),
    path('base', views.base, name='base'),
    path('my_profile/',views.my_profile,name="my_profile"),
    re_path('profile/my_profile$',views.my_profile,name="my_profile"),
    path('change_profile', views.change_profile, name="change_profile"),
    re_path(r'change_profile$', views.change_profile, name="change_profile"),
]