from django.urls import path
from .views import *


urlpatterns = [
    path('user/register/', register, name='register'),
    path('user/login/', login, name='login'),
    path('add_shop/', add_shop, name='add_shop'),
    path('add_good/', add_good, name='add_good'),
    path('buy_good/', buy_good, name='buy_good'),
    path('get_goods_list/', get_goods_list, name='get_good_list'),
    path('get_shop_list/', get_shop_list, name='get_shop_list'),
    path('test/', test, name='test'),

]
