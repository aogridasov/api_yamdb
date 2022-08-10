from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Title(models.Model):
    name = models.CharField()


class Review(models.Model):
    text = models.TextField()
    #score = models.IntegerChoices('Score', '1 2 3 4 5 6 7 8 9 10')
    score = models.IntegerField()
    title = models.ForeignKey(
        Title,
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
