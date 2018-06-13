from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import *
import json
from .models import Buyer, Seller, Goods, Shop
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
@require_POST
def login(request):
    """
    user login
    :param request:username,psw,role(1 for seller,0 for buyer)
    :return: status code(success/fail)
    """
    try:
        data = json.loads(request.body)
        role = data['role']
        # user is a seller
        if role == 1:
            username = data['username']
            try:
                seller = Seller.objects.get(username=username)
                if seller.psw == data['psw']:
                    return JsonResponse({'status': 200})
                else:
                    return JsonResponse({'status': 406})
            except Seller.DoesNotExist:
                return JsonResponse({'status': 406})
        # user is a buyer
        else:
            username = data['username']
            try:
                buyer = Buyer.objects.get(username=username)
                if buyer.psw == data['psw']:
                    return JsonResponse({'status': 200})
                else:
                    return JsonResponse({'status': 406})
            except Buyer.DoesNotExist:
                return JsonResponse({'status': 406})
    except json.JSONDecodeError:
        return JsonResponse({'status': 402})


@csrf_exempt
@require_POST
def register(request):
    """
    user register
    :param request:name,username,psw，role(1 for seller,0 for buyer)
    :return: status code(success/fail)
    """
    try:
        data = json.loads(request.body)
        # if role is not passed, default role is buyer
        role = data.get('role', 0)
        # user is a seller
        if role == 1:
            username = data['username']
            try:
                user = Seller.objects.get(username=username)
                # this user has been registered.
                return JsonResponse({'status': 401})
            # this user has not been registered.
            except Seller.DoesNotExist:
                name = data['name']
                psw = data['psw']
                new_seller = Seller()
                new_seller.name = name
                new_seller.username = username
                new_seller.psw = psw
                new_seller.save()
        # user is abuyer
        else:
            username = data['username']
            try:
                user = Buyer.objects.get(username=username)
                # this user has been registered.
                return JsonResponse({'status': 401})
            # this user has not been registered.
            except Buyer.DoesNotExist:
                name = data['name']
                psw = data['psw']
                new_buyer = Buyer()
                new_buyer.name = name
                new_buyer.username = username
                new_buyer.psw = psw
                new_buyer.save()

        return JsonResponse({'status': 200})

    except json.JSONDecodeError:
        return JsonResponse({'status': 402})


@csrf_exempt
@require_POST
def add_shop(request):
    """
    seller create a shop
    :param request: name,seller`s id
    :return:status code
    """
    try:
        data = json.loads(request.body)
        seller_id = data['id']
        try:
            seller = Seller.objects.get(id=seller_id)
            name = data['name']
            shop = Shop()
            shop.seller = seller
            shop.name = name
            shop.save()
        except Seller.DoesNotExist:
            return JsonResponse({'status': 407})

        return JsonResponse({'status': 200})

    except json.JSONDecodeError:
        return JsonResponse({'status': 402})


@csrf_exempt
@require_POST
def add_good(request):
    """
    seller add goods to his/her shop
    :param request:name,quantity,image(file streaming),unit_price,shop_id
    :return:status code
    """
    try:
        shop = Shop.objects.get(id=request.POST['shop_id'])
        good = Goods()
        good.image = request.FILES['img']
        print(good.image.url)
        # good.image.url = '4134343'
        good.name = request.POST['name']
        good.quantity = request.POST['quantity']
        good.unit_price = request.POST['unit_price']
        good.shop = shop
        good.save()
        return JsonResponse({'status': 200})

    except Shop.DoesNotExist:
        return JsonResponse({'status': 408})


@csrf_exempt
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


@csrf_exempt
def test(request):
    if request.method == 'GET':
        return HttpResponse('get')

    if request.method == 'POST':
        return HttpResponse('post')
