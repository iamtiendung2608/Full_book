from pydoc import describe
from django.db import models
from account.form import CreateUserFrom
from account.models import UserDetails,address
from django.contrib.auth.models import User
class tag(models.Model):
    name = models.CharField(max_length = 20)
    fullName = models.CharField(max_length = 20,null=True)
    describe = models.TextField(null=True)
    def __str__(self):
        return self.name

# Create your models here.
class book(models.Model):
    name = models.CharField(max_length=50)
    price = models.FloatField()
    image = models.TextField()
    author = models.CharField(max_length=30,null=True)
    describe = models.TextField(null=True)
    tag = models.ManyToManyField(tag)
    def __str__(self):
        return self.name

class Bill(models.Model):
    user = models.OneToOneField(User,null=True,on_delete=models.CASCADE,blank=True)
    date_created = models.DateTimeField(auto_now_add=True,null=True)
    is_confirmed = models.BooleanField(default = False)
    total = models.FloatField(default=0.0000)
    delivery = models.OneToOneField(address,null=True,on_delete=models.CASCADE, blank=True )
    def __str__(self):
        return self.user.username + " bill "+str(self.date_created)





class Order(models.Model):
    account = models.ForeignKey(User, null=True,on_delete=models.CASCADE)
    book = models.ForeignKey(book, null=True,on_delete=models.CASCADE)
    quantity = models.DecimalField(default = 1,max_digits =5, decimal_places=0)
    bill = models.ForeignKey(Bill,null=True, on_delete=models.SET_NULL,blank=True)    
    @property
    def calValue(self):
        return self.book.price * self.quantity

class favor(models.Model):
    #wrong in cascade
    user = models.OneToOneField(UserDetails,on_delete=models.CASCADE,blank=True,null=True)
    tag = models.ManyToManyField(tag)