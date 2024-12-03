from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from django.views.generic.edit import CreateView
from .models import BaseRegisterForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/'
    

def confirm_logout(request):
    return render(request, 'sign/confirm_logout.html')  # Страница подтверждения выхода

def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect('/news/')  # Перенаправление после выхода
    return redirect('confirm_logout')  # Если запрос не POST, отправляем на подтверждение


@login_required
def upgrade_to_author(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not user.groups.filter(name='authors').exists():  # Проверка, состоит ли пользователь в группе authors
        authors_group.user_set.add(user)
    return redirect('/')
# Create your views here.
