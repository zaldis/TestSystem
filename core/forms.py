from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from core.models import Test
from django import forms


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=100)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise ValidationError(f'User with username {username} already exists')
        return username


class ProfileForm(forms.Form):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    birthday = forms.DateField()
    about_me = forms.CharField(max_length=1000)
    profile_img = forms.ImageField(required=False)


class CommentForm(forms.Form):
    test_id = forms.IntegerField()
    text = forms.CharField()


class TestForm(forms.ModelForm):
    class Meta:
        model = Test
        exclude = ('passes', 'state', )

