from email import message
from django.db.models import FloatField 
from django.shortcuts import render
from .form import CreateUserFrom,DetailsForm
from django.contrib import messages
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate,login, logout
from .decorators import unauthenticated_user
from django.contrib.auth.models import Group
from product.models import book, Order
from .decorators import allowed_users
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.contrib.auth.models import User
from .models import UserDetails
from django.db.models import F
# Create your views here.
@unauthenticated_user
def registPage(request,template='account/templates'):
    if request.method == 'POST':
        form = CreateUserFrom(request.POST)
        if form.is_valid():
            user = form.save()
            group = Group.objects.get(name='customer')
            user.groups.add(group)
            username = form.cleaned_data.get('username')
            messages.success(request,'Hello user: '+username)
            return HttpResponseRedirect('login')
        else:
            messages.error(request,form.error_messages)
            return redirect('regist')
    form = CreateUserFrom()
    context = {'form':form}
    return render(request,'regist.html',context)

@unauthenticated_user
def loginPage(request,template='account/templates'):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request,username = username, password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.info(request,'username or password is incorrect')
            return redirect('login')
    return render(request,'login.html')

def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
@allowed_users(allowed_role=['customer'])
def Cart(request):
    # order = Order.objects.filter(account = request.user).values('book_id')
    # items = book.objects.filter(id__in = order)
    # TotalCount = items.count()aggregate(Sum('price'))['price__sum']
    items = Order.objects.filter(account = request.user)
    TotalPrice = Order.objects.filter(account = request.user).aggregate(total_group=Sum(F('quantity')*F('book__price'), output_field=FloatField()))
    return render(request, 'cart.html',{
        'items': items,
        'Sum':TotalPrice['total_group'],
    })

@login_required(login_url='login')
@allowed_users(allowed_role=['customer'])
def MoreItems(request, id = None):
    order = Order.objects.filter(id=id)
    order.update(quantity = F('quantity')+1)
    return redirect('cart')

@login_required(login_url='login')
@allowed_users(allowed_role=['customer'])
def RemoveItems(request, id = None):
    order = Order.objects.filter(id=id)
    if(order.values().quantity==1):
        order.delete()
    else:
        order.update(quantity = F('quantity')-1)
    return redirect('cart')


@login_required(login_url='login')
@allowed_users(allowed_role=['customer'])
def UserProfile(request):
    details = UserDetails.objects.get(user = request.user)
    if request.method == 'POST':
        form = DetailsForm(request.POST,request.FILES, instance = details)
        if form.is_valid():
            form.save()
            return redirect('profile')
        else:
            print(form.errors.as_data())
            return redirect('userDetails')
    form = DetailsForm(instance = details)
    return render(request,'userDetails.html',{
        'form':form,
        'pic':details.profile_pic
        })
@login_required(login_url='login')
@allowed_users(allowed_role=['customer'])
def CartDelete(request, id = None):
    pass
    
