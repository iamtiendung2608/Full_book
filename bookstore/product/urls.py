from django.urls import path
from .views import homepage, details,addToCart,TagDetails,AddBook,EditBook,DeleteBook,CheckOut,CreateAddress

urlpatterns = [
    path('',homepage,name='home'),
    path('product/<int:id>', details,name='details'),
    path('add/<int:id>', addToCart,name='add'),
    path('bill/', CreateAddress,name='addToBill'),
    path('tag/<int:id>',TagDetails ,name='tag'),
    path('book/add',AddBook ,name='adminAdd'),
    path('book/edit/<int:id>',EditBook,name = 'adminEdit'),
    path('book/delete/<int:id>',DeleteBook,name = 'adminDelete'),
    path('shop/checkout',CheckOut,name='checkout')
]