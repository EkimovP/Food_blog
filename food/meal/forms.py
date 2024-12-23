from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from captcha.fields import CaptchaField, CaptchaTextInput
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import *


class AddPostForm(forms.ModelForm):
    def __init__(self, *arg, **kwargs):
        super().__init__(*arg, **kwargs)
        self.fields['cat'].empty_label = "Категория не выбрана"

    class Meta:
        model = Food
        fields = ['title', 'slug', 'cat', 'content', 'photo', 'is_published']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control',
                                            'placeholder': 'Название блюда'}),
            'slug': forms.TextInput(attrs={'class': 'form-control',
                                           'placeholder': 'Заполниться автоматически, можно редактировать'}),
            'content': forms.Textarea(attrs={'class': 'form-control',
                                             'type': 'text',
                                             'rows': 5,
                                             'placeholder': 'Любая информация о блюде'}),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'cat': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 250:
            raise ValidationError('Длина превышает 250 символов.')

        return title


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин',
                               widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'placeholder': 'User'}))
    email = forms.EmailField(label='Email',
                             widget=forms.EmailInput(attrs={'class': 'form-control',
                                                            'placeholder': 'User@example.com'}))
    password1 = forms.CharField(label='Пароль',
                                widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                  'placeholder': 'Password'}))
    password2 = forms.CharField(label='Повтор пароля',
                                widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                  'placeholder': 'Password'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Пользователь с таким email уже зарегистрирован.")

        return email


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин',
                               widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'placeholder': 'User'}))
    password = forms.CharField(label='Пароль',
                               widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                 'placeholder': 'Password'}))


class ContactForm(forms.Form):
    name = forms.CharField(label='Имя', max_length=255,
                           widget=forms.TextInput(attrs={'class': 'form-control',
                                                         'placeholder': 'Ваше имя'}))
    email = forms.CharField(label='Email',
                            widget=forms.EmailInput(attrs={'class': 'form-control',
                                                           'placeholder': 'Почта для связи'}))
    content = forms.CharField(label='Информация',
                              widget=forms.Textarea(attrs={'class': 'form-control',
                                                           'type': 'text',
                                                           'rows': 5,
                                                           'placeholder': 'Любая информация'}))
    # графическая картинка с кодом
    captcha = CaptchaField(label='Введите текст с картинки',
                           widget=CaptchaTextInput(attrs={'class': 'form-control',
                                                          'placeholder': 'Введите текст с картинки'}))
