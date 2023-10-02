from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Avg


class Category(models.Model):
    name = models.CharField(max_length=256, )
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=256)
    year = models.PositiveIntegerField()
    category = models.ForeignKey(Category, null=True,
                                 on_delete=models.SET_NULL,
                                 related_name='titles')
    description = models.TextField(null=True)
    genre = models.ManyToManyField(Genre, related_name='titles')

    def average_rating(self):
        reviews = self.reviews.all()
        if reviews:
            return reviews.aggregate(Avg('score'))['score__avg']
        else:
            return None

    def __str__(self):
        return self.name


class TitleGenre(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title.name} - {self.genre.name}"


class Review(models.Model):
    # Черновой
    text = models.CharField(max_length=255)
    author = models.CharField(max_length=100)
    score = models.PositiveIntegerField()
    pub_date = models.DateTimeField(auto_now=True)
    title = models.ForeignKey(Title, related_name='reviews',
                              on_delete=models.CASCADE)
