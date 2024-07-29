from django.urls import path, include
from django.views.decorators.cache import cache_page


# Импортируем созданное нами представление
from .views import (
   PostsList, PostDetail, NewsCreate, NewsUpdate, NewsDelete, PostsSearch, ArticleCreate,
   ArticleUpdate, subscriptions, Index
)


urlpatterns = [
   # path — означает путь.
   # В данном случае путь ко всем товарам у нас останется пустым,
   # чуть позже станет ясно почему.
   # Т.к. наше объявленное представление является классом,
   # а Django ожидает функцию, нам надо представить этот класс в виде view.
   # Для этого вызываем метод as_view.
   path('', cache_page(60)(PostsList.as_view()), name='post_list'),

   path('i18n/', include('django.conf.urls.i18n')),  # подключаем встроенные эндопинты для работы с локализацией

   # pk — это первичный ключ товара, который будет выводиться у нас в шаблон
   # int — указывает на то, что принимаются только целочисленные значения
   path('<int:pk>', cache_page(300)(PostDetail.as_view()), name='post_detail'),
   path('news/create/', cache_page(300)(NewsCreate.as_view()), name='news_create'),
   path('news/<int:pk>/edit/', NewsUpdate.as_view(), name='news_update'),
   path('news/<int:pk>/delete/', cache_page(300)(NewsDelete.as_view()), name='news_delete'),
   path('search/', PostsSearch.as_view(), name='news_search'),
   path('article/create/',cache_page(300)(ArticleCreate.as_view()), name='article_create'),
   path('article/<int:pk>/edit/', ArticleUpdate.as_view(), name='article_update'),
   path('article/<int:pk>/delete/', cache_page(300)(ArticleUpdate.as_view()), name='article_delete'),
   path('subscriptions/', subscriptions, name='posts_subscriptions'),
   path('hello/', Index.as_view(), name='hello_world_locale')
]
