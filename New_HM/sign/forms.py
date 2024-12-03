from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group

class CustomSignupForm(SignupForm):

    def save(self, request):
        # Сначала вызываем родительский метод, чтобы сохранить пользователя
        user = super().save(request)
        # Получаем группу 'common'
        common_group = Group.objects.get(name='common')
        # Добавляем пользователя в группу
        common_group.user_set.add(user)
        return user
