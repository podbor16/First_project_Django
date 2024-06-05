from celery import shared_task
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.template.defaultfilters import truncatewords
from .models import Post, Subscriber
from django.core.mail import send_mail
from django.conf import settings


@shared_task
def after_post_create_task(pk):
	post = Post.objects.get(pk=pk)
	categories = post.category.all()
	emails = User.objects.filter(
		subscriber__category__in=categories
	).values_list('email', flat=True)

	subject = f'Новые публикации в категориях {", ".join(category.__str__() for category in categories)}'

	text_content = (
		f'Заголовок: {post.title}\n'
		f'Краткое содержание: {truncatewords(post.text, 5)}\n\n'
		f'Ссылка на товар: http://127.0.0.1:8000{post.get_absolute_url()}'
	)
	html_content = (
		f'Заголовок: {post.title}<br>'
		f'Краткое содержание: {truncatewords(post.text, 5)}<br><br>'
		f'<a href="http://127.0.0.1:8000{post.get_absolute_url()}">'
		f'Ссылка на товар</a>'
	)
	for email in emails:
		msg = EmailMultiAlternatives(subject, text_content, None, [email])
		msg.attach_alternative(html_content, "text/html")
		msg.send()


@shared_task
def new_weekly_posts():
	"""Отправка списка публикаций подписчикам"""
	one_week_ago = datetime.now() - timedelta(days=7)
	new_posts = Post.objects.filter(created_at__gte=one_week_ago)
	subscribers = Subscriber.objects.all()
	for subscriber in subscribers:
		user = subscriber.user
		category = subscriber.category
		posts_in_category = new_posts.filter(category=category)

		if posts_in_category.exists():
			post_links = '\n'.join([f"Заголовок: {post.title} \nПревью: {truncatewords(post.text, 5)}..."
									f"\n{settings.SITE_URL}{post.get_absolute_url()}" for post in posts_in_category])
			send_mail(
				f"Новые публикации в категории {category.name}",
				f'Привет, {user.username}! \n\nЗа последнюю неделю появились'
				f' новые публикации в категории "{category.name}":\n\n {post_links}\n\nПриятного чтения!',
				settings.DEFAULT_FROM_EMAIL,
				[user.email],
			)
		else:
			send_mail(
				f"Новых публикаций в категории {category.name} нет",
				"Новых публикаций нет",
				settings.DEFAULT_FROM_EMAIL,
				[user.email],
			)
