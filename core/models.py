from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE


class UserDetail(models.Model):
    user = models.OneToOneField(User, on_delete=CASCADE)
    birthday = models.DateField(blank=True, null=True)
    profile_img = models.ImageField(upload_to='profile', blank=True, null=True)
    about_me = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Details of [{self.user.username}]"


class Test(models.Model):

    class TestState(models.TextChoices):
        CREATING = 'A', 'Creating'
        CREATED = 'Z', 'Created'

    title = models.CharField(max_length=100)
    description = models.TextField()
    passes = models.PositiveIntegerField(default=0)
    creation_date = models.DateTimeField(auto_now=True)
    state = models.CharField(max_length=100, choices=TestState.choices, default=TestState.CREATING)

    def __str__(self):
        return f"{self.title}: {self.passes}"


class TestResult(models.Model):
    user_detail = models.ForeignKey(UserDetail, on_delete=CASCADE)
    test = models.ForeignKey(Test, on_delete=CASCADE)
    total = models.PositiveIntegerField()
    corrects = models.PositiveIntegerField()
    passed_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_detail.user}| {self.test.title}| {self.corrects}/{self.total}"


class Question(models.Model):
    test = models.ForeignKey(Test, on_delete=CASCADE)
    question = models.TextField()

    def __str__(self):
        return f"{self.test}: {self.question}"


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=CASCADE)
    text = models.TextField()
    is_correct = models.BooleanField(default=False)

    class Meta:
        unique_together = ('question', 'text')

    def __str__(self):
        return f"{self.question}: {self.text}"


class Comment(models.Model):
    test = models.ForeignKey(Test, on_delete=CASCADE)
    text = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.test.title}: {self.creation_date}"
