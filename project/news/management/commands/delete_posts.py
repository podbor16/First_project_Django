from django.core.management.base import BaseCommand, CommandError
from news.models import Post, Category


class Command(BaseCommand):
	# показывает подсказку при вводе "python manage.py <ваша команда> --help"
	help = 'Удаляет новости в категории при подтверждении действия пользователем'
	# напоминать ли о миграциях. Если тру — то будет напоминание о том, что не сделаны все миграции (если такие есть)
	requires_migrations_checks = True

	def add_arguments(self, parser):
		parser.add_argument('category', type=str)

	def handle(self, *args, **options):
		# здесь можете писать любой код, который выполнится при вызове вашей команды
		self.stdout.readable()
		self.stdout.write(
			# спрашиваем пользователя действительно ли он хочет удалить все товары
			f'Вы действительно хотите удалить все публикации в категории {options["category"]}? yes/no')
		answer = input()  # считываем подтверждение

		if answer != 'yes':
			self.stdout.write(self.style.ERROR('Отменено'))
			return
		try:
			# в случае подтверждения действительно удаляем все товары
			category = Category.objects.get(name=options["category"])
			Post.objects.filter(category=category).delete()
			self.stdout.write(self.style.SUCCESS('Успешно удалены публикации в категории {category.name}'))
			# В случае неправильного подтверждения, говорим что в доступе отказано
		except Category.DoesNotExist:
			self.stdout.write(self.style.ERROR(f'Could not find category {options["category"]}'))