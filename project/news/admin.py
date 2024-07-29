from django.contrib import admin
from .models import (
	Author, Category, Post, PostCategory, Comment,
	Subscriber, MyModel
)

# импортируем модель амдинки (вспоминаем модуль про переопределение стандартных админ-инструментов)
from modeltranslation.admin import TranslationAdmin


class CategoryAdmin(TranslationAdmin):
	model = Category


class MyModelAdmin(TranslationAdmin):
	model = MyModel


class PostAdmin(TranslationAdmin):
	model = Post


admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Post)
admin.site.register(PostCategory)
admin.site.register(Comment)
admin.site.register(Subscriber)
admin.site.register(MyModel)
