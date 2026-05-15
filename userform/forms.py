from django import forms
from .models import UserFormData

class UserForm(forms.ModelForm):
    class Meta:
        model = UserFormData
        fields = ['name', 'email', 'phone', 'address', 'city', 'message']