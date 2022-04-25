from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms
from .models import UserDetails,address
class CreateUserFrom(UserCreationForm):
    class Meta: 
        model = User
        fields = ['username','email','password1','password2']


class DetailsForm(ModelForm):
    #add widget and fields
    GENDER_CHOICES = (
        ('MALE' , 'male'),
        ("FEMALE",'female')
    )
    gender = forms.CharField(label='gender', widget=forms.RadioSelect(choices=GENDER_CHOICES))
    class Meta:
        model = UserDetails
        fields = '__all__'
        exclude = ['user']

class AddressDetails(ModelForm):
    class Meta:
        model = address
        fields = '__all__'
        exclude = ['bill']
        widgets = {'date_delivery': forms.DateInput(attrs={'class': 'datepicker','type':'date'})}