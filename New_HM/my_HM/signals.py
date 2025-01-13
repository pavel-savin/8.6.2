
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.core.mail import send_mail
from django.contrib.auth.models import User
from .models import Post

@receiver(m2m_changed, sender=Post.post_category.through)
def notify_subscribers(sender, instance, action, **kwargs):
    if action == 'post_add':  # Проверка на создание новой статьи
        from .models import Subscription
        # Перебираем все категории, к которым относится статья
        for category in instance.post_category.all():
            # Получаем подписчиков для каждой категории
            subscribers = Subscription.objects.filter(category=category)
            emails = [sub.user.email for sub in subscribers]
            
            # Отправляем уведомление на email
            send_mail(
                subject=f'Новая статья в категории {category.categories}',
                message=f'Статья: {instance.article_title_news}\n\nСсылка: http://127.0.0.1:8000/news/{instance.id}',
                from_email='BangBong097@yandex.ru',  # Свой email
                recipient_list=emails,
            )

@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        send_mail(
            subject='Добро пожаловать!',
            message='Спасибо за регистрацию на нашем сайте!',
            from_email='BangBong097@yandex.ru',
            recipient_list=[instance.email],
        )