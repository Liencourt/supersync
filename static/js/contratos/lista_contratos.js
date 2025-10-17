// static/js/contratos/lista_contratos.js

// static/js/contratos/lista_contratos.js

// Função para formatar data no formato dd/mm/yyyy
function formatarData(dataString) {
    if (!dataString) return '-';

    try {
        // Remove timezone se existir
        const data = new Date(dataString.split(' ')[0]);

        // Verifica se é uma data válida
        if (isNaN(data.getTime())) {
            return dataString; // Retorna original se não for data válida
        }

        const dia = String(data.getDate()).padStart(2, '0');
        const mes = String(data.getMonth() + 1).padStart(2, '0');
        const ano = data.getFullYear();

        return `${dia}/${mes}/${ano}`;
    } catch (error) {
        console.error('Erro ao formatar data:', error);
        return dataString; // Retorna original em caso de erro
    }
}

// Função para formatar valores monetários
function formatarMoeda(valor) {
    if (!valor) return '-';

    try {
        return new Intl.NumberFormat('pt-BR', {
            style: 'currency',
            currency: 'BRL'
        }).format(parseFloat(valor));
    } catch (error) {
        console.error('Erro ao formatar moeda:', error);
        return valor;
    }
}

// Função para formatar porcentagem
function formatarPorcentagem(valor) {
    if (!valor) return '-';

    try {
        const porcentagem = parseFloat(valor) * 100;
        return `${porcentagem.toFixed(2)}%`;
    } catch (error) {
        console.error('Erro ao formatar porcentagem:', error);
        return valor;
    }
}

// Função para abrir o modal e carregar os detalhes
function abrirDetalhes(nrosubcontrato) {
    const modal = new bootstrap.Modal(document.getElementById('detalhesModal'));
    const conteudo = document.getElementById('detalhesConteudo');
    const subtitle = document.getElementById('modalSubtitle');

    // Atualiza o subtítulo
    subtitle.textContent = `SubContrato: ${nrosubcontrato}`;

    // Mostra o loading
    conteudo.innerHTML = `
        <div class="loading-spinner">
            <div class="spinner-container">
                <div class="spinner-border text-primary" role="status" style="width: 3rem; height: 3rem;">
                    <span class="visually-hidden">Carregando...</span>
                </div>
                <p class="mt-3" style="color: var(--gray-medium); font-size: 1.1rem;">Carregando detalhes do contrato...</p>
            </div>
        </div>
    `;

    // Abre o modal
    modal.show();

    // Faz a requisição AJAX
    fetch(`/contratos/detalhes/${nrosubcontrato}/`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                let html = `
                    <div class="detalhes-info">
                        <i class="fas fa-hashtag"></i>
                        <strong>SubContrato: ${data.nrosubcontrato}</strong>
                    </div>
                `;

                if (data.info_contrato) {
                    const contrato = data.info_contrato;

                    // Formata as datas e valores
                    const dataInicio = formatarData(contrato.dtainiciovalidade);
                    const dataFim = formatarData(contrato.dtafimvalidade);
                    const valorDesconto = formatarMoeda(contrato.vlrdescontofixo);
                    const percentual = formatarPorcentagem(contrato.percdesconto);

                    // Informações básicas do contrato
                    html += `
                        <div class="detalhes-grid">
                            <div class="detalhe-item">
                                <div class="detalhe-label">
                                    <i class="fas fa-file-signature me-2"></i>
                                    Nome do Contrato
                                </div>
                                <div class="detalhe-value">${contrato.nomecontrato || '-'}</div>
                            </div>
                            <div class="detalhe-item">
                                <div class="detalhe-label">
                                    <i class="fas fa-file-contract me-2"></i>
                                    Nome do SubContrato
                                </div>
                                <div class="detalhe-value">${contrato.nomesubcontrato || '-'}</div>
                            </div>
                            <div class="detalhe-item">
                                <div class="detalhe-label">
                                    <i class="fas fa-percentage me-2"></i>
                                    Percentual de Desconto
                                </div>
                                <div class="detalhe-value">${percentual}</div>
                            </div>
                            <div class="detalhe-item">
                                <div class="detalhe-label">
                                    <i class="fas fa-money-bill-wave me-2"></i>
                                    Valor Desconto Fixo
                                </div>
                                <div class="detalhe-value">${valorDesconto}</div>
                            </div>
                            <div class="detalhe-item">
                                <div class="detalhe-label">
                                    <i class="fas fa-calendar-check me-2"></i>
                                    Data Início Validade
                                </div>
                                <div class="detalhe-value">${dataInicio}</div>
                            </div>
                            <div class="detalhe-item">
                                <div class="detalhe-label">
                                    <i class="fas fa-calendar-times me-2"></i>
                                    Data Fim Validade
                                </div>
                                <div class="detalhe-value">${dataFim}</div>
                            </div>
                        </div>
                    `;
                }

                // ... (restante do código para fornecedores e produtos permanece igual)
                // Tabela de fornecedores/CNPJs
                if (data.fornecedores && data.fornecedores.length > 0) {
                    html += `
                        <div class="fornecedores-section">
                            <h6 class="section-title">
                                <i class="fas fa-building me-2"></i>
                                Fornecedores Vinculados
                            </h6>
                            <div class="table-responsive">
                                <table class="fornecedores-table">
                                    <thead>
                                        <tr>
                                            <th><i class="fas fa-building me-2"></i>Razão Social</th>
                                            <th><i class="fas fa-store me-2"></i>Nome Fantasia</th>
                                            <th><i class="fas fa-id-card me-2"></i>CNPJ</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                    `;

                    data.fornecedores.forEach(fornecedor => {
                        const cnpjFormatado = fornecedor.cnpj_completo ?
                            fornecedor.cnpj_completo.replace(/(\d{2})(\d{3})(\d{3})(\d{4})(\d{2})/, "$1.$2.$3/$4-$5") :
                            '-';

                        html += `
                            <tr>
                                <td>${fornecedor.NOMERAZAO || '-'}</td>
                                <td>${fornecedor.FANTASIA || '-'}</td>
                                <td class="cnpj-cell">${cnpjFormatado}</td>
                            </tr>
                        `;
                    });

                    html += `
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    `;
                } else {
                    html += `
                        <div class="empty-fornecedores">
                            <i class="fas fa-info-circle"></i>
                            <div>
                                <strong>Nenhum fornecedor encontrado</strong>
                                <p class="mb-0">Não foram encontrados fornecedores vinculados a este contrato.</p>
                            </div>
                        </div>
                    `;
                }

                // Tabela de Produtos
                if (data.produtos && data.produtos.length > 0) {
                    html += `
                        <div class="produtos-section">
                            <h6 class="section-title">
                                <i class="fas fa-boxes me-2"></i>
                                Produtos Vinculados
                            </h6>
                            <div class="table-responsive">
                                <table class="produtos-table">
                                    <thead>
                                        <tr>
                                            <th><i class="fas fa-barcode me-2"></i>Código</th>
                                            <th><i class="fas fa-box me-2"></i>Produto</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                    `;

                    data.produtos.forEach(produto => {
                        html += `
                            <tr>
                                <td><strong>${produto.SEQPRODUTO || '-'}</strong></td>
                                <td>${produto.DESCCOMPLETA || '-'}</td>
                            </tr>
                        `;
                    });

                    html += `
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    `;
                } else {
                    html += `
                        <div class="empty-produtos">
                            <i class="fas fa-info-circle"></i>
                            <div>
                                <strong>Nenhum Produto encontrado</strong>
                                <p class="mb-0">Não foram encontrados Produtos vinculados a este contrato.</p>
                            </div>
                        </div>
                    `;
                }

                conteudo.innerHTML = html;
            } else {
                conteudo.innerHTML = `
                    <div class="erro-mensagem">
                        <i class="fas fa-exclamation-triangle"></i>
                        <div>
                            <strong>Erro ao carregar detalhes</strong>
                            <p class="mb-0">${data.erro || 'Ocorreu um erro desconhecido.'}</p>
                        </div>
                    </div>
                `;
            }
        })
        .catch(error => {
            conteudo.innerHTML = `
                <div class="erro-mensagem">
                    <i class="fas fa-exclamation-triangle"></i>
                    <div>
                        <strong>Erro ao carregar detalhes</strong>
                        <p class="mb-0">Não foi possível conectar ao servidor. Tente novamente.</p>
                    </div>
                </div>
            `;
            console.error('Erro:', error);
        });
}



// Função para mudar o número de registros por página
function changePerPage(value) {
    const urlParams = new URLSearchParams(window.location.search);
    urlParams.set('per_page', value);
    urlParams.set('page', '1');
    window.location.search = urlParams.toString();
}

// Inicialização quando o documento carrega
document.addEventListener('DOMContentLoaded', function() {
    // Animação para o toggle dos filtros
    const btnToggle = document.querySelector('.btn-toggle');
    if (btnToggle) {
        btnToggle.addEventListener('click', function() {
            const toggleIcon = this.querySelector('.toggle-icon');
            if (toggleIcon) {
                toggleIcon.classList.toggle('fa-chevron-up');
                toggleIcon.classList.toggle('fa-chevron-down');
            }
        });
    }

    // Efeito hover nas linhas da tabela
    document.querySelectorAll('.table-row').forEach(row => {
        row.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-1px)';
        });

        row.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });
});