#coding=utf-8

from django.db import models
from django.contrib.auth.models import User

news_type = (
             (0, u'最新要闻'),
             (1, u'公司新闻'),
             (2, u'行业新闻'),
             )

product_type = (
                (0,u'工业润滑'),
                (1,u'包装用品'),
                (2,u'劳防用品'),
                )

class News(models.Model):
    title = models.CharField(verbose_name=u"标题",max_length=100,blank=True,null=True)
    context = models.TextField(verbose_name=u"内容",blank=True,null=True)
    time = models.DateTimeField(verbose_name=u"时间",blank=True,null=True)
    image = models.ImageField(verbose_name=u'图片', upload_to='image/news', blank=True, null=True)
    type = models.PositiveIntegerField(verbose_name=u'类型', choices=news_type, default=0)
    
    def __unicode__(self):
        return u'%s' % self.id
    
class Comment(models.Model):
    object = models.IntegerField(verbose_name=u"目标对象",max_length=100)
    author = models.CharField(verbose_name=u"作者",max_length=100,blank=True,null=True)
    context = models.CharField(verbose_name=u'内容', max_length=100)
    time = models.DateTimeField(verbose_name=u'时间')
    company = models.CharField(u"公司名称", max_length=100, null=True, blank=True)
    phone = models.CharField(verbose_name=u"联系电话", max_length=100, null=True, blank=True)
    email = models.EmailField(verbose_name=u"联系邮箱", null=True, blank=True)
    
    def __unicode__(self):
        return u'%s' % self.id
    
    def get_replys(self):
        return Comment.objects.filter(object = self.id)

class Product(models.Model):
    name = models.CharField(verbose_name=u"名称",max_length=100,blank=True,null=True)
    context = models.TextField(verbose_name=u"内容",blank=True,null=True)
    image = models.ImageField(verbose_name=u'图片', upload_to='image/product', blank=True, null=True)
    type = models.PositiveIntegerField(verbose_name=u'类型', choices=product_type, default=0)
    
    def __unicode__(self):
        return u'%s' % self.id
