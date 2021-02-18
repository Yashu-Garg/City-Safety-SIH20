from . import models
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import People

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = People
        fields = ('EmailId',)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = People
        fields = ('EmailId',)


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), required=True, max_length=15)
    gender = forms.ChoiceField(choices=(('M', 'Male'),('F', 'Female')) )

    class Meta():
        model = models.People
        fields = ['name','gender','Age' ,'ContactNumber', 'Aadhar_Number','RecoveryMail','RecoveryNumber','EmailId','password']

class LoginForm(forms.Form):
    EmailId=forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput(), required=True, max_length=15)

    # class Meta():
    #     model = models.People
    #     fields = ['EmailId','password']