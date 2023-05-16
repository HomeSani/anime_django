from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import Form, CharField, PasswordInput, IntegerField


class SingupUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'username', 'password1', 'password2']


class LoginUserForm(Form):
    username = CharField(max_length=128)
    password = CharField(widget=PasswordInput)


class ReviewForm(Form):
    text = CharField(max_length=500)


class VoteForm(Form):
    rating = IntegerField()


class DateFilterForm(Form):
    range = CharField(max_length=12)
