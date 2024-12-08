from django import forms
from django.contrib.auth.forms import UserCreationForm

from market.models import User, Product


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        ))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
            }
        ))

class RegisterForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        ))
    email = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control', 'placeholder': 'Enter your email'
            }
        ))
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control','placeholder': 'Enter your password',
            }
        ))
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control', 'placeholder': 'Enter your password again'
            }
        ))


    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'is_buyer', 'is_farmer')

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [ 'description', 'price', 'image', 'name']

        widgets = {

            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Brief Description of the produce'}),
            'price': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Price of the product, include the unit e.g per piece or per bunch etc'}),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'title': 'Upload a photo of your produce',
                 'accept': 'image/*'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter the Product mame'}),
        }



class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'photo']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})


