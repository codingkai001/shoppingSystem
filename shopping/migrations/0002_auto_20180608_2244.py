# Generated by Django 2.0.3 on 2018-06-08 14:44

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('shopping', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goods',
            name='image',
            field=models.URLField(verbose_name='商品图片URL'),
        ),
    ]
