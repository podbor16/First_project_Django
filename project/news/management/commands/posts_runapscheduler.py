import logging
from datetime import datetime, timedelta

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.conf import settings
from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django_apscheduler import util
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from news.models import Post, Category, Subscriber

logger = logging.getLogger(__name__)


def send_weekly_post_email():
    """Отправка списка публикаций подписчикам"""
    one_week_ago = datetime.now() - timedelta(days=7)
    new_posts = Post.objects.filter(created_at__gte=one_week_ago)
    subscribers = Subscriber.objects.all()
    for subscriber in subscribers:
        user = subscriber.user
        category = subscriber.category
        posts_in_category = new_posts.filter(category=category)

        if posts_in_category.exists():
            post_links = '\n'.join([f"{post.title} - {settings.SITE_URL}"
                                    f"{post.get_absolute_url}" for post in posts_in_category])
            send_mail(
                f"Новые публикации в категории {category.name}",
                post_links,
                settings.DEFAULT_FROM_EMAIL,
                [subscriber.email],
            )
        else:
            send_mail(
                f"Новых публикаций в категории {category.name} нет",
                "Новых публикаций нет",
                settings.DEFAULT_FROM_EMAIL,
                [subscriber.email],
            )


@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    """Удаление старых записей о выполнении задач"""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            send_weekly_post_email,
            trigger=CronTrigger(day_of_week="fri", hour="18", minute="00"),
            id="send_weekly_post_email",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added weekly job: 'send_weekly_article_email'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added weekly job: 'delete_old_job_executions'.")

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
