from django import forms
from .models import Visitor

class EmailForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = Visitor
        fields = [
            'email',
        ]