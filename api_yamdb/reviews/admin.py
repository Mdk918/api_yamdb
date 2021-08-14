from django.contrib import admin

from .models import User, Category, Genre, Title, Review

# Регистрируем модели в админке

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(Title)
admin.site.register(Review)
