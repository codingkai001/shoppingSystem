from django.urls import path
from .views import *


urlpatterns = [
    path('user/register/', register, name='register'),
    path('test/', test, name='test'),

]
