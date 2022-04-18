from django.urls import path
from .views import homepage, details,addToCart,TagDetails,AddBook,EditBook,DeleteBook,CheckOut

urlpatterns = [
    path('',homepage,name='home'),
    path('product/<int:id>', details,name='details'),
    path('add/<int:id>', addToCart,name='add'),
    path('tag/<int:id>',TagDetails ,name='tag'),
    path('book/add',AddBook ,name='adminAdd'),
    path('book/edit',EditBook,name = 'adminEdit'),
    path('book/edit',DeleteBook,name = 'adminDelete'),
    path('shop/checkout',CheckOut,name='checkout')
]