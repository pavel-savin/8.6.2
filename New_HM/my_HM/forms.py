from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['post_category', 'article_title_news', 'text_title_news']
