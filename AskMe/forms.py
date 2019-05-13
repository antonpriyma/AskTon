from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError

from AskMe.models import Profile


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
    class Meta:
        model = Profile
        fields = ('username','email','photo')


class CustomUserCreationForm(forms.Form):
    username = forms.CharField(label='Enter Username', min_length=4, max_length=150)
    email = forms.EmailField(label='Enter email')
    password1 = forms.CharField(label='Enter password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

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

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError("Password don't match")

        return password2

    def save(self, commit=True):
        user = Profile.objects.create_user(
            self.cleaned_data['username'],
            self.cleaned_data['email'],
            self.cleaned_data['password1']
        )
        return user
