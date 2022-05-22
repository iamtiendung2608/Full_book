from django.shortcuts import render

# Create your views here.
import json
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.
from account.decorators import allowed_users
from product.models import tag, book, Order,Bill
from django.shortcuts import redirect
from product.forms import BookForm, TagForm
from django.db.models import F, Q
from django.db.models import Sum, Count
from django.http import JsonResponse
from django.conf import settings
from io import BytesIO
import base64
from django.template.loader import render_to_string
import re
from django.core import serializers
import requests
import matplotlib.pyplot as plt
import numpy as np
from bs4 import BeautifulSoup
from collections import defaultdict
import matplotlib
matplotlib.use('Agg')






@login_required(login_url='login')
@allowed_users(allowed_role=['admin']) 
def AddBook(request):
    if request.method == 'POST' :
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
    else:
        form = BookForm()
    return render(request, 'edit.html',{'form':form})




@login_required(login_url='login')
@allowed_users(allowed_role=['admin'])
def EditBook(request, id = None):
    item = book.objects.get(id=id)
    if request.method == 'POST':
        form = BookForm(request.POST,instance = item)
        if form.is_valid:
            form.save()
            return HttpResponseRedirect('/')
    else:
        form = BookForm(instance = item)
    return render(request, 'edit.html',{'form':form})



@login_required(login_url='login')
@allowed_users(allowed_role=['admin'])
def AddTag(request):
    if(request.method == 'POST'):
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
    else:
        form = TagForm()
    return render(request, 'edit.html',{'form':form})


@login_required(login_url='login')
@allowed_users(allowed_role=['admin'])
def EditTag(request, id = None):
    item = tag.objects.get(id=id)
    if request.method == 'POST':
        form = TagForm(request.POST,instance = item)
        if form.is_valid:
            form.save()
            return HttpResponseRedirect('/')
    else:
        form = TagForm(instance = item)
    return render(request, 'edit.html',{'form':form})




#need html to access this function
@login_required(login_url='login')
@allowed_users(allowed_role=['admin'])
def DeleteBook(request, id = None):
    item = book.objects.get(id=id).delete()
    return HttpResponseRedirect('/')



@login_required(login_url='login')
@allowed_users(allowed_role=['admin'])
def CheckOut(request):


    bills = Bill.objects.filter(is_confirmed = False).count()
    
    #get all purchase
    totals = Bill.objects.all().aggregate(Sum('total'))['total__sum']

    #get all orders
    # products = Order.objects.filter(~Q(bill = None)).values_list('quantity', flat=True)
    # print(products)

    
    x = Order.objects.filter(~Q(bill = None)).order_by('-quantity')

    books = []
    for i in x.values_list('book__name', flat=True):
        books.append(book.objects.get(name = i))
        
    

    values, names, quantities = merge_slices(x.values_list('quantity', flat=True), x.values_list('book__Title__fullName', flat=True))
    # print(s)
    graphic = graphics(values, names)
    contexts = {
        'bills':bills,
        'totals':int(totals),
        'products':quantities,
        'books':books[:5],
        'graphic':graphic
    }
    return render(request,'checkOut.html',contexts)


def merge_slices(list0, list1):
    # print(list0)
    # print(list1)
    sum = 0 


    dict_slices = defaultdict(lambda: 0)
    for val, title in zip(list0, list1):
        dict_slices[title] += val
        sum+=val
    return list(dict_slices.values()), list(dict_slices.keys()),sum

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'




def TikiAPI(request):
    if is_ajax(request = request):
        subDomain = request.GET.get('value')
        splitDomain = subDomain.split(' ')
        mergeDomain = '+'.join(splitDomain)
        urls = "https://tiki.vn/search?q={}".format(mergeDomain)
        data = Scrap(urls)
        return JsonResponse({
            'data':data
        }, status=200)

def Scrap(urls):
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'
    }
    html_request =  requests.get(urls,headers = headers)
    soup = BeautifulSoup(html_request.text,'html.parser')
    books = soup.find_all('span',class_ = 'style__StyledItem-sc-18svp8n-0 fkDgwT')
    res = []
    for book in books[:10]:
        info = book.find('div',class_='info')
        name = info.find('h3').text
        price_discount = info.find('div', class_='price-discount').text
        last_Price = price_discount.split('-')
        thumbnail = book.find('picture').find('img')
        data = {
            'Name':name,
            'Price': last_Price[0],
            'Image':thumbnail['src']
        }
        res.append(data)
    return res


def graphics(name, value):



    plt.title('Trending book title tag')
    plt.ylabel("")
    pie = plt.pie(name, autopct='%1.0f%%', pctdistance=1.1, labeldistance=1.2, startangle=0)
    # plt.legend(loc = 3, labels = value)
    plt.legend(pie[0],value, bbox_to_anchor=(1.03,0.2), loc="center right", fontsize=10, 
           bbox_transform=plt.gcf().transFigure)



    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')
    return graphic
