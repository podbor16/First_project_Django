from django import forms
from .models import Post
from django.core.exceptions import ValidationError


class NewsForm(forms.ModelForm):
	text = forms.CharField(min_length=20)

	class Meta:
		model = Post
		fields = [
			'author',
			'category',
			'title',
			'text',
			'rating'
		]

	def clean(self):
		cleaned_data = super().clean()
		text = cleaned_data.get('text')
		title = cleaned_data.get('title')
		if title == text:
			raise ValidationError('Текст должен отличаться от заголовка')
		return cleaned_data


class ArticleForm(forms.ModelForm):
	text = forms.CharField(min_length=20)

	class Meta:
		model = Post
		fields = [
			'author',
			'category',
			'title',
			'text',
			'rating'
		]

	def clean(self):
		cleaned_data = super().clean()
		text = cleaned_data.get('text')
		title = cleaned_data.get('title')
		if title == text:
			raise ValidationError('Текст должен отличаться от заголовка')
		return cleaned_data
