from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
from applications_app.models import Application

# Create your views here.

@login_required
def profile(request):
    """Представление для просмотра и редактирования профиля пользователя"""
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль успешно обновлен')
            return redirect('accounts:profile')
    else:
        form = UserChangeForm(instance=request.user)
    applications = Application.objects.filter(applicant=request.user)
    return render(request, 'accounts_app/profile.html', {
        'form': form,
        'user': request.user,
        'applications': applications,
    })
