from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from product.models import  Bill
# Create your models here.
class UserDetails(models.Model):
    user = models.OneToOneField(User,null=True,on_delete=models.CASCADE,blank=True)
    profile_pic = models.ImageField(default="defaultProfile.jpg",null=True, blank=True)
    GENDER_CHOICES = (
        ('MALE' , 'male'),
        ("FEMALE",'female')
    )
    firstName = models.CharField(max_length = 20,null=True, blank=True)
    lastName = models.CharField(max_length = 20,null=True, blank=True)
    age = models.FloatField(null=True, blank=True)
    gender = models.CharField(max_length = 20 ,choices=GENDER_CHOICES, null=True,blank=True)
    def __str__(self):
        return self.user.username +' Profile'
    def save(self,*args, **kwargs):
        super(UserDetails, self).save(*args, **kwargs)

class address(models.Model):
    bill = models.ForeignKey(Bill,null=True, blank=True, on_delete = models.CASCADE)

    Province =models.CharField(max_length = 30,null=True)
    City = models.CharField(max_length= 30,null= True)
    Ward = models.CharField(max_length = 30 ,null = True)


    Details = models.CharField(max_length=50,null=True)
    date_delivery = models.DateField(null=True)
    


class Payment(models.Model):
    bill = models.ForeignKey(Bill,null=True, blank=True, on_delete = models.CASCADE)

    name = models.CharField(max_length = 50 , null=True)
    CardNumber = models.CharField(max_length=16, null=True)
    ExpirationMonth = models.DecimalField(default = 1,max_digits =5, decimal_places=0)
    ExpirationYear = models.DecimalField(default = 2022,max_digits =5, decimal_places=0)
    SecurityCode = models.CharField(max_length = 3,null=True)
    

