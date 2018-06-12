from django.urls import path
from .views import *


urlpatterns = [
    path('user/register/', register, name='register'),
    path('user/login/', login, name='login'),
    path('add_shop/', add_shop, name='add_shop'),
    path('test/', test, name='test'),

]
