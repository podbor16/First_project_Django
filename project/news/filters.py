from django_filters import FilterSet
from .models import Post


class PostFilter(FilterSet):
	class Meta:
		model = Post
		# указывваем поля для фильтрации
		fields = {
			'title': ['icontains'],
			'categories': ['icontains'],
			'created_at': ['gt']
		}
