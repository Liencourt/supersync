from django.urls import path
from . import views

app_name = 'contratos'

urlpatterns = [
    path('', views.buscar_contratos, name='listar_contratos'),
    path('detalhes/<int:nrosubcontrato>/', views.listar_detalhes_contrato, name='detalhes_contrato'),
]