from crispy_forms.layout import Submit, Layout, Field
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError
from crispy_forms.helper import FormHelper
from AskMe.models import Profile, Question, Answer


# TODO:валидация и сообщения об ошибках

# class ImageWithPreviewInput(forms.widgets.ClearableFileInput):
#     input_text = 'Change avatar'
#     template_name = 'widgets/image_upload.html'
#
#     def __init__(self, initial_tn = None, attrs=None):
#         super().__init__(attrs=attrs)
#         self.initial_tn = initial_tn
#
#     def get_context(self, name, value, attrs):
#         context = super().get_context(name, self.initial_tn, attrs)
#         return context

class UserChangingForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.form_method = 'POST'
    helper.label_class = 'col-sm-2'
    helper.field_class = 'col-sm-4'
    # TODO: сделать красивую загрузку картинок

    helper.layout = Layout(
        'username',
        'email',
        'photo'
    )

    class Meta:
        model = Profile
        fields = ('username', 'email', 'photo')

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        r = Profile.objects.filter(username=username)
        if r.count():
            raise ValidationError("Username already exists")
        return username

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        r = Profile.objects.filter(email=email)
        if r.count():
            raise ValidationError("Email already exists")
        return email


class QuestionUploadForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.form_method = 'POST'
    helper.label_class = 'col-sm-2'
    helper.field_class = 'col-sm-6'

    class Meta:
        model = Question
        fields = ('title', 'content', 'tags')
        labels = {
            'content': 'Text',
        }
        # TODO:placeholder


class AnswerUploadForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.form_method = 'POST'
    helper.label_class = 'col-sm-2'
    helper.field_class = 'col-sm-12 rows-3'

    # TODO: сделать красивую загрузку картинок

    class Meta:
        model = Answer
        fields = ('content',)
        labels = {
            'content': 'Text',
        }
        # TODO:placeholder


class CustomUserCreationForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.form_method = 'POST'
    helper.label_class = 'col-sm-2'
    helper.field_class = 'col-sm-6'
    password = forms.CharField(label='Enter password', widget=forms.PasswordInput)
    password_repeat = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    class Meta:
        model = Profile
        fields = ('username', 'email', 'password')

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        r = Profile.objects.filter(username=username)
        if r.count():
            raise ValidationError("Username already exists")
        return username

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        r = Profile.objects.filter(email=email)
        if r.count():
            raise ValidationError("Email already exists")
        return email

    def clean_password_repeat(self):
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data['password_repeat']
        print("pass1: " + str(password1))
        print("pass2: " + str(password2))

        if password1 and password2 and password1 != password2:
            raise ValidationError("Password don't match")

        return password1

    def save(self, commit=True):
        user = Profile.objects.create_user(
            self.cleaned_data['username'],
            self.cleaned_data['email'],
            self.cleaned_data['password_repeat']
        )
        return user


class CustomLoginForm(AuthenticationForm):
    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.form_method = 'POST'
    helper.label_class = 'col-sm-2'
    helper.field_class = 'col-sm-4'
    helper.layout = Layout(
        'username',
        'password'
    )
