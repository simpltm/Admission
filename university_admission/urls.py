"""
URL configuration for university_admission project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
# from accounts.views import register, profile

urlpatterns = [
    path('', include(('applications_app.urls', 'applications'), namespace='applications')),  # Корневой маршрут теперь с namespace
    path('admin/', admin.site.urls),
    path('programs/', include('programs_app.urls')),
    path('dashboard/', include('dashboard_app.urls')),
    path('reports/', include(('reports_app.urls', 'reports_app'), namespace='reports_app')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('accounts_app.urls')),  # Добавляем URL-маршруты для профиля
    # path('accounts/register/', register, name='register'),
    # path('accounts/profile/', profile, name='profile'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += [path('__debug__/', include('debug_toolbar.urls'))]
