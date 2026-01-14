from django.urls import path
from .views import CadastroUsuarioView, UsuarioDeleteView, UsuarioListView, UsuarioUpdateView, toggle_status_usuario

app_name = 'usuarios'

urlpatterns = [
    
    path('novo/', CadastroUsuarioView.as_view(), name='cadastro-usuario'),
    path('lista/', UsuarioListView.as_view(), name='listar-usuarios'),
    path('editar/<str:pk>/', UsuarioUpdateView.as_view(), name='editar-usuario'),
    path('status/<str:pk>/', toggle_status_usuario, name='toggle-status'),
    path('excluir/<str:pk>/', UsuarioDeleteView.as_view(), name='excluir-usuario'),
    
]