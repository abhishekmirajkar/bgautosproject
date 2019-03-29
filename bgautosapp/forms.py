from django import forms
from django.contrib.auth.models import User
from bgautosapp.models import customer,comment



class UserForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput())
    email=forms.EmailField()
    class Meta():
        model = customer
        fields = ('name','email','password','city','state','phoneno','address','pincode')

class UserProfileInfoForm(forms.ModelForm):
    class Meta():
        model = customer
        fields = ()


class CommentForm(forms.ModelForm):
    class Meta:
        model = comment
        fields=('content',)
