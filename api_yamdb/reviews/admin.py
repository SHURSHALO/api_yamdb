from django.contrib import admin

from reviews.models import Title, Category, Genre, Review, Comment


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'category',
    )
    search_fields = ('name',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('title', 'author')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('text', 'author')
