from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(verbose_name='メールアドレス', unique=True)


class Category(models.Model):
    name = models.CharField(verbose_name='カテゴリー名', max_length=30)
    
    class Meta:
        verbose_name_plural = 'Categories'
    
    def __str__(self):
        return self.name


class Area(models.Model):
    name = models.CharField(verbose_name='エリア名', max_length=30)
    
    def __str__(self):
        return self.name


class Event(models.Model):
    name = models.CharField(verbose_name='セミナー名', max_length=250)
    host = models.CharField(verbose_name='主催者', max_length=100)
    description = models.TextField(verbose_name='セミナー詳細')
    image = models.ImageField(verbose_name='画像', upload_to='images/', blank=True, default='images/noimage.png')
    fee = models.IntegerField(verbose_name='参加費')
    capacity = models.IntegerField(verbose_name='定員')
    venue = models.CharField(verbose_name='会場', max_length=250)
    date = models.DateField(verbose_name='日付', auto_now=False, auto_now_add=False)
    category = models.ForeignKey(Category, verbose_name='カテゴリー', on_delete=models.PROTECT)
    area = models.ForeignKey(Area, verbose_name='エリア', on_delete=models.PROTECT)
    
    def __str__(self):
        return self.name
