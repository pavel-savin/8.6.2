from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


class Author(models.Model):
    user = models.OneToOneField(User, on_delete= models.CASCADE)
    rating = models.IntegerField(default=0)
    posts = models.Manager
    
    def update_rating(self):
        # Cуммарный рейтинг каждой статьи автора * 3
        post_rating = Post.objects.filter(author=self).aggregate(Sum('rating'))['rating__sum'] or 0
        post_rating *= 3
        # Суммарный рейтинг всех комментариев автора
        comment_rating = Comment.objects.filter(user=self.user).aggregate(Sum('rating'))['rating__sum'] or 0
        # Cуммарный рейтинг всех комментариев к статьям автора
        post_comments_rating = Comment.objects.filter(post__author=self).aggregate(Sum('rating'))['rating__sum'] or 0
        # Итоговый рейтинг
        self.rating = post_rating + comment_rating + post_comments_rating 
        self.save()
    
class Category(models.Model):
    categories = models.CharField(max_length=100, unique=True)
    
class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='post')
    article_or_news = models.IntegerField(default= 0)
    automatic_data_time = models.DateTimeField(auto_now_add= True)
    post_category = models.ManyToManyField(Category, through= 'PostCategory')
    article_title_news = models.CharField(max_length= 255, db_index=True) #добавлено индексирование
    text_title_news = models.TextField()
    rating = models.IntegerField(default=0)
    
    def like(self):
        self.rating += 1
        self.save()
        
    def dislike(self):
        self.rating -=1
        self.save()
    
    def preview(self):
        return f"{self.text_title_news[:124]}..."
    
class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    automatic_data_time = models.DateTimeField(auto_now_add= True)
    rating = models.IntegerField(default=0)
    
    def like(self):
        self.rating += 1
        self.save()
        
    def dislike(self):
        self.rating -=1
        self.save()
        