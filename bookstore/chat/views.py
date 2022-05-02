from django.shortcuts import render
from account.decorators import allowed_users
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required(login_url='login')
def lobby(request):
    return render(request,'chat/lobby.html')