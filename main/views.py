#coding=utf-8
from django.shortcuts import render_to_response, RequestContext
from django.http import HttpResponseRedirect
from models import News, Product, Comment
import datetime

def display(request):
    my_news = News.objects.filter(type='0')[:2]
    for tmp_news in my_news:
        tmp_news.context = tmp_news.context[:57]
    return render_to_response('display.jinja', {'my_news':my_news}, RequestContext(request))

def about_us(request):
    return render_to_response('about_us.jinja', {}, RequestContext(request))

def speech(request):
    return render_to_response('about_us.jinja', {'speech':'1'}, RequestContext(request))

def contact_us(request):
    return render_to_response('contact_us.jinja', {}, RequestContext(request))

def industry_news(request):
    news_type = request.GET.get('news_type', '0')
    my_news = News.objects.filter(type=news_type)
    for tmp_news in my_news:
        tmp_news.context = tmp_news.context.replace('\n', '<br>')
    return render_to_response('industry_news.jinja', {'my_news':my_news}, RequestContext(request))

def product(request):
    product_id = request.GET.get('product_id', '1')
    products = Product.objects.all()
    my_product = Product.objects.get(id=product_id)
    my_product.context = my_product.context.replace('\n', '<br>')
    return render_to_response('product.jinja', {'products':products, 'my_product':my_product}, RequestContext(request))

def question(request):
    return render_to_response('question.jinja', {'type':'1'}, RequestContext(request))

def answer(request):
    comments = Comment.objects.filter(object = 0)[:4:-1]
    comment_id = int(request.GET.get('comment_id', comments[0].id))
    return render_to_response('question.jinja', {'type':'2', 'comments':comments, 'comment_id':comment_id}, RequestContext(request))

def message(request):
    content = request.POST.get('content', '')
    person_name = request.POST.get('person_name', '')
    company_name = request.POST.get('company_name', '')
    phone = request.POST.get('content', '')
    email = request.POST.get('email', '')
    comment = Comment.objects.create(
                                     object = 0,
                                     author = person_name,
                                     context = content,
                                     time = datetime.datetime.now(),
                                     company = company_name,
                                     phone = phone,
                                     email = email,
                                     )
    return HttpResponseRedirect('/main/answer')

def reply(request):
    object = request.POST.get('object', '')
    content = request.POST.get('content', '')
    comment = Comment.objects.create(
                                     object = object,
                                     author = '',
                                     context = content,
                                     time = datetime.datetime.now(),
                                     company = '',
                                     phone = '',
                                     email = '',
                                     )
    return HttpResponseRedirect('/main/answer')