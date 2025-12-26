from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from utils.db_utils import query_django_raw_sql

def apuracao_grade_view(request: HttpRequest, contrato_id: int) -> HttpResponse:
    """
    View para retornar os dados apurados de uma grade, usando o ID do contrato
    passado via URL e consultando o banco de dados configurado no settings.
    """
    
    sql_query = """
        SELECT 
            *
        FROM 
            grupoeconomico
        WHERE 
            contrato_fk = %s;  /* Usamos %s como placeholder de segurança */
    """
    
    # 1. Prepara os Parâmetros (Lista/Tupla no formato esperado pelo cursor do Django)
    params = [contrato_id]
    
    try:
        # 2. Executa a Query
        # A função cuida de conectar e converter para uma Lista de Dicionários
        registros_apuracao = query_django_raw_sql(sql_query, params)
        
        context = {
            'contrato_id': contrato_id,
            # 'registros_apuracao' agora é uma Lista de Dicionários, ideal para o template
            'registros_apuracao': registros_apuracao,
        }
        
    except Exception as e:
        context = {
            'contrato_id': contrato_id,
            'erro': f"Erro ao executar consulta: {e}"
        }
        
    return render(request, 'apuracao_grade/grade_apuracao.html', context)


def grupoeconomico_view(request: HttpRequest) -> HttpResponse:
    
    
    sql_query = """
        SELECT 
            *
        FROM 
            grupoeconomico
        
    """
    
    
    try:
        
        registros_apuracao = query_django_raw_sql(sql_query, params=None)
        
        conteudo = {
           
            
            'registros_apuracao': registros_apuracao,
        }
        print(registros_apuracao)
        
    except Exception as e:
        conteudo = {
            
            'erro': f"Erro ao executar consulta: {e}"
        }
        
    return render(request, 'apuracao_grade/grupoeconomico.html', conteudo)