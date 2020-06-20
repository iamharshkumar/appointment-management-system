from django.urls import path
from .views import *

urlpatterns = [
    path('signup', Signup.as_view(), name='signup'),
    path('login', login.as_view(), name='login'),
    path('admin-login', Admin_login.as_view(), name='admin-login'),
]