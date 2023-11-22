# accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser 

class SignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')
    def clean_username(self):
        username = self.cleaned_data['username']
        # Check if the username contains spaces
        if ' ' in username:
            raise forms.ValidationError("Username cannot contain spaces.")
        return username
# class OTPVerificationForm(forms.Form):
#     otp = forms.CharField(max_length=6, widget=forms.TextInput(attrs={'placeholder': 'Enter OTP'}))
#     class Meta:
#         model = OTPDevice
    
        