from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.
from account.decorators import allowed_users
from .models import tag, book, Order
from django.shortcuts import redirect
from .forms import BookForm
from django.db.models import F

def homepage(request):
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
        return render(request,'home.html',{'contexts': context,})
    order = Order.objects.filter(account = request.user).values('book_id')
    TotalCount = book.objects.filter(id__in = order).count()
    return render(request,'home.html',{
        'contexts': context,
        'count':TotalCount,
    })

def details(request, id = None):
    context = book.objects.get(id=id)
    return render(request,'details.html',{'context': context})

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
