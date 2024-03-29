from django import forms
from django.forms import ModelForm
from .models import book,tag,Bill
class BookForm(ModelForm):
    name = forms.CharField(label='name', widget=forms.TextInput(attrs={'class':'form-control'}))
    price = forms.CharField(label='price', widget=forms.TextInput(attrs={'class':'form-control'}))
    image = forms.CharField(label='image', widget=forms.Textarea(attrs={'class':'form-control'}))
    author = forms.CharField(label='author', widget=forms.TextInput(attrs={'class':'form-control'}))
    describe = forms.CharField(label='describe', widget=forms.Textarea(attrs={'class':'form-control'}))
    Title = forms.ModelChoiceField(label='Title',queryset=tag.objects.all())
    class Meta:
        model = book
        fields = ['name','price','image','author','describe','Title']


class TagForm(ModelForm):
    class Meta:
        model = tag
        fields = '__all__'
