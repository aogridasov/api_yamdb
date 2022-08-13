from django.db import models


class Category(models.Model):
    name = models.CharField('Название категории', max_length=200)
    slug = models.SlugField('Слаг', unique=True)

    def __str__(self) -> str:
        return self.name


class Genres(models.Model):
    name = models.CharField('Название жанра', max_length=200)
    slug = models.SlugField('Слаг', unique=True)

    def __str__(self) -> str:
        return self.name


class Titles(models.Model):
    name = models.CharField('Название произведения', max_length=200)
    year = models.DateTimeField('Год выхода', auto_now_add=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='category'
    )

    def __str__(self) -> str:
        return self.name
