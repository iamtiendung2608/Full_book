from django.urls import path
from .views import homepage, details,addToCart,TagDetails,AddBook,EditBook,DeleteBook,CheckOut,CreateAddress,CreatePayment, callEmail, AddTag, EditTag, BillDetails

urlpatterns = [
    path('',homepage,name='home'),
    path('product/<int:id>', details,name='details'),
    path('add/<int:id>', addToCart,name='add'),
    path('bill/address', CreateAddress,name='assignAddress'),
    path('bill/payment', CreatePayment,name='assignPayment'),
    path('bill/confirm', callEmail,name='assignConfirm'),
    path('bill/details/<int:id>', BillDetails ,name='billDetails'),
    path('tag/<int:id>',TagDetails ,name='tag'),
    path('tag/add',AddTag ,name='Addtag'),
    path('tag/edit/<int:id>',EditTag ,name='Edittag'),
    path('book/add',AddBook ,name='adminAdd'),
    path('book/edit/<int:id>',EditBook,name = 'adminEdit'),
    path('book/delete/<int:id>',DeleteBook,name = 'adminDelete'),
    path('shop/checkout',CheckOut,name='checkout'),
]