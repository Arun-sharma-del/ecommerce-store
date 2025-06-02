from django import forms
from .models import Order
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm




class CheckoutForm(forms.ModelForm):
  class Meta:
    model = Order
    fields = [ 'first_name','last_name', 'email','address', 'city']


class CustomRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        labels = {
            'username': 'Username',
            'first_name': 'First name',
            'last_name': 'Last name',
            'email': 'Email address',
            'password1': 'Password',
            'password2': 'Confirm Password',
        }

    def _init_(self, *args, **kwargs):
        super()._init_(*args, **kwargs)
        # Hide all help texts
        for field_name in self.fields:
            self.fields[field_name].help_text = ''
