from django import forms
from django.forms import ModelForm
from .models import book,tag
class BookForm(ModelForm):
    name = forms.CharField(label='name', widget=forms.TextInput(attrs={'class':'form-control'}))
    price = forms.CharField(label='price', widget=forms.TextInput(attrs={'class':'form-control'}))
    image = forms.CharField(label='image', widget=forms.Textarea(attrs={'class':'form-control'}))
    author = forms.CharField(label='author', widget=forms.TextInput(attrs={'class':'form-control'}))
    descript = forms.CharField(label='image', widget=forms.Textarea(attrs={'class':'form-control'}))
    tag = forms.ModelMultipleChoiceField(label='tag',queryset=tag.objects.all())
    class Meta:
        model = book
        fields = ['name','price','image','author','descript','tag']
