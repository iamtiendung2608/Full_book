import json
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.
from account.decorators import allowed_users
from account.models import Payment,address
from .models import tag, book, Order,Bill
from django.shortcuts import redirect
from .forms import BookForm, TagForm
from django.db.models import F, Q
from django.db.models import Sum, Count
from django.db.models import FloatField 
from account.form import AddressDetails,PaymentDetails
import random
from django.http import JsonResponse
from django.shortcuts import HttpResponse
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
import re
from django.core import serializers

def homepage(request):
    tags = tag.objects.all()
    if is_ajax(request = request):
        text = request.GET.get('input')
        data = book.objects.only('author','describe').filter(name__icontains = text)
        qs_json = serializers.serialize('json', data)
        return HttpResponse(qs_json, content_type='application/json')
    else:
        context = book.objects.all()
    return render(request,'home.html',{
        'contexts': context,
        'tags':tags,
    })


def callEmail(request):
    if is_ajax(request = request):
        num = random.randint(100000,999999)
        sendEmail(request.user.username,num,request.user.email)
        print(num)
        return JsonResponse({
            'code':num
        }, status=200)
    return HttpResponse('assignAddress')



def details(request, id = None):
    context = book.objects.get(id=id)
    tags = book.objects.filter(id=id).values_list('tag')
    books = book.objects.filter(tag__id__in =  tags).distinct()
    return render(request,'details.html',{
        'context': context,
        'books':books
    })




@login_required(login_url='login')
@allowed_users(allowed_role=['customer'])
def addToCart(request,id=None):
    if is_ajax(request = request):
        item = book.objects.get(id=id)
        owner = request.user
        order = Order.objects.filter(account = owner,book=item, bill=None)
        if order:
            order.update(quantity = F('quantity')+1)
        else:
            Order.objects.create(account = owner,book=item)
        return JsonResponse({'data':None},status = 200)


def TagDetails(request, id = None):
    items = book.objects.filter(tag__id = id)
    tags = tag.objects.all()
    return render(request,'home.html',{
        'contexts': items,
        'tags':tags,
    })



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





@login_required(login_url='login')
@allowed_users(allowed_role=['admin'])
def DeleteBook(request, id = None):
    item = book.objects.get(id=id).delete()
    return HttpResponseRedirect('/')

@login_required(login_url='login')
@allowed_users(allowed_role=['admin'])
def CheckOut(request):
    bills = Bill.objects.count()
    totals = Bill.objects.all().aggregate(Sum('total'))['total__sum']
    products = Order.objects.filter(~Q(bill = None)).aggregate(Count('quantity'))['quantity__count']
    x = Order.objects.filter(~Q(bill = None)).order_by('quantity').values_list('book__id')
    books = book.objects.filter(id__in = x )


    
    contexts = {
        'bills':bills,
        'totals':totals,
        'products':products,
        'books':books
    }

    return render(request,'checkOut.html',contexts)



@login_required(login_url='login')
@allowed_users(allowed_role=['customer'])
def CreateAddress(request):
    bill = Bill.objects.latest('date_created')
    ele = address.objects.get(bill = bill)
    if request.method == 'POST':
        addressDetails = AddressDetails(request.POST, instance = ele)
        if addressDetails.is_valid():
            addressDetails.save()
            filter1 = Q(account = request.user)
            filter2 = Q(bill = None)

            items = Order.objects.filter(filter1 & filter2)
            
            totals = items.aggregate(total_group=Sum(F('quantity')*F('book__price'), output_field=FloatField()))
            
            print(totals['total_group'])
            
            
            
            bill.total = totals['total_group']
            bill.save(update_fields=["total"])
            items.update(bill = bill)
            return redirect('home')
    else:
        form = AddressDetails(instance = ele)
        return render(request,'Address.html',{
            'form':form,
        })


@login_required(login_url='login')
@allowed_users(allowed_role=['customer'])
def CreatePayment(request):
    if request.method == 'POST':
        bill = Bill.objects.latest('date_created')
        element = Payment.objects.get(bill = bill)
        payment = PaymentDetails(request.POST, instance = element)
        if payment.is_valid():
            payment.save()
        return redirect('assignAddress')
    else:



        bill = Bill.objects.create(user = request.user)
        payment = Payment.objects.get(bill = bill)
        form = PaymentDetails(instance = payment)
        return render(request,'Payment.html',{
            'form':form,
        })


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'



def sendEmail(user, num, email):
    template = render_to_string('emailTemplate.html',{
            'username':user,
            'code':num
    })
    email = EmailMessage(
        'Thank You!',
        template,
        settings.EMAIL_HOST_USER,
        [email]
    )
    email.fail_silently = False
    email.send()


