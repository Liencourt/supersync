from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from gcp_services.services import bigquery_client
from django.http import JsonResponse

# Create your views here.

@login_required
def buscar_contratos(request):
    """
    Busca, filtra e pagina os contratos a partir do BigQuery.

    Esta view lida com a exibição da lista de contratos, permitindo filtros
    por descrição de subcontrato e nome do contrato. Os resultados são paginados
    e exibidos no template.

    Args:
        request: O objeto HttpRequest do Django. Os seguintes parâmetros GET são utilizados:
            - 'descsub' (str, opcional): Filtro para a descrição do subcontrato.
            - 'desccontrato' (str, opcional): Filtro para o nome do contrato.
            - 'page' (int, opcional): O número da página a ser exibida. Padrão é 1.
            - 'per_page' (int, opcional): Número de registros por página. Padrão é 25.

    Returns:
        HttpResponse: Renderiza o template 'contratos/lista_contratos.html' com o
                      contexto contendo os contratos paginados e informações de filtro.
                      Em caso de erro na consulta, um campo 'erro' é adicionado ao contexto.
    """
    # Captura os parâmetros de filtro e paginação da requisição GET.
    filtro_descsub = request.GET.get('descsub', '').strip()
    filtro_desccontrato = request.GET.get('desccontrato', '').strip()
    page = request.GET.get('page', 1)
    per_page = request.GET.get('per_page', '25')

    # Garante que o valor de 'per_page' seja um inteiro válido.
    try:
        per_page = int(per_page)
        if per_page not in [10, 25, 50, 100, 200]:
            per_page = 25  # Valor padrão se a seleção for inválida
    except ValueError:
        per_page = 25  # Valor padrão se a conversão falhar

    # Query base para selecionar os contratos no BigQuery.
    query = """SELECT nomesubcontrato, 
                      nomecontrato,
                      cast(nrocontrato as int) as nrocontrato, 
                      cast(contrato as int) as contrato, 
                      cast(subcontrato as int) as subcontrato
               FROM `singular-ray-422121`.gold.dim_contrato"""

    # Constrói as cláusulas WHERE dinamicamente com base nos filtros fornecidos.
    condicoes = []
    if filtro_descsub:
        condicoes.append(f"UPPER(nomesubcontrato) LIKE UPPER('%{filtro_descsub}%')")
    if filtro_desccontrato:
        condicoes.append(f"UPPER(nomecontrato) LIKE UPPER('%{filtro_desccontrato}%')")

    if condicoes:
        query += " WHERE " + " AND ".join(condicoes)

    query += " ORDER BY nomesubcontrato;"

    try:
        # Executa a query no BigQuery.
        resultados = bigquery_client.run_query(query)
        
        # Converte os resultados para uma lista de dicionários.
        contratos = [dict(row) for row in resultados] if resultados else []

        # Aplica a paginação aos resultados da consulta.
        paginator = Paginator(contratos, per_page)
        try:
            contratos_paginados = paginator.page(page)
        except PageNotAnInteger:
            # Se a página não for um inteiro, exibe a primeira página.
            contratos_paginados = paginator.page(1)
        except EmptyPage:
            # Se a página estiver fora do intervalo, exibe a última página.
            contratos_paginados = paginator.page(paginator.num_pages)

        context = {
            'contratos': contratos_paginados,
            'total': len(contratos),
            'per_page': per_page,
            'filtros': {
                'descsub': filtro_descsub,
                'desccontrato': filtro_desccontrato,
            }
        }
        return render(request, 'contratos/lista_contratos.html', context)

    except Exception as e:
        # Em caso de erro na execução da query, retorna a página com uma mensagem de erro.
        context = {
            'contratos': [],
            'total': 0,
            'per_page': per_page,
            'erro': f"Ocorreu um erro ao buscar os contratos: {e}",
            'filtros': {
                'descsub': filtro_descsub,
                'desccontrato': filtro_desccontrato,
            }
        }
        return render(request, 'contratos/lista_contratos.html', context)


@login_required
def listar_detalhes_contrato(request, nrosubcontrato):
    """
    Busca e retorna os detalhes de um subcontrato específico em formato JSON.

    Esta view é projetada para ser consumida por chamadas AJAX. Ela busca
    informações detalhadas de um subcontrato, incluindo dados básicos,
    fornecedores associados e produtos vinculados, a partir de múltiplas
    consultas no BigQuery.

    Args:
        request: O objeto HttpRequest do Django.
        nrosubcontrato (int): O número do subcontrato a ser detalhado,
                              capturado da URL.

    Returns:
        JsonResponse: Um objeto JSON contendo:
            - 'success' (bool): True se a busca for bem-sucedida, False caso contrário.
            - 'info_contrato' (dict): Informações básicas do contrato.
            - 'fornecedores' (list): Lista de fornecedores associados.
            - 'produtos' (list): Lista de produtos no contrato.
            - 'erro' (str): Mensagem de erro, presente apenas se 'success' for False.
    """
    # Query para buscar informações básicas do contrato.
    query_contrato = f"""SELECT DISTINCT
                        a.nomecontrato,
                        a.nomesubcontrato,
                        a.percdesconto/100 as percdesconto,
                        a.vlrdescontofixo, 
                        a.dtainiciovalidade, 
                        a.dtafimvalidade,
                        a.subcontrato
                    FROM `singular-ray-422121`.gold.dim_contrato a
                    WHERE a.subcontrato = {nrosubcontrato}"""

    # Query para buscar os fornecedores (redes) associados ao contrato.
    query_fornecedores = f"""SELECT 
                            b.NOMERAZAO,
                            b.FANTASIA,
                            b.cnpj_completo
                        FROM `singular-ray-422121`.gold.dim_contrato a
                        LEFT JOIN `singular-ray-422121`.gold.dim_fornecedor b ON a.seqrede = b.SEQREDE
                        WHERE a.subcontrato = {nrosubcontrato}
                        AND b.cnpj_completo IS NOT NULL"""

    # Query para buscar os produtos incluídos no contrato.
    query_produtos = f"""SELECT  
                        cast(a.SEQPRODUTO AS int) as SEQPRODUTO, 
                        b.DESCCOMPLETA 
                    FROM `singular-ray-422121`.gold.dim_produto_por_contrato a 
                    left join (SELECT DISTINCT SEQPRODUTO, DESCCOMPLETA
                               FROM `singular-ray-422121`.gold.dim_produto) as b on a.SEQPRODUTO = b.seqproduto
                    where seqidentificador={nrosubcontrato}
                    ORDER BY b.DESCCOMPLETA
                    limit 10;"""

    try:
        # Executa as queries e processa os resultados.
        resultado_contrato = bigquery_client.run_query(query_contrato)
        info_contrato = dict(resultado_contrato[0]) if resultado_contrato else {}

        resultado_fornecedores = bigquery_client.run_query(query_fornecedores)
        fornecedores = [dict(row) for row in resultado_fornecedores] if resultado_fornecedores else []

        resultado_produtos = bigquery_client.run_query(query_produtos)
        produtos = [dict(row) for row in resultado_produtos] if resultado_produtos else []

        # Retorna os dados consolidados em uma resposta JSON.
        return JsonResponse({
            'success': True,
            'info_contrato': info_contrato,
            'fornecedores': fornecedores,
            'produtos': produtos,
            'nrosubcontrato': nrosubcontrato
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'erro': f"Ocorreu um erro ao detalhar o contrato: {e}",
            'nrosubcontrato': nrosubcontrato
        }, status=500)
