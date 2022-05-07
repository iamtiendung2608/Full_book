from django.contrib import admin
from .models import tag, book,Order,Bill
# Register your models here.
admin.site.register(book)
admin.site.register(tag)
admin.site.register(Order)
admin.site.register(Bill)