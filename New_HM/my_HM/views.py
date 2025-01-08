from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView)
from .models import Post
from .filter_search import PostFilter
from .forms import PostForm
from django.http import HttpResponseForbidden
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Author



# Список постов
class PostsList(ListView):
    model = Post
    ordering = '-automatic_data_time'  # Изменено на обратный порядок
    template_name = 'flatpages/news_feed.html'
    context_object_name = 'Posts'
    paginate_by = 5  # Пагинация



# Детали новости
class PostDetail(DetailView):
    model = Post
    template_name = 'flatpages/Post.html'
    context_object_name = 'Post'
   
   
# Поиск новостей    
class NewsSearchView(ListView):
    model = Post
    ordering = '-automatic_data_time'
    template_name = 'flatpages/news_search.html'
    context_object_name = 'news'
    paginate_by = 3

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context
    
# Переход после success_url
class BasePostView:
    success_url = reverse_lazy('posts_list')

    def get_success_url(self):
        return self.success_url


# Универсальный класс для создания, обновления и удаления постов
class PostCreateView(LoginRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'flatpages/post_edit.html'

    # Проверка на группу 'authors'
    def dispatch(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='authors').exists():
            return HttpResponseForbidden("У вас нет прав на создание постов.")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_author'] = self.request.user.groups.filter(name='authors').exists()
        return context

    def get_success_url(self):
        return reverse_lazy('posts_list')  # Это перенаправит на список постов после успешного создания

    def form_valid(self, form):
        post = form.save(commit=False)
    
        # Получаем или создаем объект Author для текущего пользователя
        author, created = Author.objects.get_or_create(user=self.request.user)
    
        # Устанавливаем автора для поста
        post.author = author
    
        # Если путь начинается с /news/, то это новость, иначе статья
        if self.request.path.startswith('/news/'):
            post.article_or_news = 0  # новость
        elif self.request.path.startswith('/articles/'):
            post.article_or_news = 1  # статья

        # Сохраняем пост
        post.save()
    
        return super().form_valid(form)





class PostUpdateView(LoginRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'flatpages/post_edit.html'

    # Проверка на группу 'authors' и права на редактирование поста
    def dispatch(self, request, *args, **kwargs):
        post = self.get_object()
        if not request.user.groups.filter(name='authors').exists():
            return HttpResponseForbidden("У вас нет прав на редактирование постов.")
        if post.author.user != request.user:
            return HttpResponseForbidden("Вы не можете редактировать чужие посты.")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_author'] = self.request.user.groups.filter(name='authors').exists()
        return context

    def get_success_url(self):
        return reverse_lazy('posts_list')  # Перенаправляем на список постов после успешного редактирования


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'flatpages/post_delete.html'

    # Проверка на группу 'authors'
    def dispatch(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='authors').exists():
            return HttpResponseForbidden("У вас нет прав на удаление постов.")
        return super().dispatch(request, *args, **kwargs)
    
    
# # Универсальный класс для создания, обновления и удаления постов
# class PostCreateView(BasePostView, CreateView):
#     form_class = PostForm
#     model = Post
#     template_name = 'flatpages/post_edit.html'
    
#     def form_valid(self, form):
#         post = form.save(commit=False)
#         # Устанавливаем тип в зависимости от URL
#         if 'news' in self.request.path:
#             post.article_or_news = 0  # новость
#         elif 'articles' in self.request.path:
#             post.article_or_news = 1  # статья
#         return super().form_valid(form)

# class PostUpdateView(BasePostView, UpdateView):
#     form_class = PostForm
#     model = Post
#     template_name = 'flatpages/post_edit.html'

# class PostDeleteView(BasePostView, DeleteView):
#     model = Post
#     template_name = 'flatpages/post_delete.html'