from django.contrib import admin
from .models import DimFornecedor


# Opcional: Crie uma classe de admin para configurar a exibição
class DimFornecedorAdmin(admin.ModelAdmin):
    # Apenas para leitura, remove os botões de adicionar/mudar
    def has_add_permission(self, request):
        return False
    def has_change_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False

    list_display = ('nomerazao', 'fantasia', 'cnpj_completo', 'nome_rede')
    search_fields = ('nomerazao', 'fantasia', 'cnpj_completo')

admin.site.register(DimFornecedor, DimFornecedorAdmin)

# Register your models here.
