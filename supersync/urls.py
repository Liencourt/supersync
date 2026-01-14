"""
URL configuration for supersync project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('contratos/', include('contratos.urls')),
    path('apuracao/', include('apuracao_contrato.urls')),
    path('apuracao_grade/', include('apuracao_grade.urls')),
    # Redireciona a URL raiz para a página de login
    path('', RedirectView.as_view(url='/accounts/login/', permanent=False)),
    path('usuarios/', include('usuarios.urls')),
]
