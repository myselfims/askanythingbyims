from django import forms

class LoginForm(forms.Form):
    username = forms.CharField( max_length=50, required=True, label='Username')
    password = forms.CharField(max_length=20, widget=forms.PasswordInput)
    

class SignupForm(forms.Form):
    username = forms.CharField(max_length=50, required=True, label='Username')
    email = forms.EmailField(max_length=50, required=True, label='Email')
    password = forms.CharField(max_length=20, widget=forms.PasswordInput)