from django import forms


class RegistrationForm(forms.Form):
    email = forms.EmailField(label='Input your email')
    password = forms.CharField(widget=forms.PasswordInput())


class SignInForm(forms.Form):
    email = forms.EmailField(label='Input your email')
    password = forms.CharField(widget=forms.PasswordInput())


class PostForm(forms.Form):
    photo = forms.ImageField(label='Load photo')
    title = forms.CharField(max_length=100, label='Title of your post')
    description = forms.CharField(max_length=200, label='Description')
