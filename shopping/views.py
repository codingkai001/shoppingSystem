from django.http import JsonResponse
from django.views.decorators.http import *


@require_POST
def login(request):
    """
    user login
    :param request:username,psw
    :return: user`s data(json)
    """
    pass


@require_POST
def register(request):
    """
    user register
    :param request:name,username,psw
    :return: status code(success/fail)
    """
    pass


@require_POST
def add_shop(request):
    """
    seller create a shop
    :param request: name,seller`s id
    :return:status code
    """
    pass


@require_POST
def add_good(request):
    """
    seller add goods to his/her shop
    :param request:name,quantity,image(file streaming),unit_price,shop_id
    :return:status code
    """
    pass


@require_POST
def buy_good(request):
    """
    buyer add goods to his/her list
    :param request: buyer_id,good_id,quantity,status(1 for add,0 for cancel)
    :return:status code
    """
    pass


@require_GET
def get_goods_list(request):
    """
    buyer get his/her goods list
    :param request: buyer_id
    :return:goods list(json)
    """
    pass


@require_GET
def get_shop_list(request):
    """
    seller get his/her all shop
    :param request:sller_id
    :return:shop list(json)
    """
    pass
