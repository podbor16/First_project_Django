from django import template
from django.template.base import TemplateSyntaxError

register = template.Library()


@register.filter()
def censor_words(value, args='урюпа,фофанъ,фуфлыга,хабалъ,баламошка,пентюх,брыблый,баляба'):
	"""Фильтр для цензурирования слов в тексте."""
	if not isinstance(value, str):
		raise TemplateSyntaxError("Filter 'censor_words' should only be applied to string variables.")
	# Разделяем входную строку по пробелам и преобразуем в множество для уникальности
	value_words = value.split()
	# Преобразуем аргументы в множество для уникальности
	#args_words = set(args.split(','))
	args_words = [word.lower() for word in args.split(',')]

	# Создаем новый список слов, где каждое слово из args заменяется на '*', кроме 1 и последней буквы
	censored_words = [
		word if word.lower() not in args_words else word[0] + '*' * (len(word) - 2) + word[-1]
		for word in value_words
	]

	# Возвращаем результат в виде строки
	return ' '.join(censored_words)
	#return str(censored_words)
