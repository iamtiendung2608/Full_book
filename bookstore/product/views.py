from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.
from account.decorators import allowed_users
from .models import tag, book, Order,Bill
from django.shortcuts import redirect
from .forms import BookForm
from django.db.models import F
from django.db.models import Sum
from django.db.models import FloatField 
from account.form import AddressDetails
import random


from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string



def homepage(request):
    tags = tag.objects.all()
    '''if search button are hit Post Search form'''
    if request.method == 'POST':
        '''get value through name 'kw' from request'''
        name = request.POST.get('kw')
        '''__contains indicated that book's name must contain search value'''
        context = book.objects.filter(name__contains = name)
    else:
        '''normal load page get all the book'''
        context = book.objects.all()
    if not request.user.is_authenticated:
        return render(request,'home.html',{'contexts': context,'tags':tags})
    order = Order.objects.filter(account = request.user).values('book_id')
    TotalCount = book.objects.filter(id__in = order).count()
    return render(request,'home.html',{
        'contexts': context,
        'tags':tags,
    })

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
    item = book.objects.get(id=id)
    owner = request.user
    order = Order.objects.filter(account = owner,book=item)
    if order:
        order.update(quantity = F('quantity')+1)
    else:
        print('here')
        Order.objects.create(account = owner,book=item)
    return redirect('home')


def TagDetails(request, id = None):
    items = book.objects.filter(tag__id = id)
    return render(request,'home.html',{
        'contexts': items,
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
def DeleteBook(request, id = None):
    item = book.objects.get(id=id).delete()
    return HttpResponseRedirect('/')

@login_required(login_url='login')
@allowed_users(allowed_role=['admin'])
def CheckOut(request):
    contexts = {}
    return render(request,'profile.html',contexts)


@login_required(login_url='login')
@allowed_users(allowed_role=['customer'])
def CreateAddress(request):
    if request.method == 'POST':
        address = AddressDetails(request.POST)
        if address.is_valid():
            S = address.save()
            TotalPrice = Order.objects.filter(account = request.user).aggregate(total_group=Sum(F('quantity')*F('book__price'), output_field=FloatField()))
            CurrentBill = Bill.objects.create(user = request.user, delivery = S, total = TotalPrice['total_group'])
            Order.objects.filter(account = request.user).update(bill = CurrentBill)
            return redirect('home')
    else:
        num = str(random.randint(100000,999999))
        template = render_to_string('emailTemplate.html',{
            'username':request.user.username,
            'code':num
        })
        email = EmailMessage(
            'Thank You!',
            template,
            settings.EMAIL_HOST_USER,
            [request.user.email]
        )
        email.fail_silently = False
        email.send()
        form = AddressDetails()
        return render(request,'BillDetails.html',{'form':form})



