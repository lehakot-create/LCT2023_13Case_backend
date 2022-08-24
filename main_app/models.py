from django.contrib.auth.hashers import identify_hasher, make_password
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

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


# Таблица с технологиями
class Stack(models.Model):
    name = models.CharField(max_length=64, verbose_name='Стек технологий')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'стек технологий'
        verbose_name_plural = 'стек технологий'


# Тип проекта - коммерческий/некоммерческий
class TypeProject(models.Model):
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


# Тип проекта - открытый/закрытый
class Public(models.Model):
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


# Направление проекта (разработка, тестирование, анализ и т.д.)
class Direction(models.Model):
    name = models.CharField(max_length=64, verbose_name='Направление проекта')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'направление проекта'
        verbose_name_plural = 'направления проектов'

# Тариф
class Rate(models.Model):
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

# Стадии проекта
class Stage(models.Model):
    stage = models.JSONField()

    def __str__(self):
        return self.stage

    class Meta:
        verbose_name = 'стадия проекта'
        verbose_name_plural = 'стадии проектов'

# Таблица проектов
class Project(models.Model):
    id_project_type = models.ForeignKey(TypeProject, on_delete=models.DO_NOTHING, verbose_name='Тип проекта')
    name = models.CharField(max_length=128, verbose_name='Название проекта')
    id_type = models.ForeignKey(Public, on_delete=models.DO_NOTHING,
                                verbose_name='Доступность проекта')  # Тип проекта (открытый/закрытый)
    # author = models.ForeignKey(Users, on_delete=models.DO_NOTHING)
    members_limit = models.IntegerField(validators=[MinValueValidator(1)],
                                        verbose_name='Максимальное количество участников')  # Максимальное количество участников
    members = models.ManyToManyField('Profile',
                                     verbose_name='Список участников')  # Список участников. Получаем список всех участников проекта
    direction = models.ForeignKey(Direction, on_delete=models.CASCADE, verbose_name='Направление проекта')
    deadline = models.DateField(verbose_name='Срок окончания проекта')  # срок окончания проекта
    id_rate = models.ForeignKey(Rate, on_delete=models.DO_NOTHING, verbose_name='Тариф')  # тариф
    id_stage = models.ForeignKey(Stage, on_delete=models.DO_NOTHING, null=True, blank=True,
                                 verbose_name='Стадия проекта')
    rating = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], verbose_name='Рейтинг')

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

# Таблица пользователей
class Profile(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


    id_status = models.ForeignKey(Status, default=1, on_delete=models.DO_NOTHING,
                                  verbose_name='ID статуса')  # применить
    description = models.CharField(max_length=1024, verbose_name='Описание')  # Описание
    img = models.ImageField(blank=True, null=True, verbose_name='Аватар')  # посмотреть тип картинка
    stack = models.ManyToManyField(Stack, verbose_name='Стек технологий')  # Список технологий должен
    # rating = models.ForeignKey(Project, on_delete=models.DO_NOTHING)  # Рейтинг
    telephone = models.CharField(max_length=50, verbose_name='Телефон')  # тип номер телефона


    """
    процедура создания списка стеков, т.к. при соедниении manytomany, мы получаем список записей
    """

    def get_stacks(self):
        return ' '.join([str(s) for s in self.stack.all()])

    def __str__(self):
        return self.username

    """
    процедура проверки пароля на хешированность перед сохранением
    """

    def save(self, *args, **kwargs):
        try:
            _alg = identify_hasher(self.password)
        except ValueError:
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'профиль'
        verbose_name_plural = 'профили пользователей'
    # нужно добавить две функции чтобы создавался профиль пользователя при создании юзера. Это если первый путь выберешь
