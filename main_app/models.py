from django.db.models import Max
from django.contrib import auth
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.utils import timezone
from django.core.mail import send_mail
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    """
    Переопределение модели UserManager.
    Регистрация по email
    """
    use_in_migrations = True

    def _create_user(self, email=None, password=None, **extra_fields):
        if not email:
            raise ValueError('Необходимо ввести email адрес')
        if not password:
            raise ValueError('Необходимо ввести пароль')
        email = self.normalize_email(email)

        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        if not extra_fields.get('nick_name'):
            extra_fields.setdefault('nick_name', self.get_nick_name())
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)

    @staticmethod
    def get_nick_name():
        return "User" + str(int(Profile.objects.aggregate(Max('pk')).get('pk__max')) + 1)

    def with_perm(self, perm, is_active=True, include_superusers=True, backend=None, obj=None):
        if backend is None:
            backends = auth._get_backends(return_tuples=True)
            if len(backends) == 1:
                backend, _ = backends[0]
            else:
                raise ValueError(
                    'You have multiple authentication backends configured and '
                    'therefore must provide the `backend` argument.'
                )
        elif not isinstance(backend, str):
            raise TypeError(
                'backend must be a dotted import path string (got %r).'
                % backend
            )
        else:
            backend = auth.load_backend(backend)
        if hasattr(backend, 'with_perm'):
            return backend.with_perm(
                perm,
                is_active=is_active,
                include_superusers=include_superusers,
                obj=obj,
            )
        return self.none()


class Profile(AbstractBaseUser, PermissionsMixin):
    """
    Таблица пользователей
    """
    email = models.EmailField(unique=True, max_length=255)
    nick_name = models.CharField(max_length=255, blank=True)
    full_name = models.CharField(max_length=255, blank=True)
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    dateofbirth = models.CharField(max_length=10, blank=True)
    country = models.CharField(max_length=64, blank=True)
    citizenship = models.CharField(max_length=64, blank=True)
    agreement = models.BooleanField(default=False)
    gender = models.CharField(max_length=100, blank=True)
    education = models.CharField(max_length=256, blank=True, verbose_name='Образование')
    employment = models.CharField(max_length=256, blank=True, verbose_name='Занятость')
    experience = models.CharField(max_length=256, blank=True, verbose_name='Опыт')
    achievements = models.CharField(max_length=256, blank=True, verbose_name='Достижения')
    profession = models.CharField(max_length=128, blank=True, verbose_name='Направление')
    stack = models.CharField(max_length=128, blank=True, verbose_name='Навыки')
    role_in_command = models.CharField(max_length=128, blank=True)
    command = models.CharField(max_length=100, blank=True, verbose_name='Наличие команды')

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    user = 'US'
    moderator = "MO"
    choice = [
        (user, 'Пользователь'),
        (moderator, 'Администратор')
    ]
    role = models.CharField(max_length=2, choices=choice, default=user)
    status = models.CharField(max_length=64, blank=True, verbose_name='Готовность участия в проектах')

    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    img = models.ImageField(blank=True, null=True, verbose_name='Аватар')  # посмотреть тип картинка

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nick_name']

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    '''
    процедура создания списка стеков, т.к. при соедниении manytomany, мы получаем список записей
    '''

    def get_stacks(self):
        return ' '.join([str(s) for s in self.stack.all()])

    def __str__(self):
        return self.nick_name

    class Meta:
        verbose_name = 'профиль'
        verbose_name_plural = 'профили пользователей'
