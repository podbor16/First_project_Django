from django_filters import FilterSet, ModelChoiceFilter, DateFilter, CharFilter
from .models import Post, Category
from django import forms


class PostFilter(FilterSet):
	date = DateFilter(
		field_name='created_at',
		widget=forms.DateInput(attrs={'type': 'date'}),
		lookup_expr='date__gte',
		label='Показ постов после выбранного дня',
	)

	category = ModelChoiceFilter(
		field_name='postcategory__category',
		queryset=Category.objects.all(),
		label='Категория',
		empty_label='Выберите категорию',
	)

	title = CharFilter(
		field_name='title',
		lookup_expr='icontains',
		label='Поиск по заголовку',
	)

	class Meta:
		model = Post
		# указывваем поля для фильтрации
		fields = {
			#'title': ['icontains'],
		}
