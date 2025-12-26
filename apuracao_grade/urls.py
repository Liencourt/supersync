from django.urls import path
from .views import grupoeconomico_view

app_name = 'apuracao_grade'

urlpatterns = [
    path('grupoeconomico/', grupoeconomico_view, name='grupoeconomico'),
]
