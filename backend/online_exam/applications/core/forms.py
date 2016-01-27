from django import forms


class LoginForm(forms.Form):
    attrs = {'class': 'form-control', 'required': True}
    username = forms.CharField(widget=forms.TextInput(attrs=attrs))
    password = forms.CharField(widget=forms.PasswordInput(attrs=attrs))
