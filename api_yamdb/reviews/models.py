from django.db import models

from users.models import User


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


class Review(models.Model):
    text = models.TextField()
    #score = models.IntegerChoices('Score', '1 2 3 4 5 6 7 8 9 10')
    score = models.IntegerField()
    title = models.ForeignKey(
        Titles,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
    )

    def __str__(self):
        return self.text


class Comment(models.Model):
    text = models.TextField()
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True,
    )

    def __str__(self):
        return self.text

