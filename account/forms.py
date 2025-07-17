from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Profile


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True, 
                             widget=forms.EmailInput(attrs={"class": "input-field", "placeholder": "Your email"}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        field_attrs = {
            "username": "Username",
            "password1": "Password",
            "password2": "Repeat password",
        }
        for field, placeholder in field_attrs.items():
            self.fields[field].widget.attrs.update({"class": "input-field", "placeholder": placeholder})

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ["username", "password"]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        field_attrs = {
            "username": "Username",
            "password": "Password",
        }
        for field, placeholder in field_attrs.items():
            self.fields[field].widget.attrs.update({"class": "input-field", "placeholder": placeholder})

class ProfileEditForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    avatar = forms.ImageField(required=False, widget=forms.FileInput(attrs={"class": "file-input"}))

    class Meta:
        model = Profile
        fields = ["first_name", "last_name", "email", "bio", "avatar"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        field_attrs = {
            "first_name": "First name",
            "last_name": "Last name",
            "email": "Email",
            "bio": "Bio",
        }
        for field, placeholder in field_attrs.items():
            self.fields[field].widget.attrs.update({"class": "input-field", "placeholder": placeholder})
        
        self.fields["first_name"].initial = self.instance.user.first_name
        self.fields["last_name"].initial = self.instance.user.last_name
        self.fields["email"].initial = self.instance.user.email
        self.fields["avatar"].initial = self.instance.avatar

    def save(self, commit=True):
        profile = super().save(commit=False)
        profile.user.first_name = self.cleaned_data["first_name"]
        profile.user.last_name = self.cleaned_data["last_name"]
        profile.user.email = self.cleaned_data["email"]
        if commit:
            profile.user.save()
            profile.save()
        return profile

