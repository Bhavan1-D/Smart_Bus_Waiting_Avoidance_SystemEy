from django import forms
from django.contrib.auth.models import User
from .models import Student, Driver

# ================= USER FORM =================
class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


# ================= STUDENT FORM =================

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['regno', 'name', 'email']

 
# ================= DRIVER FORM =================
class DriverForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ['mobile', 'bus_no']


# ================= FEEDBACK FORM =================
#class FeedbackForm(forms.ModelForm):
    #class Meta:
     #   model = Feedback
     #   fields = ['rating', 'message']
