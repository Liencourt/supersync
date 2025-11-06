from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from gcp_services.services import bigquery_client
from decimal import Decimal

@login_required
def apuracao(request):
    context = {
        'has_data': False,
        'entradas': {},
        'devolucoes': {},
        'summary': {
            'entradas': 'R$ 0,00',
            'devolucoes': 'R$ 0,00',
            'final': 'R$ 0,00'
        }
    }

    try:
        distinct_contratos_query = "SELECT DISTINCT nomesubcontrato FROM `singular-ray-422121`.gold.obt_tb_apuracao_contrato ORDER BY nomesubcontrato"
        distinct_contracts_results = bigquery_client.run_query(distinct_contratos_query)
        context['contract_names'] = [row['nomesubcontrato'] for row in distinct_contracts_results]
    except Exception as e:
        print(f"Ocorreu um erro ao buscar os nomes dos contratos: {e}")
        context['contract_names'] = []

    if request.method == 'GET' and 'data_inicio' in request.GET:
        dtini = request.GET.get('data_inicio')
        dtfim = request.GET.get('data_fim')
        nomesubcontrato = request.GET.get('contract_name_input')

        if dtini and dtfim and nomesubcontrato:
            query = f"""
                SELECT data_emissao, NomeAssociado, Nome_Produto, Nome_Fornecedor, nro_nota_fiscal, tipo_nota_fiscal, 
                       CAST(QtdCompra AS NUMERIC) as QtdCompra, CAST(valorbruto_comipi AS NUMERIC) as valorbruto_comipi
                FROM `singular-ray-422121`.gold.obt_tb_apuracao_contrato
                WHERE nomesubcontrato = '{nomesubcontrato}' AND data_emissao BETWEEN '{dtini}' AND '{dtfim}'
            """
            try:
                results = bigquery_client.run_query(query)
                if results:
                    context['has_data'] = True
                    entradas_data = {}
                    devolucoes_data = {}
                    total_entradas = Decimal(0)
                    total_devolucoes = Decimal(0)

                    for row in results:
                        valor_bruto = Decimal(row.get('valorbruto_comipi') or 0)
                        qtd = Decimal(row.get('QtdCompra') or 0)
                        associado = row.get('NomeAssociado')
                        nota = row.get('nro_nota_fiscal')
                        produto = {
                            'nome': row.get('Nome_Produto'),
                            'fornecedor': row.get('Nome_Fornecedor'),
                            'quantidade': qtd,
                            'valor': valor_bruto
                        }

                        target_data = entradas_data if row.get('tipo_nota_fiscal') == 'R' else devolucoes_data
                        if row.get('tipo_nota_fiscal') == 'R':
                            total_entradas += valor_bruto
                        else:
                            total_devolucoes += valor_bruto

                        # Associado Level
                        if associado not in target_data:
                            target_data[associado] = {'total': Decimal(0), 'quantidade': Decimal(0), 'notas': {}}
                        target_data[associado]['total'] += valor_bruto
                        target_data[associado]['quantidade'] += qtd

                        # Nota Level
                        if nota not in target_data[associado]['notas']:
                            target_data[associado]['notas'][nota] = {'total': Decimal(0), 'quantidade': Decimal(0), 'produtos': [], 'data_emissao': row.get('data_emissao')}
                        target_data[associado]['notas'][nota]['total'] += valor_bruto
                        target_data[associado]['notas'][nota]['quantidade'] += qtd
                        target_data[associado]['notas'][nota]['produtos'].append(produto)

                    context['entradas'] = entradas_data
                    context['devolucoes'] = devolucoes_data
                    valor_liquido = total_entradas - total_devolucoes
                    
                    context['summary']['entradas'] = f"R$ {total_entradas:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
                    context['summary']['devolucoes'] = f"R$ {total_devolucoes:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
                    context['summary']['final'] = f"R$ {valor_liquido:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

            except Exception as e:
                print(f"Ocorreu um erro ao buscar os contratos: {e}")
                context['error_message'] = "Ocorreu um erro ao processar sua solicitação."
            
    return render(request, 'apuracao_contrato/apuracao_contrato.html', context)
