from pydoc import describe
from django.db import models
from account.form import CreateUserFrom
from account.models import UserDetails
from django.contrib.auth.models import User
class tag(models.Model):
    name = models.CharField(max_length = 20)
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

class Order(models.Model):
    book = models.ForeignKey(book, null=True,on_delete=models.CASCADE)
    account = models.ForeignKey(User, null=True,on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True,null=True)

class favor(models.Model):
    #wrong in cascade
    user = models.OneToOneField(UserDetails,on_delete=models.CASCADE,blank=True,null=True)
    tag = models.ManyToManyField(tag)
    