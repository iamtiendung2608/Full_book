from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.
from account.decorators import allowed_users
from .models import tag, book, Order
from django.shortcuts import redirect



@login_required(login_url='login')
@allowed_users(allowed_role=['customer'])
def homepage(request):
    order = Order.objects.filter(account = request.user).values('book_id')
    TotalCount = book.objects.filter(id__in = order).count()
    context = book.objects.all()
    return render(request,'home.html',{
        'contexts': context
    })


@login_required(login_url='login')
@allowed_users(allowed_role=['customer'])
def details(request, id = None):
    context = book.objects.get(id=id)
    return render(request,'details.html',{'context': context})

@login_required(login_url='login')
@allowed_users(allowed_role=['customer'])
def addToCart(request,id=None):
    item = book.objects.get(id=id)
    account = request.user
    order = Order(book=item, account=account)
    order.save()
    return redirect('home')
    
