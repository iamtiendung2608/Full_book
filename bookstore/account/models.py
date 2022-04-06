from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserDetails(models.Model):
    user = models.OneToOneField(User,null=True,on_delete=models.CASCADE,blank=True)
    profile_pic = models.ImageField(null=True, blank=True)
    GENDER_CHOICES = (
        ('MALE' , 'male'),
        ("FEMALE",'female')
    )
    firstName = models.CharField(max_length = 20,null=True)
    lastName = models.CharField(max_length = 20,null=True)
    age = models.FloatField(null=True)
    gender = models.CharField(max_length = 20 ,choices=GENDER_CHOICES, null=True,blank=True)
    def __str__(self):
        return self.firstName + ' ' + self.lastName
    def save(self,*args, **kwargs):
        super(UserDetails, self).save(*args, **kwargs)
