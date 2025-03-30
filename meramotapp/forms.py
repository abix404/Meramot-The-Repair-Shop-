from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, SellerProfile



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


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
    mobile_no = forms.CharField(max_length=15, required=True, widget=forms.TextInput(attrs={'placeholder': 'Mobile No'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    is_seller = forms.BooleanField(required=False, widget=forms.CheckboxInput())

    class Meta:
        model = CustomUser
        fields = ("first_name", "last_name", "mobile_no", "email", "password1", "password2", "is_seller")

class UserSignupForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name", "email", "mobile_no", "password1", "password2"]