from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.template.defaultfilters import truncatewords

from .models import Post, PostCategory


@receiver(m2m_changed, sender=PostCategory)
def notify_subscribers(instance, **kwargs):
    if kwargs['action'] == 'post_add':
        categories = instance.category.all()
        emails = User.objects.filter(
            subscriptions__category__in=categories
        ).values_list('email', flat=True)

        subject = f'Новая публикация в категориях {", ".join(category.__str__() for category in categories)}'

        text_content = (
            f'Заголовок: {instance.title}\n'
            f'Краткое содержание: {truncatewords(instance.text, 5)}\n\n'
            f'Ссылка на товар: http://127.0.0.1:8000{instance.get_absolute_url()}'
        )
        html_content = (
            f'Заголовок: {instance.title}<br>'
            f'Краткое содержание: {truncatewords(instance.text, 5)}<br><br>'
            f'<a href="http://127.0.0.1:8000{instance.get_absolute_url()}">'
            f'Ссылка на товар</a>'
        )
        for email in emails:
            msg = EmailMultiAlternatives(subject, text_content, None, [email])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
