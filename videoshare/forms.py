from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm

from .models import User


class UserRegistrationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email', "first_name", "last_name")
        help_texts = {
            "username": None,
        }
        
    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields["password1"].help_text = None
        self.fields["password2"].help_text = None
    
    # clean the email
    def clean_email(self):

        email = self.cleaned_data.get("email").lower()
        if not email:
            raise ValidationError("No email!")

        new_email = User.objects.filter(email=email)


        if new_email.count():
            raise ValidationError("Email already Exists!")

        return email
    
    # Clean the Username 
    def clean_username(self):
        username = self.cleaned_data.get("username").lower()
        
        if not username:
            raise ValidationError("No username!r")

        new_username = User.objects.filter(username=username)
        if new_username.count():
            raise ValidationError("Username already Exist!")
        return username

    # Clean the password and verify that they are the same
    def clean_password2(self):
        
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")


        if not password1 and password2:
            raise ValidationError("No Password!")

        if  password1 != password2:
            raise ValidationError("Passwords do not match!")
        return password2

class LoginForm(AuthenticationForm):
    pass
