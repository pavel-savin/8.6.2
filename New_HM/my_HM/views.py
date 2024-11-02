from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView)
from .models import Post
from .filter_search import PostFilter
from .forms import PostForm

# Список постов
class PostsList(ListView):
    model = Post
    ordering = '-automatic_data_time'  # Изменено на обратный порядок
    template_name = 'flatpages/news_feed.html'
    context_object_name = 'Posts'
    paginate_by = 10  # Пагинация



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
class PostCreateView(BasePostView, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'flatpages/post_edit.html'
    
    def form_valid(self, form):
        post = form.save(commit=False)
        # Устанавливаем тип в зависимости от URL
        if 'news' in self.request.path:
            post.article_or_news = 0  # новость
        elif 'articles' in self.request.path:
            post.article_or_news = 1  # статья
        return super().form_valid(form)

class PostUpdateView(BasePostView, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'flatpages/post_edit.html'

class PostDeleteView(BasePostView, DeleteView):
    model = Post
    template_name = 'flatpages/post_delete.html'