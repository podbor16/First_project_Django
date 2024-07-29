from datetime import datetime

from django.http import HttpResponse
from django.views import View
# Импортируем класс, который говорит нам о том,
# что в этом представлении мы будем выводить список объектов из БД
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from django_filters.views import FilterView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render

from django.views.decorators.csrf import csrf_protect
from django.db.models import Exists, OuterRef
# импортируем наш кэш
from django.core.cache import cache


from .models import Post, Category, Subscriber, MyModel
from .filters import PostFilter
from .forms import NewsForm, ArticleForm

# импортируем функцию для перевода
from django.utils.translation import gettext as _


# Функция для перевода только одной строки
class Index(View):
    def get(self, request):
        # . Translators: This message appears on the home page only
        models = MyModel.objects.all()

        context = {
            'models': models,
        }

        return HttpResponse(render(request, 'index.html', context))


@login_required
def show_protected_page(request):
    pass


class PostsList(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    # Поле, которое будет использоваться для сортировки объектов
    ordering = '-created_at'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'posts.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'news'

    # Указываем количество записей на странице
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs


class PostsSearch(FilterView):
    model = Post
    ordering = 'created_at'
    filterset_class = PostFilter
    template_name = 'posts_search.html'
    context_object_name = 'news'
    paginate_by = 10


class PostDetail(DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельному товару
    model = Post
    # Используем другой шаблон — product.html
    template_name = 'post.html'
    # Название объекта, в котором будет выбранный пользователем продукт
    context_object_name = 'new'


class NewsCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.news_create',)
    form_class = NewsForm
    model = Post
    template_name = 'news_create.html'

    def form_valid(self, form):
        news = form.save(commit=False)
        news.post_type = _('news')
        return super().form_valid(form)


class ArticleCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.article_create',)
    form_class = ArticleForm
    model = Post
    template_name = 'article_create.html'

    def form_valid(self, form):
        article = form.save(commit=False)
        article.post_type = _('article')
        return super().form_valid(form)


class NewsUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.news_update',)
    form_class = NewsForm
    model = Post
    template_name = 'news_edit.html'

    # Переопределяем метод получения объекта
    def get_object(self, *args, **kwargs):
        # Кэш очень похож на словарь, и метод get действует так же.
        # Он забирает значение по ключу, если его нет, то забирает None
        obj = cache.get(f'post-{self.kwargs["pk"]}', None)

        # Если объекта нет в кэше, то получаем его и записываем в кэш
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'post-{self.kwargs["pk"]}', obj)
            return obj


class ArticleUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.article_update',)
    form_class = ArticleForm
    model = Post
    template_name = 'article_edit.html'

    # Переопределяем метод получения объекта
    def get_object(self, *args, **kwargs):
        # Кэш очень похож на словарь, и метод get действует так же.
        # Он забирает значение по ключу, если его нет, то забирает None
        obj = cache.get(f'post-{self.kwargs["pk"]}', None)

        # Если объекта нет в кэше, то получаем его и записываем в кэш
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'post-{self.kwargs["pk"]}', obj)
            return obj


class NewsDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.news_delete',)
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('post_list')


class ArticleDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.article_delete',)
    model = Post
    template_name = 'article_delete.html'
    success_url = reverse_lazy('post_list')


@login_required
@csrf_protect
def subscriptions(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        action = request.POST.get('action')

        category = Category.objects.get(id=category_id)
        if action == 'subscribe':
            Subscriber.objects.get_or_create(user=request.user, category=category)
        elif action == 'unsubscribe':
            Subscriber.objects.filter(user=request.user, category=category).delete()

    categories_with_subscriptions = Category.objects.annotate(
        user_subscribed=Exists(
            Subscriber.objects.filter(user=request.user, category=OuterRef('pk'))
        )
    ).order_by('name')

    return render(request, 'post_subscriptions.html', {'categories': categories_with_subscriptions})
