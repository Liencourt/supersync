from django.db import connection
from typing import Optional, List, Any, Dict

def query_django_raw_sql(sql: str, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
    """
    Executa uma consulta SQL bruta usando a conexão do Django
    e retorna os resultados como uma lista de dicionários.
    """
    if params is None:
        params = {}
        
    with connection.cursor() as cursor:
        cursor.execute(sql, params)
                
        # Obtém os nomes das colunas
        columns = [col[0] for col in cursor.description]
        
        # Pega todos os resultados
        data = cursor.fetchall()
        
        # Converte a lista de tuplas para uma lista de dicionários
        results = [
            dict(zip(columns, row))
            for row in data
        ]
        
        return results