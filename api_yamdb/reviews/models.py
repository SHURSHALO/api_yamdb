from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Avg


class User(AbstractUser):
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'
    ROLES = [
        (USER, USER),
        (ADMIN, ADMIN),
        (MODERATOR, MODERATOR),
    ]

    username = models.CharField(max_length=150,
                                unique=True,
                                blank=False,
                                null=False,
                                )
    email = models.EmailField(max_length=254,
                              unique=True,
                              blank=False,
                              null=False,
                              )
    role = models.CharField('роль',
                            max_length=20,
                            choices=ROLES,
                            default=USER,
                            blank=True,
                            )
    bio = models.TextField('биография',
                           blank=True,
                           )
    first_name = models.CharField('Имя',
                                  max_length=150,
                                  blank=True,
                                  )
    last_name = models.CharField('Фамилия',
                                 max_length=150,
                                 blank=True,
                                 )
    confirmation_code = models.CharField('Код подтверждения',
                                         max_length=260,
                                         null=True,
                                         blank=False,
                                         default='AAAA'
                                         )
    
    @property
    def is_user(self):
        return self.role == self.USER
    
    @property
    def is_admin(self):
        return self.role == self.ADMIN
    
    @property
    def is_moderator(self):
        return self.role == self.MODERATOR
    
    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username

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
