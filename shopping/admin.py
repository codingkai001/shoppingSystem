from django.contrib import admin
from .models import Seller, Buyer, Shop, BuyerGoods, Goods


@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'username']
    ordering = ['-id']


@admin.register(Buyer)
class BuyerAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'username']
    ordering = ['-id', ]


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'seller']
    ordering = ['-id', ]


@admin.register(Goods)
class GoodsAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'quantity', 'shop', 'unit_price', 'image']
    ordering = ['-id', ]


@admin.register(BuyerGoods)
class BuyerGoodsAdmin(admin.ModelAdmin):
    list_display = ['buyer', 'good', 'quantity', 'status']


admin.site.site_title = '网购后台管理系统'
admin.site.site_header = admin.site.site_title
