from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField


# Create your models here.

class Status(models.Model):
    STATUSES = (
        (1, 'Phisical'),
        (2, 'Legal'),
    )

    status = models.PositiveIntegerField(choices=STATUSES, default=1)  # статус


# Таблица с технологиями
class Stack(models.Model):
    name = models.CharField(max_length=64)


# Таблица пользователей
class Users(models.Model):
    id_status = models.ForeignKey(Status, on_delete=models.DO_NOTHING)
    #profile = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    first_last_name = models.CharField(max_length=128)  # ФИО
    description = models.CharField(max_length=1024)  # Описание
    img = models.ImageField()  # посмотреть тип картинка
    stack = models.ManyToManyField(Stack)  # Список технологий должен
    rating = models.IntegerField()  # Рейтинг
    telephone = models.CharField(max_length=50)  # тип номер телефона
    email = models.EmailField()  # посмотреть тип email

    def set_rating(self):
        pass

    def get_rating(self):
        pass

    # нужно добавить две функции чтобы создавался профиль пользователя при создании юзера. Это если первый путь выберешь

# Тип проекта - коммерческий/некоммерческий
class TypeProject(models.Model):
    PROJECT_TYPES = (
        (1, 'Commercial'),
        (2, 'Non commercial'),
    )
    type = models.PositiveIntegerField(choices=PROJECT_TYPES, default=1)


# Тип проекта - открытый/закрытый
class Public(models.Model):
    TYPES = (
        (1, 'Open'),
        (2, 'Close'),
    )
    public = models.PositiveIntegerField(choices=TYPES, default=1)


# Направление проекта (разработка, тестирование, анализ и т.д.)
class Direction(models.Model):
    name = models.CharField(max_length=64)


# Тариф
class Rate(models.Model):
    RATE_TYPES = (
        (1, 'Tarif 1'),
        (2, 'Tarif 2'),
        (3, 'Tarif 3'),
    )
    description = models.PositiveIntegerField(choices=RATE_TYPES, default=1)


# Стадии проекта
class Stage(models.Model):
    stage = models.JSONField()


# Таблица проектов
class Project(models.Model):
    id_project_type = models.ForeignKey(TypeProject, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=128)
    id_type = models.ForeignKey(Public, on_delete=models.DO_NOTHING)  # Тип проекта (открытый/закрытый)
    # author = models.ForeignKey(Users, on_delete=models.DO_NOTHING)
    members_limit = models.IntegerField()  # Максимальное количество участников
    members = models.ManyToManyField(Users)  # Список участников. Получаем список всех участников проекта
    direction = models.ForeignKey(Direction, on_delete=models.CASCADE)
    deadline = models.DateField()  # срок окончания проекта
    id_rate = models.ForeignKey(Rate, on_delete=models.DO_NOTHING)  # тариф
    id_stage = models.ForeignKey(Stage, on_delete=models.DO_NOTHING)
    rating = models.IntegerField()

    def set_rating(self):
        pass

    def get_rating(self):
        pass
