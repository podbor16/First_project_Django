from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver

from .models import Post, PostCategory
from .tasks import after_post_create_task


@receiver(m2m_changed, sender=PostCategory)
def notify_subscribers(instance, **kwargs):
	if kwargs['action'] == 'post_add':
		after_post_create_task.delay(instance.pk)
