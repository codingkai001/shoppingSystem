from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import *
import json
from .models import Buyer, Seller, Goods, Shop, BuyerGoods
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from datetime import datetime, timedelta


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
                    response = JsonResponse({'status': 200})
                    # cookie一周内有效
                    response.set_cookie("SID", str(seller.id), expires=datetime.now() + timedelta(days=7))
                    return response
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
                    response = JsonResponse({'status': 200})
                    response.set_cookie("BID", str(buyer.id), expires=datetime.now() + timedelta(days=7))
                    return response
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
    :param request: name
    :return:status code
    """
    try:
        data = json.loads(request.body)
        seller_id = request.COOKIES.get('SID', '')
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
    :param request:name,quantity,image(file streaming),unit_price
    :return:status code
    """
    try:
        shop_id = request.COOKIES['SHOPID']
        shop = Shop.objects.get(id=shop_id)
        good = Goods()
        good.image = request.FILES['img']
        # print(good.image.url)
        # good.image.url = '4134343'
        good.name = request.POST['name']
        good.quantity = request.POST['quantity']
        good.unit_price = request.POST['unit_price']
        good.shop = shop
        good.save()
        return JsonResponse({'status': 200})
    except KeyError:
        return JsonResponse({'status': 408})
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
    try:
        buyer_id = request.COOKIES['BID']
        data = json.loads(request.body)
        buyer = Buyer.objects.get(id=buyer_id)
        good = Goods.objects.get(id=data['good_id'])
        quantity = data['quantity']
        status = data['status']
        item = BuyerGoods()
        item.quantity = quantity
        item.status = status
        item.buyer = buyer
        item.good = good
        item.save()
        return JsonResponse({'status': 200})
    except (Buyer.DoesNotExist, Goods.DoesNotExist, KeyError):
        return JsonResponse({'status': 409})
    except json.JSONDecodeError:
        return JsonResponse({'status': 402})


@require_GET
def get_goods_list(request):
    """
    buyer get his/her goods list
    :param request: buyer_id
    :return:goods list(json)
    """
    try:
        buyer = request.GET['buyer_id']
        # content_type = request.META['CONTENT_TYPE']
        good_list = BuyerGoods.objects.filter(buyer=buyer).filter(status=1)
        # if good_list.count() == 0:
        #     return JsonResponse({'status': 410})
        data = serializers.serialize('json', good_list, fields=('buyer', 'good', 'quantity'), ensure_ascii=False)
        return JsonResponse({'status': 200, 'data': data})
    except KeyError:
        return JsonResponse({'status': 410})
    except Exception as e:
        print(e)
        return JsonResponse({'status': 500})


@require_GET
def get_shop_list(request):
    """
    seller get his/her all shop
    :param request:
    :return:shop list(json)
    """
    try:
        seller = request.COOKIES.get('SID', '')
        shop_list = Shop.objects.filter(seller=seller)
        data = serializers.serialize('json', shop_list, fields=('name', 'seller'), ensure_ascii=False)
        return JsonResponse({'status': 200, 'data': data})
    except KeyError:
        return JsonResponse({'status': 410})
    except Exception as e:
        print(e)
        return JsonResponse({'status': 500})


@csrf_exempt
@require_GET
def show_shop(request):
    """
    show all shops to buyer
    :param request:
    :return: shop list
    """
    try:
        shop_list = Shop.objects.all()
        data = serializers.serialize('json', shop_list, fields=('name', 'seller'), ensure_ascii=False)
        return JsonResponse({'status': 200, "data": data})

    except Exception:
        return JsonResponse({'status': 500})


@csrf_exempt
@require_GET
def show_goods(request):
    try:
        shop = Shop.objects.get(id=request.GET['shop_id'])
        goods_list = Goods.objects.filter(shop=shop)
        good_detail = []

        for good in goods_list:
            item = {}  # 外部申明会覆盖
            item['id'] = good.id
            item['name'] = good.name
            item['quantity'] = good.quantity
            item['unit_price'] = good.unit_price
            item['shop_id'] = good.shop.id
            item['image_url'] = good.image.url
            good_detail.append(item)

        response = JsonResponse({'status': 200, 'data': good_detail})
        return response
    except (KeyError, Shop.DoesNotExist):
        return JsonResponse({'status': 408})


@csrf_exempt
@require_POST
def shop_detail(request):
    try:
        id = json.loads(request.body)['shop_id']
        shop = Shop.objects.get(id=id)
        response = JsonResponse({'status': 200, 'name': str(shop.name)})
        response.set_cookie('SHOPID', shop.id)
        return response
    except Shop.DoesNotExist:
        return JsonResponse({'status': 408})
    except json.JSONDecodeError:
        return JsonResponse({'status': 402})


@csrf_exempt
def test(request):
    if request.method == 'GET':
        return HttpResponse('get')

    if request.method == 'POST':
        return JsonResponse({'data': '分割'})
