
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Post, Subscription
from django.contrib.auth.models import User

@receiver(post_save, sender=Post)
def notify_subscribers(sender, instance, created, **kwargs):
    if created and instance.category:
        subscribers = Subscription.objects.filter(category=instance.category)
        emails = [sub.user.email for sub in subscribers]
        send_mail(
            subject=f'Новая статья в категории {instance.category.name}',
            message=f'Статья: {instance.title}\n\nСсылка: http://127.0.0.1:8000/news/{instance.id}',
            from_email='your_username@yandex.ru',
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