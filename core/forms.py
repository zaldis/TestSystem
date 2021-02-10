from django import forms


class ProfileForm(forms.Form):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    birthday = forms.DateField()
    about_me = forms.CharField(max_length=1000)
    profile_img = forms.ImageField(required=False)


class CommentForm(forms.Form):
    test_id = forms.IntegerField()
    text = forms.CharField()
