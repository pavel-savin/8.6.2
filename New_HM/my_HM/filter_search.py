import django_filters 
from my_HM.models import Post
from django import forms


class PostFilter(django_filters.FilterSet):
    article_title_news = django_filters.CharFilter(
        lookup_expr='icontains', label='Название'
    )
    author__user__username = django_filters.CharFilter(
        lookup_expr='icontains', label='Автор'
    )
    automatic_data_time = django_filters.DateFilter(
        lookup_expr='gte', label='Позже даты',
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = Post
        fields = ['article_title_news', 'author__user__username', 'automatic_data_time']