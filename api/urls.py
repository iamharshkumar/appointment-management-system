from django.urls import path
from .views import *

urlpatterns = [
    path('signup', Signup, name='signup'),
    path('login', login, name='login'),

]