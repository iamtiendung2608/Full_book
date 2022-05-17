from email import message
from django.db.models import FloatField 
from django.shortcuts import render
from .form import CreateUserFrom,DetailsForm
from django.contrib import messages
from django.shortcuts import redirect
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate,login, logout
from .decorators import unauthenticated_user
from django.contrib.auth.models import Group
from product.models import book, Order
from .decorators import allowed_users
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.contrib.auth.models import User
from .models import UserDetails
from product.models import  Bill
from django.db.models import F, Q
# Create your views here.
@unauthenticated_user
def registPage(request,template='account/templates'):
    if request.method == 'POST':
        form = CreateUserFrom(request.POST)
        if form.is_valid():
            user = form.save()
            group = Group.objects.get(name='customer')
            user.groups.add(group)
            return HttpResponseRedirect('login')
        else:
            messages.error(request,form.errors.as_data())
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
            redirect_to = request.POST.get('next', request.GET.get('next', 'home') if not None else 'home' )
            return redirect(redirect_to)
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
    
    filter1 = Q(account = request.user)
    filter2 = Q(bill = None)

    items = Order.objects.filter(filter1 & filter2)
    TotalPrice = items.aggregate(total_group=Sum(F('quantity')*F('book__price'), output_field=FloatField()))
    return render(request, 'cart.html',{
        'items': items,
        'Sum':TotalPrice['total_group'],
    })





@login_required(login_url='login')
@allowed_users(allowed_role=['customer'])
def ChangeItems(request, id = None):

    filter1 = Q(account = request.user)
    filter2 = Q(bill = None)
    filter3 = Q(id = id)

    order = Order.objects.get(filter1 & filter2 & filter3)
    
    order.quantity = int(request.GET.get('quantity'))

    order.save(update_fields=["quantity"])

    return JsonResponse({'data':None}, status = 200)





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
            return redirect('userDetails')
    form = DetailsForm(instance = details)
    filter1 = Q(user=request.user)
    filter2 = Q(is_confirmed = True)
    bills = Bill.objects.filter(filter1 & filter2)
    return render(request,'userDetails.html',{
        'form':form,
        'pic':details.profile_pic,
        'bills': bills,
    })

    