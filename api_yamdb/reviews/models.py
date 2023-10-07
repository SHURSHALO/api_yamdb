from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Avg

from users.models import User
from .utils import check_year_availability


class Category(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='category',
        help_text='Введите категорию'
    )
    slug = models.SlugField(max_length=50, unique=True, )

    class Meta:
        verbose_name_plural = 'categories',

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=256, verbose_name='genre',
                            help_text='Введите жанр')
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        verbose_name_plural = 'genres'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=256, verbose_name='title',
                            help_text='Введите произведение')
    year = models.PositiveSmallIntegerField(
        validators=(check_year_availability,),
        help_text='Дата выхода произведения')
    category = models.ForeignKey(
        Category, null=True, on_delete=models.SET_NULL, related_name='titles'
    )
    description = models.TextField(null=True)
    genre = models.ManyToManyField(Genre, related_name='titles')

    def average_rating(self):
        reviews = self.reviews.all()
        if reviews.exists():
            return reviews.aggregate(Avg('score'))['score__avg']
        else:
            return None

    class Meta:
        verbose_name_plural = 'titles'

    def __str__(self):
        return self.name


class TitleGenre(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE,
                              related_name='title_genre')
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE,
                              related_name='title_genre')

    def str(self):
        return f"{self.title.name} - {self.genre.name}"


class Review(models.Model):
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews',
        verbose_name='title'
    )
    text = models.TextField(
        max_length=255, verbose_name='text', help_text='Введите текст'
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews'
    )
    score = models.PositiveSmallIntegerField(
        verbose_name='score',
        validators=[
            MinValueValidator(1, message='Оценка должна быть не менее 1.'),
            MaxValueValidator(10, message='Оценка должна быть не более 10.'),
        ], help_text='Введите оценку'
    )
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=('title', 'author'), name='unique_title_author'
            ),
        )
        verbose_name = 'отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return self.text[:15]


class Comment(models.Model):
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments',
        verbose_name='review'
    )
    text = models.TextField(
        max_length=255, verbose_name='text', help_text='Введите текст'
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments'
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text[:15]
