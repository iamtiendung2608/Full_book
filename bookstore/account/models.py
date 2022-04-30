from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
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
    Province =models.CharField(max_length =30,null=True)
    City = models.CharField(max_length=30,null= True)
    Details = models.CharField(max_length=50,null=True)
    date_delivery = models.DateField(null=True)
    confirmCode = models.CharField(max_length = 10, null=True)
