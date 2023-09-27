from django.contrib import admin

from .models import Title, Category, Genre


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ('name', 'category',)
    search_fields = ('name',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)
