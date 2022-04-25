from django.contrib import admin
from .models import tag, book,Order,favor,Bill
# Register your models here.
admin.site.register(book)
admin.site.register(tag)
admin.site.register(Order)
admin.site.register(favor)                                                                                                                                                                                
admin.site.register(Bill)