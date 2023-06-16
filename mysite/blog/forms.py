from django import forms
from django.contrib.auth.models import User


class PostForm(forms.Form):
    title = forms.CharField(max_length=100, required=True)
    title.widget = forms.Textarea(attrs={'class': 'post_form_input'})
    title.error_messages = {'required': 'Заголовок пуст', 'max_length': 'Заголовок не может быть длиннее 100 символов'}

    text = forms.CharField(required=False)
    text.widget = forms.Textarea(attrs={'class': 'post_form_input_text'})


class CommentForm(forms.Form):
    text = forms.CharField(required=True)
    text.error_messages = {'required': 'Комментарий пуст'}
    text.widget = forms.Textarea(attrs={'class': 'comment_form_input'})


class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    username.widget = forms.TextInput(attrs={'class': 'auth_form_input'})
    password = forms.CharField(required=True)
    password.widget = forms.PasswordInput(attrs={'class': 'auth_form_input'})


class RegisterForm(forms.Form):
    username = forms.CharField(required=True)
    username.widget = forms.TextInput(attrs={'class': 'auth_form_input'})
    password = forms.CharField(required=True)
    password.widget = forms.PasswordInput(attrs={'class': 'auth_form_input'})

    class Meta:
        model = User
        fields = ('username',)
