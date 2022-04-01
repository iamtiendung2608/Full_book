from django.contrib import admin
from .models import tag, book,Order
# Register your models here.
admin.site.register(book)
admin.site.register(tag)
admin.site.register(Order)