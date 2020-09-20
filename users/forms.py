from django import forms
from django.contrib.auth.models import User 
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from .models import Profile

class UserRegisterForm(UserCreationForm):
	alphanumeric = RegexValidator(r'^[A-Za-zא-ת]')
	numeric = RegexValidator(r'^[0-9]')
	email = forms.EmailField()
	first_name = forms.CharField(validators=[alphanumeric],help_text='רק אותיות')
	last_name = forms.CharField(validators=[alphanumeric],help_text='רק אותיות')
	phone_number = forms.CharField(label='מספר פלאפון',validators=[numeric],help_text='רק מספרים',required=True)
	class Meta:
		model = User
		fields = ['username','first_name','last_name','phone_number', 'email', 'password1', 'password2'] 

class ProfileRegisterForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone_number']

class CustomAuthenticationForm(AuthenticationForm):
	username = UsernameField(
		label='שם משתמש',
		widget=forms.TextInput(attrs={'autofocus': True})
	)

class UserUpdateForm(forms.ModelForm):
	email = forms.EmailField()

	class Meta:
		model = User
		fields = ['username','first_name','last_name', 'email'] 

class ProfileUpdateForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ['phone_number','join_meet_the_rider']