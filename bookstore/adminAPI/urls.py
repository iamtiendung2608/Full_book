
from django.urls import path
from .views import *

urlpatterns = [
    path('tag/add',AddTag ,name='Addtag'),
    path('tag/edit/<int:id>',EditTag ,name='Edittag'),
    path('book/add',AddBook ,name='adminAdd'),
    path('book/edit/<int:id>',EditBook,name = 'adminEdit'),
    path('book/delete/<int:id>',DeleteBook,name = 'adminDelete'),
    path('shop/checkout',CheckOut,name='checkout'),
    path('shop/api',TikiAPI,name='viewAPI'),
]