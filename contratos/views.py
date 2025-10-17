from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from gcp_services.services import bigquery_client
from django.http import JsonResponse

# Create your views here.

@login_required
def buscar_contratos(request):
    # Captura os filtros do GET
    filtro_descsub = request.GET.get('descsub', '').strip()
    filtro_desccontrato = request.GET.get('desccontrato', '').strip()
    # filtro_cnpj = request.GET.get('cnpj', '').strip()

    # Captura a página atual e o número de registros por página
    page = request.GET.get('page', 1)
    per_page = request.GET.get('per_page', '25')  # Default: 25 registros

    # Valida o número de registros por página
    try:
        per_page = int(per_page)
        if per_page not in [10, 25, 50, 100, 200]:
            per_page = 25
    except ValueError:
        per_page = 25

    # Monta a query base
    query = """SELECT nomesubcontrato, 
                      nomecontrato,
                      cast(nrocontrato as int) as nrocontrato, 
                      cast(contrato as int) as contrato, 
                      cast(subcontrato as int) as subcontrato,
                      
                      
               FROM `singular-ray-422121`.gold.dim_contrato"""

    # Lista para armazenar as condições WHERE
    condicoes = []

    # Adiciona filtros se foram fornecidos
    if filtro_descsub:
        condicoes.append(f"UPPER(nomesubcontrato) LIKE UPPER('%{filtro_descsub}%')")

    if filtro_desccontrato:
        condicoes.append(f"UPPER(nomecontrato) LIKE UPPER('%{filtro_desccontrato}%')")

    # if filtro_cnpj:
    #     # Remove caracteres especiais do CNPJ para busca
    #     cnpj_limpo = filtro_cnpj.replace('.', '').replace('/', '').replace('-', '')
    #     condicoes.append(f"REPLACE(REPLACE(REPLACE(cnpj_completo, '.', ''), '/', ''), '-', '') LIKE '%{cnpj_limpo}%'")

    # Adiciona as condições à query se houver filtros
    if condicoes:
        query += " WHERE " + " AND ".join(condicoes)

    # Adiciona ordenação
    query += " ORDER BY nomesubcontrato;"

    try:
        resultados = bigquery_client.run_query(query)

        # Converte os resultados para lista de dicionários
        contratos = []
        if resultados:
            for row in resultados:
                contratos.append(dict(row))


        # Implementa a paginação
        paginator = Paginator(contratos, per_page)

        try:
            contratos_paginados = paginator.page(page)
        except PageNotAnInteger:
            contratos_paginados = paginator.page(1)
        except EmptyPage:
            contratos_paginados = paginator.page(paginator.num_pages)

        context = {
            'contratos': contratos_paginados,
            'total': len(contratos),
            'per_page': per_page,
            'filtros': {
                'descsub': filtro_descsub,
                'desccontrato': filtro_desccontrato,
                # 'cnpj': filtro_cnpj,
            }
        }

        return render(request, 'contratos/lista_contratos.html', context)

    except Exception as e:
        context = {
            'contratos': [],
            'total': 0,
            'per_page': per_page,
            'erro': str(e),
            'filtros': {
                'descsub': filtro_descsub,
                'desccontrato': filtro_desccontrato,
                # 'cnpj': filtro_cnpj,
            }
        }
        return render(request, 'contratos/lista_contratos.html', context)


@login_required
def listar_detalhes_contrato(request, nrosubcontrato):
    # Query para informações básicas do contrato (sem duplicação)
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

    # Query separada para fornecedores/CNPJs
    query_fornecedores = f"""SELECT 
                            b.NOMERAZAO,
                            b.FANTASIA,
                            b.cnpj_completo
                        FROM `singular-ray-422121`.gold.dim_contrato a
                        LEFT JOIN `singular-ray-422121`.gold.dim_fornecedor b ON a.seqrede = b.SEQREDE
                        WHERE a.subcontrato = {nrosubcontrato}
                        AND b.cnpj_completo IS NOT NULL"""

    query_produtos = f"""SELECT  
                        cast(a.SEQPRODUTO AS int) as SEQPRODUTO, 
                        b.DESCCOMPLETA 
                    FROM `singular-ray-422121`.gold.dim_produto_por_contrato a 
                    left join (SELECT DISTINCT  SEQPRODUTO, DESCCOMPLETA,
                    FROM `singular-ray-422121`.gold.dim_produto )  as b on a.SEQPRODUTO = b.seqproduto
                    where seqidentificador={nrosubcontrato}
                    ORDER BY b.DESCCOMPLETA
                    limit 10;"""

    try:
        # Busca informações do contrato
        resultado_contrato = bigquery_client.run_query(query_contrato)
        info_contrato = dict(resultado_contrato[0]) if resultado_contrato else {}

        # Busca lista de fornecedores
        resultado_fornecedores = bigquery_client.run_query(query_fornecedores)
        fornecedores = []
        if resultado_fornecedores:
            for row in resultado_fornecedores:
                fornecedores.append(dict(row))

        # Busca lista de produtos
        resultado_produtos = bigquery_client.run_query(query_produtos)
        produtos = []
        if resultado_produtos:
            for row in resultado_produtos:
                produtos.append(dict(row))

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
            'erro': str(e),
            'nrosubcontrato': nrosubcontrato
        }, status=500)