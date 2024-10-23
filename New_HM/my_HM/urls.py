from django.urls import path
from .views import PostsList, PostDetail

urlpatterns = [
    path('', PostsList.as_view(), name='posts_list'),  # Главная страница с постами
    path('<int:pk>/', PostDetail.as_view(), name='post_detail'),  # Страница деталей поста
]
