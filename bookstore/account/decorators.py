from django.http import HttpResponse
from django.shortcuts import redirect
def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func



def allowed_users(allowed_role=[]):
    def decorator(view_func):
        def wrapper_func(request,*args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group in allowed_role:
                return view_func(request,*args, **kwargs)
            else:
                return HttpResponse('You are not authorize to see this page')
        return wrapper_func
    return decorator