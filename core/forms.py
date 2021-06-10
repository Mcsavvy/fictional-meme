
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import AddressAndInfo, Profile


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'email', ]

    def save(self, node):
        obj = super().save(commit=False)
        obj.node = node
        obj.save()
        return obj


class AddressForm(ModelForm):
    class Meta:
        model = AddressAndInfo
        fields = ['country', 'city', 'home_street', 'phone']

    def save(self, node):
        obj = super().save(commit=False)
        obj.node = node
        obj.save()
        return obj
