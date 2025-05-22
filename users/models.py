from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import FileExtensionValidator
from django_countries.fields import CountryField
from django.contrib.auth.models import BaseUserManager
from users.validators import validate_image_size


class UserManager(BaseUserManager):
    """Класс менеджера модели "Пользователь"."""
    def create_user(self, email, phone_number, password=None, **extra_fields):
        """Метод для создания пользователя."""
        if not email:
            raise ValueError("Адрес электронной почты должен быть указан")
        email = self.normalize_email(email)
        if not phone_number:
            raise ValueError("Телефон должен быть указан")
        phone_number = self.normalize_email(phone_number)
        user = self.model(email=email, phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Метод для создания пользователя с правами суперпользователя."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Суперпользователь должен иметь is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Суперпользователь должен иметь is_superuser=True.")
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """Класс модели "Пользователь"."""
    email = models.EmailField(unique=True, verbose_name='Адрес электронной почты')
    avatar = models.ImageField(upload_to='users/photos', null=True, blank=True, verbose_name='Фото профиля',
                               validators=[validate_image_size,
                                           FileExtensionValidator(['jpg', 'png'],
                                                                  'Расширение файла « %(extension)s » не допускается. '
                                                                  'Разрешенные расширения: %(allowed_extensions)s .'
                                                                  'Недопустимое расширение!')])
    phone_number = models.CharField(unique=True, max_length=12, verbose_name='Номер телефона')
    country = CountryField(max_length=150, blank=True, blank_label="(Выберите страну)", verbose_name='Страна')
    username = None
    token = models.CharField(max_length=150, blank=True, null=True, verbose_name='Токен для верификации')
    create_at = models.DateField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateField(auto_now=True, verbose_name='Дата последнего изменения')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        """Метод для описания человеко читаемого вида модели "Пользователь"."""
        return f'{self.email} - {self.phone_number}'

    class Meta:
        """Класс для изменения поведения полей модели "Пользователь"."""
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['email', 'last_name', 'first_name', 'phone_number', 'country', 'create_at']
        permissions = [
            ("can_block_user", "Заблокировать/разблокировать пользователя"),
        ]
