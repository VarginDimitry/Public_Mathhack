from datetime import date
from django.urls import reverse
from django.db import models

from django.contrib.auth.models import User

from django.db.models.signals import post_save
from django.dispatch import receiver


class Author(models.Model):
    """Автор варианта или заданий"""
    name = models.CharField("Название или Имя", max_length=50)
    link = models.TextField("Ссылка на автора", max_length=130, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('actor_detail', kwargs={"slug": self.name})

    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"


class Task(models.Model):
    """Задания"""
    type = models.IntegerField("Тип")
    text = models.TextField("Текст задания")
    image = models.ImageField("Изображение", upload_to="tasks/", blank=True)
    ful_answer = models.TextField("Развернутый ответ", max_length=1000, default="", blank=True)
    answer = models.TextField("Ответ", max_length=60, default="", blank=True)
    author = models.ManyToManyField(Author, verbose_name="Автор", related_name="task_author")
    date = models.DateTimeField("Дата добавления", auto_now=True)
    url = models.SlugField(max_length=130, unique=True)

    def __str__(self):
        return f'id: {self.id} - {self.type}'

    class Meta:
        verbose_name = "Задание"
        verbose_name_plural = "Задания"


class Variant(models.Model):
    """Варианты"""

    num = models.IntegerField("Номер варианта")
    tasks = models.ManyToManyField(Task, verbose_name='Задание', related_name='variant_task')
    author = models.ManyToManyField(Author, verbose_name="Автор", related_name="variant_author")
    date = models.DateTimeField("Дата добавления", auto_now=True)
    url = models.SlugField(max_length=130, unique=True)

    def __str__(self):
        return f'id: {self.id} - {self.num}'

    class Meta:
        verbose_name = "Варинт"
        verbose_name_plural = "Варианты"


class SolvingVariant(models.Model):
    """Решение варианта"""

    variant = models.ManyToManyField(Variant, verbose_name='Вариант', related_name='solved_variant')

    task1 = models.CharField(max_length=20, blank=True)
    task2 = models.CharField(max_length=20, blank=True)
    task3 = models.CharField(max_length=20, blank=True)
    task4 = models.CharField(max_length=20, blank=True)
    task5 = models.CharField(max_length=20, blank=True)
    task6 = models.CharField(max_length=20, blank=True)
    task7 = models.CharField(max_length=20, blank=True)
    task8 = models.CharField(max_length=20, blank=True)
    task9 = models.CharField(max_length=20, blank=True)
    task10 = models.CharField(max_length=20, blank=True)
    task11 = models.CharField(max_length=20, blank=True)
    task12 = models.CharField(max_length=20, blank=True)

    task13 = models.CharField(max_length=1, blank=True)
    task14 = models.CharField(max_length=1, blank=True)
    task15 = models.CharField(max_length=1, blank=True)
    task16 = models.CharField(max_length=1, blank=True)
    task17 = models.CharField(max_length=1, blank=True)
    task18 = models.CharField(max_length=1, blank=True)
    task19 = models.CharField(max_length=1, blank=True)

    solving_str = models.CharField("Перечисление + и -", max_length=19, blank=True)
    total = models.CharField('Итог', max_length=2, blank=True)
    date = models.DateTimeField("Дата решения", auto_now=True)

    def __str__(self):
        return f'{self.date.hour}:{self.date.minute} {self.date.day}.{self.date.month}.{self.date.year} - {self.solving_str}'

    class Meta:
        verbose_name = "Решение варианта"
        verbose_name_plural = "Решения вариантов"


class ChangeUserModel(models.Model):
    """Change User"""

    change_username = models.CharField("Изменить имя", max_length=30, blank=True)
    change_grade = models.CharField("Изменить класс", max_length=2, blank=True)
    change_user_image = models.ImageField(upload_to='user_images/', blank=True)

    date = models.DateTimeField("Дата добавления", auto_now=True)

    def __str__(self):
        return f'{self.change_username} - {date.day}.{date.month}.{date.year}'

    class Meta:
        verbose_name = "Изменение пользователя"
        verbose_name_plural = "Изменения пользователей"


class Customer(models.Model):
    """Custom User"""
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    user_image = models.ImageField(upload_to='user_images/',
                                   default='user_images/None_user.jpg')
    grade = models.CharField("Класс", max_length=2, default='11')

    points_sum = models.IntegerField("Общее число баллов", default=0)
    points_num = models.IntegerField("Колличество решенных вариантов", default=0)

    solved_variants = models.ManyToManyField(SolvingVariant, verbose_name="Решенный вариант",
                                             related_name="solved_variant", blank=True)

    user_changes = models.ManyToManyField(ChangeUserModel, verbose_name="Изменение пользователя",
                                          related_name='user_change', blank=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "Пользователь++"
        verbose_name_plural = "Пользователи++"

