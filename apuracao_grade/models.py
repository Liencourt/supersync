from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.conf import settings


#--Classe de Evento - Cabeçalho dos eventos comerciais --#
class Evento(models.Model):
    # ... campos anteriores (id, descricao, datas) mantidos iguais ...
    id = models.AutoField(db_column='idevento', primary_key=True)
    descricao = models.CharField(db_column='nomeevento', max_length=255, verbose_name=_("Nome do Evento"))
    data_inicio = models.DateField(db_column='datainicio', verbose_name=_("Data de Início"))
    data_fim = models.DateField(db_column='datafim', verbose_name=_("Data de Fim"))

    
    criado_em = models.DateTimeField(auto_now_add=True, null=True, verbose_name=_("Criado em"))
    atualizado_em = models.DateTimeField(auto_now=True, null=True, verbose_name=_("Atualizado em"))

    class Meta:
        db_table = 'gradeevento'
        verbose_name = _("Evento")
        verbose_name_plural = _("Eventos")
        ordering = ['-data_inicio']
        # managed = True 

    
    def __str__(self):
        return f"{self.descricao} ({self.data_inicio.year})"

    def clean(self):
        if self.data_inicio and self.data_fim and self.data_inicio > self.data_fim:
            raise ValidationError(_("A data final não pode ser anterior à inicial."))

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)






    # Cabeçalho Grade - detalhes resumidos


class Grade(models.Model):
    """
    1º Nível: O Cabeçalho (Supergrade)
    """
    STATUS_CHOICES = [
        ('rascunho', 'Rascunho'),
        ('em_analise', 'Em Análise'),
        ('aprovada', 'Aprovada'),
        ('concluida', 'Concluída'),
        ('cancelada', 'Cancelada'),
    ]

    # Vincula ao Evento que já criamos
    evento = models.ForeignKey(
        'Evento', 
        on_delete=models.PROTECT,
        related_name='grades',
        verbose_name=_("Evento Comercial")
    )
    
    # Comprador: Pode ser um texto livre (nome) ou vínculo com usuário, conforme sua regra
    comprador_responsavel = models.CharField(
        max_length=100, 
        verbose_name="Comprador (Antigo/Texto)", 
        null=True, blank=True
    )
    
    comprador = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, # Se apagar o usuário, a grade não apaga (fica sem comprador)
        null=True, 
        blank=True,
        related_name='grades_comprador',
        limit_choices_to={'perfil__eh_comprador': True}, # <--- O PULO DO GATO: Filtra no Admin do Django
        verbose_name="Comprador Responsável"
    )
    
    
    data_inicio = models.DateField(verbose_name=_("Início da Grade"))
    data_fim = models.DateField(verbose_name=_("Fim da Grade"))
    
    observacoes = models.TextField(blank=True, null=True, verbose_name=_("Observações"))
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='rascunho')
    
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Grade de Compra"
        verbose_name_plural = "Grades de Compras"
        ordering = ['-id']

    def __str__(self):
        return f"Grade #{self.id} - {self.grupo_economico_nome}"

class GradeGrupo(models.Model):
    """
    Tabela filha que permite múltiplos fornecedores/grupos para uma única grade.
    """
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, related_name='grupos')
    
    grupo_id = models.CharField(max_length=50, verbose_name="Cód. Grupo")
    grupo_nome = models.CharField(max_length=255, verbose_name="Nome Grupo")
    
    

    def __str__(self):
        return f"{self.grupo_nome} ({self.grade_id})"


class ItemGrade(models.Model):
    """
    2º Nível: O Agrupamento de Negociação (ex: 'Suco Tang em pó 25g')
    """
    UNIDADE_CHOICES = [
        ('UN', 'Unidade'),
        ('CX', 'Caixa'),
        ('FD', 'Fardo'),
        ('KG', 'Quilo'),
        ('TON', 'Tonelada'),
    ]

    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, related_name='itens')
    
    descricao_resumida = models.CharField(
        max_length=255, 
        verbose_name=_("Descrição Resumida"),
        help_text="Ex: Suco Tang Diversos Sabores 25g"
    )
    
    unidade_medida = models.CharField(max_length=10, choices=UNIDADE_CHOICES, default='UN')

    quantidade_embalagem = models.DecimalField(
        max_digits=10, decimal_places=2, 
        default=1,
        verbose_name="Qtd. na Embalagem",
        help_text="Ex: 12 (para caixa com 12 un)"
    )
    
    # Valores Monetários e Volumes
    volume_negociado = models.DecimalField(
        max_digits=12, decimal_places=2, verbose_name=_("Volume Total Negociado")
    )

    # --- NOVO CAMPO ADICIONADO AQUI ---
    custo_bruto = models.DecimalField(
        max_digits=10, decimal_places=2, 
        verbose_name=_("Custo Bruto Unit."),
        help_text="Custo com impostos"
    )
    
    custo_liquido = models.DecimalField(
        max_digits=10, decimal_places=2, 
        verbose_name=_("Custo Líquido Unit."),
        help_text="Custo final sem impostos recuperáveis"
    )
    
    verba_sell_in = models.DecimalField(
        max_digits=10, decimal_places=2, 
        verbose_name=_("Verba Sell-In"),
        default=0
    )
    
    desconto_boleto = models.DecimalField(
        max_digits=5, decimal_places=2, 
        verbose_name=_("Desconto Boleto (%)"),
        help_text="Informe o percentual (ex: 5.00 para 5%)",
        default=0
    )

    def __str__(self):
        return f"{self.descricao_resumida} (Grade {self.grade_id})"
    

class ItemGradeSKU(models.Model):
    item_grade = models.ForeignKey(ItemGrade, on_delete=models.CASCADE, related_name='skus')
    
    codigo_produto = models.CharField(max_length=50, verbose_name="Cód. Produto (ERP)")
    descricao_produto = models.CharField(max_length=255, verbose_name="Descrição (ERP)")
    embalagem = models.CharField(max_length=50, blank=True, null=True)
    
    class Meta:
        unique_together = ('item_grade', 'codigo_produto')
        verbose_name = "SKU do Item"
        verbose_name_plural = "SKUs do Item"


class ItemGradeDistribuicao(models.Model):
    """
    3º Nível (Paralelo): A divisão do volume por Associado.
    """
    item_grade = models.ForeignKey(ItemGrade, on_delete=models.CASCADE, related_name='distribuicoes')
    
    associado_id = models.IntegerField(verbose_name="ID Associado") 
    associado_nome = models.CharField(max_length=255)
    
    percentual_participacao = models.DecimalField(
        max_digits=5, decimal_places=2, 
        verbose_name="% Participação"
    )
    
    volume_compra_minima = models.DecimalField(
        max_digits=12, decimal_places=2,
        verbose_name="Volume Mínimo (CX/FD)"
    )

    # --- CAMPO FALTANTE (ADICIONAR) ---
    volume_fisico = models.DecimalField(
        max_digits=12, decimal_places=2,
        verbose_name="Volume Físico (UN)",
        default=0,
        help_text="Volume convertido em unidades soltas para conferência"
    )

    class Meta:
        ordering = ['associado_nome']
        verbose_name = "Distribuição por Associado"
        verbose_name_plural = "Distribuições por Associados"
        # Garante que não duplique loja no mesmo item
        unique_together = ('item_grade', 'associado_id')