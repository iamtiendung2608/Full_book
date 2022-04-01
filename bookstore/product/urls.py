from django.urls import path
from .views import homepage, details,addToCart

urlpatterns = [
    path('',homepage,name='home'),
    path('product/<int:id>', details,name='details'),
    path('add/<int:id>', addToCart,name='add'),
]