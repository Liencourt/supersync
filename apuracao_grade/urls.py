from django.urls import path
from .views import (
    EventoListView, 
    EventoCreateView, 
    EventoUpdateView, 
    EventoDeleteView,
    GradeDetalheView,
    GradeListView,
    GradeCreateView,
    buscar_fornecedores_api,
    buscar_produtos_api,
    excluir_grade,
    excluir_item_grade,
    exportar_grade_excel,
    gerenciar_distribuicao,
    api_obter_item,      
    editar_item_grade,
    finalizar_grade,
    api_dashboard_apuracao,
    DashboardGradeView,
    excluir_grade,
    api_criar_evento_modal,
    atualizar_distribuicao_view

)
from apuracao_grade import views

app_name = 'apuracao_grade'

urlpatterns = [
    # Rotas de Eventos
    path('eventos/', EventoListView.as_view(), name='evento-list'),
    path('eventos/novo/', EventoCreateView.as_view(), name='evento-create'),
    path('eventos/<int:pk>/editar/', EventoUpdateView.as_view(), name='evento-update'),
    path('eventos/<int:pk>/excluir/', EventoDeleteView.as_view(), name='evento-delete'),

    path('grades/', GradeListView.as_view(), name='grade-list'),
    path('grades/nova/', GradeCreateView.as_view(), name='grade-create'),
    path('grades/<int:pk>/itens/', GradeDetalheView.as_view(), name='grade-detalhe'),
    path('api/buscar-produtos/', buscar_produtos_api, name='api-buscar-produtos'),
    path('itens/<int:pk>/excluir/', excluir_item_grade, name='item-delete'),
    path('grades/<int:pk>/excluir/', excluir_grade, name='grade-delete'),
    path('api/eventos/novo-modal/', api_criar_evento_modal, name='api-criar-evento-modal'),
    
    
    path('api/buscar-fornecedores/', buscar_fornecedores_api, name='api-buscar-fornecedores'),
    path('itens/<int:pk>/distribuicao/', gerenciar_distribuicao, name='item-distribuicao'),
    path('api/item/<int:pk>/', api_obter_item, name='api-obter-item'),
    path('itens/<int:pk>/editar/', editar_item_grade, name='item-update'),
    path('grades/<int:pk>/finalizar/', finalizar_grade, name='grade-finalizar'),
    path('grades/<int:pk>/exportar/', exportar_grade_excel, name='grade-exportar'),
    path('api/dashboard/<int:pk>/', api_dashboard_apuracao, name='api-dashboard'),
    path('grades/<int:pk>/dashboard/', DashboardGradeView.as_view(), name='grade-dashboard'),
    path('grade/<int:grade_id>/editar-cabecalho/', views.editar_cabecalho_grade, name='editar_cabecalho_grade'),
    

    path('api/atualizar-distribuicao/', views.atualizar_distribuicao_view, name='api-atualizar-distribuicao'),
]