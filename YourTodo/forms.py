from django import forms
from .models import Todo
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
class ToDoForms(forms.ModelForm):
    class Meta:
        model=Todo
        fields=['Title','Description','Isdone','due_date','priority']
        widgets = {
    'due_date': forms.DateInput(attrs={'type': 'date'})  
}
class UserRegistrationForm(UserCreationForm):
    email=forms.EmailField
    class Meta:
        model=User
        fields=('username','email','password1','password2')
