from email import message
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

# Create your views here.
@unauthenticated_user
def registPage(request,template='account/templates'):
    
    form = CreateUserFrom()
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
            return redirect('home')
    return render(request,'login.html')

def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
@allowed_users(allowed_role=['customer'])
def Cart(request):
    order = Order.objects.filter(account = request.user).values('book_id')
    items = book.objects.filter(id__in = order)
    TotalCount = items.count()
    TotalPrice = items.aggregate(Sum('price'))['price__sum']
    return render(request, 'cart.html',{
        'items': items,
        'TotalPrice': TotalPrice,
        'TotalCount': TotalCount
    })
@login_required(login_url='login')
@allowed_users(allowed_role=['customer'])
def CheckOut(request):
    contexts = {}
    return render(request,'profile.html',contexts)

@login_required(login_url='login')
@allowed_users(allowed_role=['customer'])
def UserProfile(request):
    if request.method == 'POST':
        form = DetailsForm(request.POST)
        if form.is_valid():
            your_object = form.save(commit=False)
            your_object.user = request.user
            your_object.save()
            return redirect('home')
        else:
            print(form.errors.as_data())
            return redirect('userDetails')
    form = DetailsForm()
    return render(request,'userDetails.html',{'form':form})


        
