from django.urls import path
from .views import homepage, details,addToCart,TagDetails,CreateAddress,CreatePayment, callEmail, BillDetails

urlpatterns = [
    path('',homepage,name='home'),
    path('product/<int:id>', details,name='details'),
    path('add/<int:id>', addToCart,name='add'),
    path('bill/address', CreateAddress,name='assignAddress'),
    path('bill/payment', CreatePayment,name='assignPayment'),
    path('bill/confirm', callEmail,name='assignConfirm'),
    path('bill/details/<int:id>', BillDetails ,name='billDetails'),
    path('tag/<int:id>',TagDetails ,name='tag'),
]