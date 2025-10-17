from django.urls import path
from . import views

app_name = 'apuracao_contrato'

urlpatterns = [
    path('', views.apuracao, name='apuracao'),
]