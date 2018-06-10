from django.db import models
from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import ResizeToFill


class Seller(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='编号')
    name = models.CharField(max_length=20, verbose_name='姓名')
    username = models.CharField(max_length=20, verbose_name='账号')
    psw = models.CharField(max_length=20, verbose_name='密码')

    class Meta:
        verbose_name = '商家'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s(%s)' % (self.id, self.name)


class Buyer(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='编号')
    name = models.CharField(max_length=20, verbose_name='姓名')
    username = models.CharField(max_length=20, verbose_name='账号')
    psw = models.CharField(max_length=20, verbose_name='密码')

    class Meta:
        verbose_name = '顾客'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s(%s)' % (self.id, self.name)


class Shop(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='编号')
    name = models.CharField(max_length=20, verbose_name='名字')
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, verbose_name='所属卖家编号')

    class Meta:
        verbose_name = '商店'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s(%s)' % (self.id, self.name)


class Goods(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='编号')
    name = models.CharField(max_length=20, verbose_name='名字')
    quantity = models.IntegerField(default=0, verbose_name='库存')
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, verbose_name='所属商店')
    image = ProcessedImageField(upload_to='goods_img', processors=[ResizeToFill(100, 100)], format='JPEG')
    unit_price = models.FloatField(verbose_name='单价')

    class Meta:
        verbose_name = '商品'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s(%s)' % (self.id, self.name)


class BuyerGoods(models.Model):
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE, verbose_name='买主编号')
    good = models.ForeignKey(Goods, on_delete=models.CASCADE, verbose_name='商品编号')
    quantity = models.IntegerField(default=1, verbose_name='购买数量')
    status = models.BooleanField(default=True, verbose_name='是否购买')

    class Meta:
        verbose_name = '购物情况'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s 购买了 %s 个 %s' % (self.buyer.name, self.quantity, self.good.name)
