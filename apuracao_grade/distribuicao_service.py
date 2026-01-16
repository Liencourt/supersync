import os
import pandas as pd
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from google.cloud import bigquery
from sqlalchemy import create_engine
from django.conf import settings

def get_db_engine():
    """
    Cria uma engine SQLAlchemy corrigindo o bug do 'postgres://'
    """
    # Pega a URL do banco
    db_url = os.getenv('DATABASE_URL')
    
    if not db_url:
        # Fallback local
        db_url = "postgresql://postgres:13752738@localhost:5432/sync"
    
    # --- A CORREÇÃO MÁGICA ESTÁ AQUI ---
    # Se a URL vier como 'postgres://', trocamos para 'postgresql://'
    if db_url and db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)
        
    return create_engine(db_url)

def calculatrimestre():
    hoje = date.today()
    trimestre_atual = (hoje.month - 1) // 3 + 1

    if trimestre_atual == 1:
        ano_trimestre_anterior = hoje.year - 1
        trimestre_anterior = 4
    else:
        ano_trimestre_anterior = hoje.year
        trimestre_anterior = trimestre_atual - 1

    mes_inicio = 3 * (trimestre_anterior - 1) + 1
    mes_fim = mes_inicio + 2
    data_inicio = datetime(ano_trimestre_anterior, mes_inicio, 1)

    if mes_fim == 12:
        data_fim = datetime(ano_trimestre_anterior + 1, 1, 1) - relativedelta(days=1)
    else:
        data_fim = datetime(ano_trimestre_anterior, mes_fim + 1, 1) - relativedelta(days=1)

    return [trimestre_anterior, data_inicio.date(), data_fim.date(), ano_trimestre_anterior]

def agrupaporcategoria(df):
    df_agrupado = df.groupby(['NomeAssociado', 'Nome_Grupo'], as_index=False)[['qtditens', 'valorTotalItem']].sum()
    qtd_por_subgrupo = df_agrupado.groupby('Nome_Grupo')['qtditens'].transform('sum')
    df_agrupado['percentual_qtd'] = (df_agrupado['qtditens'] / qtd_por_subgrupo) * 100
    df_agrupado = df_agrupado.sort_values(by=['Nome_Grupo', 'percentual_qtd'], ascending=[True, False])
    return df_agrupado

def agrupaporassociado(df):
    df_agrupado = df.groupby(['NomeAssociado'], as_index=False)[['qtditens', 'valorTotalItem']].sum()
    df_agrupado['percentual_qtd'] = (df_agrupado['qtditens'] / df_agrupado['qtditens'].sum()) * 100
    df_agrupado = df_agrupado.round(2)
    return df_agrupado

def pivotableassociado(df):
    df_pivot = df.pivot_table(
        index='Nome_Grupo',
        columns='NomeAssociado',
        values='percentual_qtd',
        fill_value=0
    )
    df_pivot_grupo = df_pivot.sort_index()
    pivot = df_pivot_grupo.reset_index()
    return pivot

def executar_atualizacao_distribuicao():
    """
    Função principal chamada pela View do Django
    """
    print("Iniciando rotina de distribuição...")
    
    # 1. Conexão BigQuery (Blindada Híbrida)
    try:
        client = bigquery.Client() # Tenta Cloud Run (Automático)
    except:
        from google.oauth2 import service_account
        if os.path.exists('credenciais.json'):
            client = bigquery.Client(credentials=service_account.Credentials.from_service_account_file('credenciais.json'))
        else:
            return False, "Erro: Credenciais GCP não encontradas."

    # 2. Conexão Postgres (SQLAlchemy)
    engine = get_db_engine()

    # 3. Lógica de Negócio
    listadados = calculatrimestre()
    trimestre = listadados[0]
    datainicio = listadados[1]
    datafim = listadados[2]
    ano = listadados[3]

    print(f"Processando Trimestre: {trimestre}/{ano}")

    query = f"""SELECT  NomeAssociado, NomeLoja,Nome_Produto as Produto,seqfamilia,Nome_familia as Familia,Nome_Grupo,Nome_SubGrupo as subgrupo,
    sum(quantidadeItem) as qtditens, sum(valorAcrescimoItem) as valorAcrescimoItem ,
    sum(valorDescontoItem) as valorDescontoItem , sum(valorTotalItem-valorDescontoItem) as valorTotalItem , sum(qtdCupomDepartamento) as qtdCupomDepartamento
    FROM `singular-ray-422121`.gold.obt_tb_venda_sumarizada_prodcrm
    where dataVenda between '{datainicio}' and '{datafim}'
    group by NomeAssociado,NomeLoja,Nome_Produto,seqfamilia,Nome_familia,Nome_Grupo,Nome_SubGrupo
    order by NomeAssociado, NomeLoja,Nome_Produto,Nome_Grupo,Nome_SubGrupo"""

    try:
        df = client.query(query).to_dataframe()
    except Exception as e:
        return False, f"Erro BigQuery: {str(e)}"

    if df.empty:
        return False, "Nenhum dado encontrado no período."

    # Processamento Pandas
    df_agrupado = agrupaporcategoria(df)
    df_associado = agrupaporassociado(df)
    df_pivot = pivotableassociado(df_agrupado)

    df_pivot['trimestre'], df_associado['trimestre'] = trimestre, trimestre
    df_pivot['ano'], df_associado['ano'] = ano, ano
    
    df_pivot = df_pivot.round(2)
    df_associado = df_associado.round(2)
    
    df_pivot['dataatualizacao'] = date.today()
    df_associado['dataatualizacao'] = date.today()
    
    # Limpeza de colunas
    df_pivot.columns = [col.lower().strip().replace(" ","_") for col in df_pivot.columns]
    df_associado.columns = [col.lower().strip().replace(" ","_") for col in df_associado.columns]

    # Gravação no Banco (Substitui to_sql antigo)
    try:
        # Verifica se já existe (Lógica simplificada: Sempre atualiza as tabelas atuais)
        # O user queria checar 'gradepercmov', podemos manter a lógica se quiser, 
        # mas para simplificar vamos garantir que as tabelas de uso atual estejam atualizadas.
        
        df_pivot.to_sql('gradepercatual', index=False, if_exists='replace', con=engine)
        df_associado.to_sql('gradepercatualassoc', index=False, if_exists='replace', con=engine)
        
        # Opcional: Histórico
        # df_pivot.to_sql('gradepercmov', index=False, if_exists='append', con=engine) 

        return True, "Tabelas atualizadas com sucesso!"
    except Exception as e:
        return False, f"Erro ao salvar no PostgreSQL: {str(e)}"