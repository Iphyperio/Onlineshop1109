from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.forms import TextInput, EmailInput, FileInput, Select


class RegistrationForm(UserCreationForm):
    username= forms.CharField(max_length=30, label='Username: ')
    email = forms.EmailField(max_length=200, label='Email:')
    first_name = forms.CharField(max_length=150, label='First name: ')
    last_name = forms.CharField(max_length=150, label='Last name: ')

    class Meta:
        model = User
        fields = ['username','email','first_name','last_name','password1','password2']

class UserUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['username','email','first_name','last_name']
        widgets = { 'username': TextInput({'class':'input',
                                           'placeholder':'username'}),
                    'email': EmailInput({'class': 'input',
                                           'placeholder': 'email'}),
                    'first_name': TextInput({'class': 'input',
                                           'placeholder': 'First name'}),
                    'last_name': TextInput({'class': 'input',
                                           'placeholder': 'Last name'}),
        }


from .models import UserProfile
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        CITY = [('Astana', 'Astana'),
                ('Moscow', 'Moscow'),
                ('Ankara', 'Ankara')]
        model = UserProfile
        fields = ['phone','address','city','country','image']
        widgets = { 'phone': TextInput({'class':'input',
                                           'placeholder':'phone number'}),
                    'address': TextInput({'class': 'input',
                                           'placeholder': 'address'}),
                    'city': Select({'class': 'input',
                                           'placeholder': 'city'},
                                   choices=CITY),
                    'country': TextInput({'class': 'input',
                                           'placeholder': 'country'}),
                    'image': FileInput({'class': 'input',
                                           'placeholder': 'image'})
        }
