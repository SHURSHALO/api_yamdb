from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Avg


User = get_user_model()


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
    category = models.ForeignKey(Category, null=True,
                                 on_delete=models.SET_NULL,
                                 related_name='titles')
    genre = models.ManyToManyField(Genre, related_name='titles')
    year = models.PositiveIntegerField()
    description = models.TextField(null=True)

    def average_rating(self):
        reviews = self.reviews.all()
        if reviews:
            return reviews.aggregate(Avg('score'))['score__avg']
        else:
            return None

    def __str__(self):
        return self.name


class Review(models.Model):

    title = models.ForeignKey(Title, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews'
    )
    score = models.PositiveIntegerField('Оценка', validators=[
        MinValueValidator(1, message='Оценка должна быть не менее 1.'),
        MaxValueValidator(10, message='Оценка должна быть не более 10.')
    ])
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    def __str__(self):
        return self.text[:15]


class Comment(models.Model):

    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments'
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    def __str__(self):
        return self.text[:15]

