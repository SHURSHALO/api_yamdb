from django.db import models
from django.db.models import Avg

from users.models import User
from reviews.utils import check_year_availability, check_score


class Category(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Категория',
        help_text='Введите категорию'
    )
    slug = models.SlugField(max_length=50, unique=True,
                            verbose_name='Слаг категории',
                            help_text='Введите слаг для категории')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории',

    def __str__(self):
        return self.name[:15]


class Genre(models.Model):
    name = models.CharField(max_length=256, verbose_name='Жанр',
                            help_text='Введите жанр')
    slug = models.SlugField(max_length=50, unique=True,
                            verbose_name='Слаг жанра',
                            help_text='Введите слаг для жанра')

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name[:15]


class Title(models.Model):
    name = models.CharField(max_length=256, verbose_name='Произведение',
                            help_text='Введите название произведения')
    year = models.PositiveSmallIntegerField(
        validators=(check_year_availability,),
        help_text='Дата выхода произведения', verbose_name='Дата выхода')
    category = models.ForeignKey(
        Category, null=True, on_delete=models.SET_NULL, related_name='titles',
        verbose_name='Категория',
        help_text='Выберете категорию'
    )
    description = models.TextField(null=True, verbose_name='Описание',
                                   help_text='Введите описание')
    genre = models.ManyToManyField(Genre, related_name='titles',
                                   verbose_name='Жанр',
                                   help_text='Введите жанр')

    def average_rating(self):
        reviews = self.reviews.all()
        if reviews.exists():
            return reviews.aggregate(Avg('score'))['score__avg']
        return None

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name[:15]


class TitleGenre(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE,
                              related_name='title_genres')
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE,
                              related_name='titles_genre')

    def __str__(self):
        return f'{self.title.name} - {self.genre.name}'


class Review(models.Model):
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews',
        verbose_name='Произведение', help_text='Введите произведение'
    )
    text = models.TextField(
        max_length=255, verbose_name='Текст', help_text='Введите текст'
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews',
        verbose_name='Автор', help_text='Введите автора'
    )
    score = models.PositiveSmallIntegerField(
        verbose_name='score', validators=(check_score,),
        help_text='Введите оценку'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата публикации',
        help_text='Введите дату'
    )

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
        verbose_name='Отзыв', help_text='Введите отзыв'
    )
    text = models.TextField(
        max_length=255, verbose_name='Текст', help_text='Введите текст'
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments',
        verbose_name='Автор', help_text='Введите автора'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата публикации',
        help_text='Введите дату'
    )

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text[:15]
