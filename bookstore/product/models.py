from pydoc import describe
from django.db import models
from django.contrib.auth.models import User

class tag(models.Model):
    name = models.CharField(max_length = 20)
    fullName = models.CharField(max_length = 20,null=True)
    describe = models.TextField(null=True)
    def __str__(self):
        return self.fullName

# Create your models here.
class book(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(default = 1,max_digits = 10, decimal_places=0)
    image = models.TextField()
    author = models.CharField(max_length=30,null=True)
    describe = models.TextField(null=True)
    Title = models.ForeignKey(tag, null=True, on_delete=models.SET_NULL)
    def __str__(self):
        return self.name


class Bill(models.Model):
    user = models.ForeignKey(User,null=True,on_delete=models.CASCADE,blank=True)
    date_created = models.DateTimeField(auto_now= True, null=True)
    total = models.DecimalField(default = 0,max_digits = 9, decimal_places=0)
    is_confirmed = models.BooleanField(default = False)
    def __str__(self):
        return self.user.username + " bill "+str(self.date_created)
    class Meta:
        unique_together = (('id','date_created'),)


class Order(models.Model):
    account = models.ForeignKey(User, null=True,on_delete=models.CASCADE)
    book = models.ForeignKey(book, null=True,on_delete=models.CASCADE)
    quantity = models.DecimalField(default = 1,max_digits =5, decimal_places=0)
    bill = models.ForeignKey(Bill,null=True, on_delete=models.SET_NULL,blank=True)    
    @property
    def calValue(self):
        return self.book.price * self.quantity
