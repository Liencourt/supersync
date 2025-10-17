from django.db import models

class DimFornecedor(models.Model):
    # Mapeamento dos campos
    # Definimos 'seqpessoa' como a chave primária, pois é o identificador único.
    seqpessoa = models.IntegerField(primary_key=True, db_column='seqpessoa')

    # Usamos CharField para campos de texto. É uma boa prática definir um max_length.
    # Se você não souber o tamanho exato, um valor como 255 é um padrão seguro.
    nomerazao = models.CharField(max_length=255, db_column='NOMERAZAO')
    fantasia = models.CharField(max_length=255, db_column='FANTASIA', null=True, blank=True)
    nrocgccpf = models.CharField(max_length=14, db_column='NROCGCCPF')
    digcgccpf = models.CharField(max_length=2, db_column='DIGCGCCPF')
    cnpj_completo = models.CharField(max_length=18, db_column='cnpj_completo')
    seqrede = models.IntegerField(db_column='SEQREDE')
    nome_rede = models.CharField(max_length=255, db_column='NOME_REDE', null=True, blank=True)
    seqloja = models.IntegerField(db_column='SEQLOJA')
    seqassociado = models.IntegerField(db_column='SEQASSOCIADO', null=True, blank=True)
    nomeassociado = models.CharField(max_length=255, db_column='NOMEASSOCIADO', null=True, blank=True)
    tipfornecedor = models.CharField(max_length=50, db_column='TIPFORNECEDOR', null=True, blank=True)

    class Meta:
        # A MÁGICA ACONTECE AQUI
        managed = False
        # Nome exato da tabela no banco de dados, incluindo o schema.
        # O Django usará a conexão 'gcp_contracts' para encontrar isso.
        db_table = '"gold"."dim_fornecedor"'
        # Opcional, mas bom para organização:
        verbose_name = 'Fornecedor (Dimensão)'
        verbose_name_plural = 'Fornecedores (Dimensão)'

    def __str__(self):
        return self.nomerazao

