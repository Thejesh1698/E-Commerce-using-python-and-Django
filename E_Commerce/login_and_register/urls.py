
from django.urls import path, include, re_path
from . import views
app_name = 'login_and_register'

urlpatterns=[
    path('loginPage/',views.login_page,name='loginPage'),
    re_path(r'loginPage$',views.login_page,name='loginPage'),
    re_path(r'login_or_register$',views.login_or_register,name='login_or_register'),
    re_path(r'logout$',views.user_logout,name='logout'),
]