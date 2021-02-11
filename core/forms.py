from core.models import Question, Test
from django import forms
from django.forms import formset_factory


class ProfileForm(forms.Form):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    birthday = forms.DateField()
    about_me = forms.CharField(max_length=1000)
    profile_img = forms.ImageField(required=False)


class CommentForm(forms.Form):
    test_id = forms.IntegerField()
    text = forms.CharField()


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        exclude = ('test', )

QuestionFormSet = formset_factory(QuestionForm, min_num=5)


class TestForm(forms.ModelForm):
    class Meta:
        model = Test
        exclude = ('passes', 'state', )

