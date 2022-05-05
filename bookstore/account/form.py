from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms
from .models import UserDetails,address,Payment
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
    gender = forms.ChoiceField(label='gender', choices=GENDER_CHOICES)
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

class PaymentDetails(ModelForm):
    Year_Choice = (
        (2022,2022),
        (2023,2023),
        (2024,2024),
        (2025,2025)
    )
    Month_Choice = (
        (1,1),
        (2,2),
        (3,3),
        (4,4),
        (5,5),
        (6,6),
        (7,7),
        (8,8),
        (9,9),
        (10,10),
        (11,11),
        (12,12)
    )
    ExpirationMonth = forms.ChoiceField(choices = Month_Choice)
    ExpirationYear = forms.ChoiceField(choices = Year_Choice)
    class Meta:
        model = Payment
        fields = '__all__'
