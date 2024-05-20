from datetime import datetime
# Импортируем класс, который говорит нам о том,
# что в этом представлении мы будем выводить список объектов из БД
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from django_filters.views import FilterView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from .models import Post
from .filters import PostFilter
from .forms import NewsForm, ArticleForm


@login_required
def show_protected_page(request):
    pass


class PostsList(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    # Поле, которое будет использоваться для сортировки объектов
    ordering = 'created_at'
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

    # Метод get_context_data позволяет нам изменить набор данных,
    # который будет передан в шаблон.
    def get_context_data(self, **kwargs):
        # С помощью super() мы обращаемся к родительским классам
        # и вызываем у них метод get_context_data с теми же аргументами,
        # что и были переданы нам.
        # В ответе мы должны получить словарь.
        context = super().get_context_data(**kwargs)
        # К словарю добавим текущую дату в ключ 'time_now'.
        context['time_now'] = datetime.utcnow()
        # Добавим ещё одну пустую переменную,
        # чтобы на её примере рассмотреть работу ещё одного фильтра.
        context['next_sale'] = "Распродажа в среду"
        context['filterset'] = self.filterset
        return context


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
        news.post_type = 'news'
        return super().form_valid(form)


class ArticleCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.article_create',)
    form_class = ArticleForm
    model = Post
    template_name = 'article_create.html'

    def form_valid(self, form):
        article = form.save(commit=False)
        article.post_type = 'article'
        return super().form_valid(form)


class NewsUpdate(PermissionRequiredMixin,UpdateView):
    permission_required = ('news.news_update',)
    form_class = NewsForm
    model = Post
    template_name = 'news_edit.html'


class ArticleUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.article_update',)
    form_class = ArticleForm
    model = Post
    template_name = 'article_edit.html'


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