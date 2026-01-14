from django import forms
from .models import Evento
from .models import Grade
from .models import ItemGrade
from django.contrib.auth import get_user_model

class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = ['descricao', 'data_inicio', 'data_fim']
        widgets = {
            'descricao': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Ex: Aniversário da Rede 2025'
            }),
            'data_inicio': forms.DateInput(attrs={
                'class': 'form-control', 
                'type': 'date'
            }),
            'data_fim': forms.DateInput(attrs={
                'class': 'form-control', 
                'type': 'date'
            }),
        }

User = get_user_model()

class GradeForm(forms.ModelForm):
    # --- PARTE 1: BUSCA DE GRUPO ---
    busca_grupo = forms.CharField(
        label="Adicionar Fornecedor / Grupo",
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Busque e adicione múltiplos grupos...',
            'id': 'input-busca-grupo'
        })
    )

    grupos_json = forms.CharField(widget=forms.HiddenInput(), required=False)

    # --- PARTE 2: CORREÇÃO AQUI (Trocamos 'first_name' por 'name') ---
    comprador = forms.ModelChoiceField(
        # Filtra compradores ativos e ordena pelo campo 'name' que existe no seu banco
        queryset=User.objects.filter(perfil__eh_comprador=True, is_active=True).order_by('name'),
        label="Comprador Responsável",
        widget=forms.Select(attrs={'class': 'form-select select2'}), 
        required=True
    )

    class Meta:
        model = Grade
        fields = [
            'evento', 
            'comprador', 
            'data_inicio', 
            'data_fim', 
            'observacoes',
            'grupos_json'
        ]
        
        widgets = {
            'evento': forms.Select(attrs={'class': 'form-select'}),
            'data_inicio': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'data_fim': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # CORREÇÃO NA EXIBIÇÃO DO NOME
        # Como seu usuário não tem get_full_name() padrão, usamos obj.name direto
        self.fields['comprador'].label_from_instance = lambda obj: f"{obj.name} ({obj.username})"

    def clean(self):
        cleaned_data = super().clean()
        grupos = cleaned_data.get('grupos_json')
        
        if not grupos or grupos == '[]':
            self.add_error('busca_grupo', "Adicione pelo menos um Grupo Econômico à grade.")
        
        return cleaned_data
    
class ItemGradeForm(forms.ModelForm):
    # Campo "fake" para buscar SKUs no BigQuery
    busca_sku = forms.CharField(
        label="Buscar Produtos (SKUs)",
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Digite o cód ou nome para buscar...',
            'id': 'input-busca-sku'
        })
    )
    
    # Campo oculto para receber o JSON dos SKUs selecionados
    skus_json = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = ItemGrade
        fields = [
            'descricao_resumida', 'unidade_medida', 'quantidade_embalagem',
            'volume_negociado', 'custo_bruto', 'custo_liquido', 
            'verba_sell_in', 'desconto_boleto'
        ]
        widgets = {
            'descricao_resumida': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Suco Tang 25g'}),
            
          
            'unidade_medida': forms.Select(attrs={'class': 'form-select'}),
            'quantidade_embalagem': forms.NumberInput(attrs={
                'class': 'form-control', 
                'step': '0.01', 
                'placeholder': '1'
            }),            
            'volume_negociado': forms.NumberInput(attrs={'class': 'form-control'}),
            'custo_bruto': forms.NumberInput(attrs={'class': 'form-control'}),
            'custo_liquido': forms.NumberInput(attrs={'class': 'form-control'}),
            'verba_sell_in': forms.NumberInput(attrs={'class': 'form-control'}),
            'desconto_boleto': forms.NumberInput(attrs={'class': 'form-control'}),
        }