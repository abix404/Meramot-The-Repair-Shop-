from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, SellerProfile, Service, Booking
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm

CustomUser = get_user_model()


class SellerSignUpForm(UserCreationForm):
    mobile_no = forms.CharField(max_length=15)
    address = forms.CharField(widget=forms.Textarea)
    experience = forms.CharField(max_length=255)
    image = forms.ImageField()

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'mobile_no', 'address', 'experience', 'image']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_seller = True
        if commit:
            user.save()
            SellerProfile.objects.create(
                user=user,
                mobile_no=self.cleaned_data['mobile_no'],
                address=self.cleaned_data['address'],
                experience=self.cleaned_data['experience'],
                image=self.cleaned_data['image']
            )
        return user

class SellerProfileForm(forms.ModelForm):
    class Meta:
        model = SellerProfile
        fields = ['mobile_no', 'address', 'experience', 'image']
        widgets = {
                    "password": forms.PasswordInput(),
                }

class UserSignupForm(forms.ModelForm):
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"placeholder": "Password"})
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={"placeholder": "Confirm Password"})
    )

    class Meta:
        model = CustomUser
        fields = ["username", "email", "mobile_no", "password1", "password2"]
        widgets = {
            "username": forms.TextInput(attrs={"placeholder": "Username"}),
            "mobile_no": forms.TextInput(attrs={"placeholder": "Mobile Number"}),
            "first_name": forms.TextInput(attrs={"placeholder": "First Name"}),
            "last_name": forms.TextInput(attrs={"placeholder": "Last Name"}),
            "email": forms.EmailInput(attrs={"placeholder": "Email"}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match!")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])  # Hash password
        if commit:
            user.save()
        return user


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['category', 'title', 'description', 'price', 'image', 'location']

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['date', 'time_slot']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'time_slot': forms.Select(choices=[
                ("9:00 AM - 10:00 AM", "9:00 AM - 10:00 AM"),
                ("10:00 AM - 11:00 AM", "10:00 AM - 11:00 AM"),
                ("11:00 AM - 12:00 PM", "11:00 AM - 12:00 PM"),
                ("2:00 PM - 3:00 PM", "2:00 PM - 3:00 PM"),
                ("3:00 PM - 4:00 PM", "3:00 PM - 4:00 PM"),
                ("4:00 PM - 5:00 PM", "4:00 PM - 5:00 PM"),
            ], attrs={'class': 'form-control'}),
        }

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Username"})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Password"})
    )