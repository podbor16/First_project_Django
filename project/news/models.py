from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.cache import cache


# Create your models here.
class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        self.rating = (sum(post.rating * 3 for post in self.post_set.all()) +
                       sum(comment.rating for comment in self.user.comment_set.all()) +
                       sum(comment.rating for post in self.post_set.all() for comment in post.comment_set.all()))
        self.save()

    def __str__(self):
        return self.user.username


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    TYPE_CHOICES = [
        ('article', 'Статья'),
        ('news', 'Новость'),
    ]

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=200)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    def preview(self):
        return (self.text[:124] + '...') if len(self.text) > 124 else self.text

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self, rating):
        self.rating -= 1 if rating > 0 else self.rating
        self.save()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])

    def save(self,  *args, **kwargs):
        # Сначала вызываем метод родителя, чтобы объект сохранился
        super().save(*args, **kwargs)
        # Затем удаляем его из кэша, чтобы сбросить его
        cache.delete(f'post-{self.pk}')


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.post.title}: {self.category.name}'


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self, rating):
        self.rating -= 1 if rating > 0 else self.rating
        self.save()


class Subscriber(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='subscriber',
    )
    category = models.ForeignKey(
        to='Category',
        on_delete=models.CASCADE,
        related_name='subscriber',
    )

    def __str__(self):
        return f'{self.user.username} - {self.category.name}'