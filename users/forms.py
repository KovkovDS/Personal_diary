from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, SetPasswordForm, PasswordResetForm
from .models import User
from django_countries.widgets import CountrySelectWidget


class UserRegistrationForm(UserCreationForm):
    """Класс формы создания объекта модели "Пользователь"."""
    class Meta(UserCreationForm.Meta):
        """Класс для изменения поведения полей формы модели "Пользователь"."""
        model = User
        fields = ('email', 'avatar', 'first_name', 'last_name', 'phone_number', 'country', 'password1', 'password2')
        widgets = {"country": CountrySelectWidget(layout='{widget}<img class="country-select-flag" id="{flag_id}" '
                                                         'style="margin: 3px 4px 6px; width: 2.5%; height: 2.5%" '
                                                         'class="me-auto flex-shrink-1" '
                                                         'src="{country.flag}">')}

    def clean_email(self):
        """Метод проверки поля "Адрес электронной почты" формы модели "Пользователь"."""
        email = self.cleaned_data.get('email')
        if '@' not in email:
            raise forms.ValidationError('Некорректный адрес электронной почты. Пожалуйста введите корректные данные.')
        return email

    def clean_phone_number(self):
        """Метод проверки поля "Номер телефона" формы модели "Пользователь"."""
        phone_number = self.cleaned_data.get('phone_number')
        if phone_number and not phone_number.isdigit():
            raise forms.ValidationError('Номер телефона должен состоять только из цифр.')
        return phone_number

    def __init__(self, *args, **kwargs):
        """Инициализирует поля формы"""
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Введите ваш E-mail'})
        self.fields['avatar'].widget.attrs.update({'class': 'form-control', 'type': 'file', 'id': 'formFile',
                                                   'label': 'Фото профиля'})
        self.fields['first_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Введите ваше имя'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Введите вашу фамилию'})
        self.fields['phone_number'].widget.attrs.update({'class': 'form-control',
                                                         'placeholder': 'Введите ваш номер телефона',
                                                         'label': 'Номер телефона'})
        self.fields['country'].widget.attrs.update({'class': 'form-select', 'placeholder': 'Выберите страну',
                                                    'style': 'width: 90%'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Введите пароль'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Введите пароль для '
                                                                                              'подтверждения'})


class UserUpdateForm(UserCreationForm):
    """Класс формы обновления объекта модели "Пользователь"."""
    class Meta(UserCreationForm.Meta):
        """Класс для изменения поведения полей формы модели "Пользователь"."""
        model = User
        fields = ('email', 'avatar', 'first_name', 'last_name', 'phone_number', 'country')
        widgets = {"country": CountrySelectWidget(layout='{widget}<img class="country-select-flag" id="{flag_id}" '
                                                         'style="margin: 3px 4px 6px; width: 2.5%; height: 2.5%" '
                                                         'class="me-auto flex-shrink-1" '
                                                         'src="{country.flag}">')}

    def clean_email(self):
        """Метод проверки поля "Адрес электронной почты" формы модели "Пользователь"."""
        email = self.cleaned_data.get('email')
        if '@' not in email:
            raise forms.ValidationError('Некорректный адрес электронной почты. Пожалуйста введите корректные данные.')
        return email

    def clean_phone_number(self):
        """Метод проверки поля "Номер телефона" формы модели "Пользователь"."""
        phone_number = self.cleaned_data.get('phone_number')
        if phone_number and not phone_number.isdigit():
            raise forms.ValidationError('Номер телефона должен состоять только из цифр.')
        return phone_number

    def __init__(self, *args, **kwargs):
        """Инициализирует поля формы"""
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Введите ваш E-mail'})
        self.fields['avatar'].widget.attrs.update({'class': 'form-control', 'type': 'file', 'id': 'formFile',
                                                   'label': 'Фото профиля'})
        self.fields['first_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Введите ваше имя'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Введите вашу фамилию'})
        self.fields['phone_number'].widget.attrs.update({'class': 'form-control',
                                                         'placeholder': 'Введите ваш номер телефона',
                                                         'label': 'Номер телефона'})
        self.fields['country'].widget.attrs.update({'class': 'form-select', 'placeholder': 'Выберите страну',
                                                    'style': 'width: 90%'})


class UserAuthorizationForm(AuthenticationForm):
    """Класс формы авторизации пользователя."""
    class Meta(AuthenticationForm):
        """Класс для изменения поведения полей формы модели "Пользователь"."""
        fields = ('email', 'password')

    def __init__(self, *args, **kwargs):
        """Инициализируем поля формы."""
        super(UserAuthorizationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Введите ваш E-mail'})
        self.fields['password'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Введите пароль'})


class ProfilePasswordResetForm(PasswordResetForm):
    """Форма запроса на восстановление пароля."""

    def __init__(self, *args, **kwargs):
        """Инициализируем поля формы."""
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control", "autocomplete": "off"})


class ProfileChangingPasswordForm(SetPasswordForm):
    """Форма изменения пароля пользователя после подтверждения."""

    def __init__(self, *args, **kwargs):
        """Инициализируем поля формы."""
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control", "autocomplete": "off"})


class ProfilePasswordRecoveryForm(forms.Form):
    """Форма восстановления пароля пользователя."""
    email = forms.EmailField(label="Укажите Email")

    def clean_email(self):
        """Проверка email на уникальность."""
        email = self.cleaned_data.get("email")
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("Такого email нет в системе")
        return email
