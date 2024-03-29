from django.urls import path, URLPattern
from .views import *



urlpatterns = [
    path('login',loginPage,name='login'),
    path('regist',registPage,name='regist'),
    path('logout',logoutUser,name='logout'),
    path('cart',Cart,name='cart'),
    path('cart/change/<int:id>',ChangeItems,name='changeValue'),
    path('details/',UserProfile,name='profile'),
]
