# Documentação: Este módulo é o ponto central para todas as interações
# com o Google BigQuery. Qualquer parte da aplicação que precisar de dados
# do BigQuery deve usar as funções daqui.

from google.cloud import bigquery
from django.conf import settings
import pandas as pd

def _get_client():
    """
    Função privada para criar e retornar um cliente BigQuery autenticado.
    O underscore (_) no início indica que ela deve ser usada apenas dentro deste módulo.
    """
    credentials_path = settings.GOOGLE_APPLICATION_CREDENTIALS
    return bigquery.Client.from_service_account_json(credentials_path)

def run_query(query: str) -> list | None:
    """
    Executa uma consulta SQL no BigQuery e retorna os resultados.

    Args:
        query (str): A string da consulta SQL a ser executada.

    Returns:
        Uma lista de dicionários representando as linhas do resultado,
        ou None se ocorrer um erro.
    """
    try:
        client = _get_client()
        query_job = client.query(query)
        # O to_dataframe é muito eficiente para lidar com os resultados
        results_df = query_job.to_dataframe()
        return results_df.to_dict('records')
    except Exception as e:
        # No futuro, podemos adicionar um log de erro aqui
        print(f"Erro no serviço BigQuery: {e}")
        return None