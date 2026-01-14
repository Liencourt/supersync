# dashboard/views.py
from django.views.generic import TemplateView
# Importe seus models quando tiver
# from apuracao_grade.models import Grade
# from apuracao_contrato.models import Contrato

class HomeView(TemplateView):
    template_name = 'dashboard/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Exemplo de dados que você injetará futuramente:
        # context['total_grades'] = Grade.objects.filter(status='aberta').count()
        # context['contratos_pendentes'] = Contrato.objects.filter(status='analise').count()
        
        # Por enquanto, dados mocados para o visual:
        context['kpi_grades'] = 12
        context['kpi_contratos'] = 5
        context['kpi_fornecedores'] = 142
        return context
