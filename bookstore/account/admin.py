from django.contrib import admin
from .models import UserDetails,address,Payment
# Register your models here.
admin.site.register(UserDetails)
admin.site.register(address)
admin.site.register(Payment)