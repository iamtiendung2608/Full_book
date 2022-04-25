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
    province = forms.CharField(label='Province', widget=forms.TextInput(attrs={'class':'form-control'}))
    city = forms.CharField(label='City', widget=forms.TextInput(attrs={'class':'form-control'}))
    details = forms.CharField(label='Address Details', widget=forms.Textarea(attrs={'class':'form-control'}))
    class Meta:
        model = address
        fields = '__all__'
        widgets = {'date_delivery': forms.DateInput(attrs={'class': 'datepicker','id':'id_date'})}
