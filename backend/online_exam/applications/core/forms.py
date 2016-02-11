from django import forms
from applications.user.models import User


class LoginForm(forms.Form):
    attrs = {'class': 'form-control', 'required': True}
    username = forms.CharField(widget=forms.TextInput(attrs=attrs))
    password = forms.CharField(widget=forms.PasswordInput(attrs=attrs))


class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        exclude = ['role', 'is_staff', 'is_active']
