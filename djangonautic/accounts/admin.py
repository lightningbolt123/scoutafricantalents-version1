# users/admin.py
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('bio', 'picture', 'phone_number', 'gender', 'date_of_birth', 'country_of_birth')}),
        )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('bio', 'picture', 'phone_number', 'gender', 'date_of_birth', 'country_of_birth')}),
        )
    list_display = ['username', 'first_name', 'last_name', 'bio', 'picture', 'phone_number', 'gender', 'date_of_birth', 'country_of_birth']
    

admin.site.register(CustomUser, CustomUserAdmin)