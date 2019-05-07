from django import forms


class UserForm(forms.Form):
    login = forms.CharField(max_length=60)
    name = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100)
