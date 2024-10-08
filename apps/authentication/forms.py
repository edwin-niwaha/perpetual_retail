from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.db import transaction

from .models import Contact, Profile
from apps.customers.models import Customer


# =================================== Register  ===================================
class RegisterForm(UserCreationForm):
    # fields we want to include and customize in our form
    first_name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(
            attrs={
                "placeholder": "First Name",
                "class": "form-control",
            }
        ),
    )
    last_name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Last Name",
                "class": "form-control",
            }
        ),
    )
    username = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "form-control",
            }
        ),
    )
    email = forms.EmailField(
        required=True,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Email",
                "class": "form-control",
            }
        ),
    )
    password1 = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control",
                "data-toggle": "password",
                "id": "password",
            }
        ),
    )
    password2 = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Confirm Password",
                "class": "form-control",
                "data-toggle": "password",
                "id": "password",
            }
        ),
    )

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "password1",
            "password2",
        ]

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data.get("email")
        user.first_name = self.cleaned_data.get("first_name")
        user.last_name = self.cleaned_data.get("last_name")
        if commit:
            user.save()
            # Create a Customer instance
            Customer.objects.create(user=user)
        return user


# =================================== Login  ===================================
class LoginForm(AuthenticationForm):
    username = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "form-control",
            }
        ),
    )
    password = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control",
                "data-toggle": "password",
                "id": "password",
                "name": "password",
            }
        ),
    )
    remember_me = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = ["username", "password", "remember_me"]


# =================================== User Update  ===================================
class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    email = forms.EmailField(
        required=True, widget=forms.TextInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = User
        fields = ["username", "email"]


# =================================== Pofile Update  ===================================


class UpdateProfileForm(forms.ModelForm):
    avatar = forms.ImageField(
        widget=forms.FileInput(attrs={"class": "form-control-file"})
    )
    bio = forms.CharField(
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 3})
    )

    class Meta:
        model = Profile
        fields = ["avatar", "bio"]
        widgets = {
            "role": forms.Select(attrs={"class": "form-control", "required": True}),
        }


# =================================== Pofile Update * ===================================


class UpdateProfileAllForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ["role"]
        widgets = {
            "role": forms.Select(attrs={"class": "form-control", "required": True}),
        }


# =================================== Contact Form  ===================================
class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        exclude = ("is_valid",)
        widgets = {
            "message": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
        }

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not email:
            raise forms.ValidationError("Email field is required")
        return email

    def clean_message(self):
        message = self.cleaned_data.get("message")
        if not message:
            raise forms.ValidationError("Message field is required")
        return message
