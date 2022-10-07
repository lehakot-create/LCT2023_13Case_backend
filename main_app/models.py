from django.db.models import Max
from django.contrib import auth
from django.contrib.auth.hashers import identify_hasher, make_password
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
# from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.utils import timezone
from django.core.mail import send_mail
from django.apps import apps
from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.indexes import GinIndex


# Create your models here.

class Status(models.Model):
    STATUSES = (
        (1, 'Phisical'),
        (2, 'Legal'),
    )

    status = models.PositiveIntegerField(choices=STATUSES, default=1,
                                         verbose_name='Статус - физическое/юридическое лицо')  # статус

    def __str__(self):
        for el in Status.STATUSES:
            if el[0] == self.status:
                return el[1]

    class Meta:
        verbose_name = 'статус'
        verbose_name_plural = 'статусы'


class Stack(models.Model):
    '''
    Таблица с технологиями
    '''

    name = models.CharField(max_length=64, verbose_name='Стек технологий')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'стек технологий'
        verbose_name_plural = 'стек технологий'


class TypeProject(models.Model):
    '''
    Тип проекта - коммерческий/некоммерческий
    '''

    PROJECT_TYPES = (
        (1, 'Commercial'),
        (2, 'Non commercial'),
    )
    type = models.PositiveIntegerField(choices=PROJECT_TYPES, default=1,
                                       verbose_name='Тип проекта - коммерческий/некоммерческий')

    def __str__(self):
        for el in TypeProject.PROJECT_TYPES:
            if el[0] == self.type:
                return el[1]

    class Meta:
        verbose_name = 'тип проекта'
        verbose_name_plural = 'типы проектов'


class Public(models.Model):
    '''
    Тип проекта - открытый/закрытый
    '''

    TYPES = (
        (1, 'Open'),
        (2, 'Close'),
    )
    public = models.PositiveIntegerField(choices=TYPES, default=1, verbose_name='Доступность проекта')

    def __str__(self):
        for el in Public.TYPES:
            if el[0] == self.public:
                return el[1]

    class Meta:
        verbose_name = 'доступность проекта'
        verbose_name_plural = 'доступность проекта'


class Direction(models.Model):
    '''
    Направление проекта (разработка, тестирование, анализ и т.д.)
    '''
    name = models.TextField(verbose_name='Направление проекта')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'направление проекта'
        verbose_name_plural = 'направления проектов'


class Rate(models.Model):
    '''
    Тариф
    '''

    RATE_TYPES = (
        (1, 'Tarif 1'),
        (2, 'Tarif 2'),
        (3, 'Tarif 3'),
    )
    description = models.PositiveIntegerField(choices=RATE_TYPES, default=1, verbose_name='Тариф')

    def __str__(self):
        for el in Rate.RATE_TYPES:
            if el[0] == self.description:
                return el[1]

    class Meta:
        verbose_name = 'тариф'
        verbose_name_plural = 'тарифы'


class Stage(models.Model):
    '''
    Стадии проекта
    '''
    stage = models.JSONField()

    def __str__(self):
        return self.stage

    class Meta:
        verbose_name = 'стадия проекта'
        verbose_name_plural = 'стадии проектов'


class Project(models.Model):
    '''
    Таблица проектов
    '''
    id_project_type = models.ForeignKey(TypeProject, on_delete=models.DO_NOTHING, verbose_name='Тип проекта', default=2)
    name = models.CharField(max_length=128, verbose_name='Название проекта')
    id_type = models.ForeignKey(Public, on_delete=models.DO_NOTHING,
                                verbose_name='Доступность проекта', default=1)  # Тип проекта (открытый/закрытый)

    # author = models.ForeignKey(Users, on_delete=models.DO_NOTHING)
    members_limit = models.IntegerField(validators=[MinValueValidator(1)],
                                        verbose_name='Максимальное количество участников', default=1)  # Максимальное количество участников
    members = models.ManyToManyField('Profile',
                                     verbose_name='Список участников', blank=True)  # Список участников. Получаем список всех участников проекта
    # direction = models.ForeignKey(Direction, on_delete=models.CASCADE, verbose_name='Направление проекта')
    description = models.TextField(verbose_name='Описание проекта', default='Описание проекта')
    deadline = models.DateField(verbose_name='Срок окончания проекта', blank=True, null=True)  # срок окончания проекта
    id_rate = models.ForeignKey(Rate, on_delete=models.DO_NOTHING, verbose_name='Тариф', default=1)  # тариф
    id_stage = models.ForeignKey(Stage, on_delete=models.DO_NOTHING, null=True, blank=True,
                                 verbose_name='Стадия проекта')
    rating = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], verbose_name='Рейтинг', default=100)
    colour = models.CharField(max_length=20, default='green')

    # def set_rating(self, rate):
    #     try:
    #         rate in range (1, 101)
    #     except ValueError('Рейтинг должен быть в диапазоне от 1 до 100') as er:
    #         return er
    #     self.rating = rate
    #     self.rating.save()

    def get_rating(self):
        return self.rating

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'проект'
        verbose_name_plural = 'проекты'
        indexes = [GinIndex(fields=['name'])]


class UserManager(BaseUserManager):
    '''
    Переопределение модели UserManager.
    Регистрация по email
    '''
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
    '''
    Таблица пользователей
    '''

    email = models.EmailField(unique=True, max_length=255)
    nick_name = models.CharField(max_length=255, blank=True)
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    id_status = models.ForeignKey(Status, default=1, on_delete=models.DO_NOTHING,
                                  verbose_name='ID статуса')  # применить
    description = models.CharField(max_length=1024, verbose_name='Описание')  # Описание
    img = models.ImageField(blank=True, null=True, verbose_name='Аватар')  # посмотреть тип картинка
    stack = models.ManyToManyField(Stack, verbose_name='Стек технологий')  # Список технологий должен
    # rating = models.ForeignKey(Project, on_delete=models.DO_NOTHING)  # Рейтинг
    telephone = models.CharField(max_length=50, verbose_name='Телефон')  # тип номер телефона

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

class Task(models.Model):
    """
    Статусы задач
    """
    STATUSES = (
        (1, 'нужно сделать'),
        (2, 'в процессе'),
        (3, 'готово'),
        (4, 'архив'),
    )

    status = models.IntegerField(choices=STATUSES, default=1)
    description = models.CharField(max_length=255, default='Описание задачи')
    profile = models.ManyToManyField(Profile)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def get_profiles(self):
        return ' '.join([str(p) for p in self.profile.all()])

    def __str__(self):
        return self.description

