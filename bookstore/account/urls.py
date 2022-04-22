from django.urls import path, URLPattern
from .views import *
urlpatterns = [
    path('login',loginPage,name='login'),
    path('regist',registPage,name='regist'),
    path('logout',logoutUser,name='logout'),
    path('cart',Cart,name='cart'),
    path('cart/delete/<int:id>',RemoveItems,name='deleteItem'),
    path('cart/add/<int:id>',MoreItems,name='moreItems'),
    path('details/',UserProfile,name='profile'),
]
