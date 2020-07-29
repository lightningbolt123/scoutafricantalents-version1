from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
from django.contrib.auth.models import Group
from django import forms

CHOICES = [
    ('M','M'),
    ('F','F')
]

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(max_length=30, required=True)
    gender = forms.CharField(widget=forms.Select(choices=CHOICES), required=True)
    date_of_birth =  forms.DateField(widget=forms.TextInput(attrs={'type':'date'}))
    
    class Meta:
        model = CustomUser
        fields = [
        'username',
        'first_name',
        'last_name',
        'email',
        'bio',
        'picture',
        'phone_number',
        'picture',
        'date_of_birth',
        'country_of_birth',
        'password1',
        'password2'
        ]

class UserGroupForm(forms.ModelForm):
    group = forms.ModelChoiceField(label='Register as', queryset=Group.objects.all().exclude(name='admin'), required=True)

    class Meta:
        model = Group
        fields = [
            'group',
        ]

class CustomUserChangeForm(UserChangeForm):
    email = forms.EmailField(max_length=30, required=True)
    gender = forms.CharField(widget=forms.Select(choices=CHOICES), required=True)
    date_of_birth =  forms.DateField(widget=forms.TextInput(attrs={'type':'date'}))
    
    class Meta:
        model = CustomUser
        fields = [
        'bio',
        'picture',
        'phone_number',
        'picture',
        'date_of_birth',
        'country_of_birth'
        ]
