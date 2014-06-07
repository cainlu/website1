#coding=utf-8
 
from django.contrib import admin
from models import News, Product
import os
 
class News_Admin(admin.ModelAdmin):
    model = News
    list_display = ('id', 'title', 'context', 'time', 'image', 'type',)
    list_filter = ('type',)
    list_editable = ('title', 'context', 'time', 'image', 'type',)

class Product_Admin(admin.ModelAdmin):
    model = Product
    list_display = ('id', 'name', 'context', 'image', 'type',)
    list_filter = ('type',)
    list_editable = ('name', 'context', 'image', 'type',)

admin.site.register(News, News_Admin)
admin.site.register(Product, Product_Admin)