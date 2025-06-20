from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CheckoutForm(forms.Form):
    full_name = forms.CharField(label='Full Name', max_length=100)
    address = forms.CharField(widget=forms.Textarea)
    payment_method = forms.ChoiceField(
        choices=[('mock', 'Mock Payment'), ('cash', 'Cash on Delivery')],
        widget=forms.RadioSelect
    )

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )