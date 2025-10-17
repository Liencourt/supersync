// static/js/apuracao_contrato/apuracao_contrato.js

class ApuracaoContrato {
    constructor() {
        this.estados = {
            INICIAL: 'inicial',
            CARREGANDO: 'carregando',
            DADOS: 'dados',
            VAZIO: 'vazio'
        };
        this.estadoAtual = this.estados.INICIAL;
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.mostrarEstado(this.estados.INICIAL);
    }

    // --- GERENCIAMENTO DE ESTADOS ---
    mostrarEstado(estado) {
        // Esconder todos os estados
        document.querySelectorAll('.estado-container').forEach(container => {
            container.classList.add('hidden');
        });

        // Mostrar estado específico
        const elementoEstado = document.getElementById(`estado-${estado}`);
        if (elementoEstado) {
            elementoEstado.classList.remove('hidden');
        }

        this.estadoAtual = estado;
        this.atualizarBotoes();
    }

    atualizarBotoes() {
        const btnGravar = document.getElementById('open-save-modal-btn');
        const btnApurar = document.getElementById('btn-apurar');

        if (this.estadoAtual === this.estados.DADOS) {
            btnGravar.disabled = false;
            btnApurar.disabled = false;
        } else {
            btnGravar.disabled = true;
            btnApurar.disabled = false;
        }
    }

    // --- VALIDAÇÃO DE FORMULÁRIO ---
    validarFormulario() {
        const dataInicio = document.getElementById('data-inicio').value;
        const dataFim = document.getElementById('data-fim').value;
        const contrato = document.getElementById('contract-name-input').value;

        if (!dataInicio || !dataFim || !contrato) {
            this.mostrarMensagem('Por favor, preencha todos os campos obrigatórios.', 'warning');
            return false;
        }

        if (new Date(dataInicio) > new Date(dataFim)) {
            this.mostrarMensagem('A data de início não pode ser maior que a data fim.', 'warning');
            return false;
        }

        return true;
    }

    mostrarMensagem(mensagem, tipo = 'info') {
        // Você pode implementar um sistema de toast/mensagens aqui
        alert(mensagem); // Temporário - substitua por um sistema de mensagens bonito
    }

    // --- PROCESSO DE APURAÇÃO ---
    async processarApuracao() {
        if (!this.validarFormulario()) {
            return;
        }

        this.mostrarEstado(this.estados.CARREGANDO);

        try {
            // Simular delay de rede
            await new Promise(resolve => setTimeout(resolve, 1500));

            // Aqui você fará a chamada para sua API Django
            const dados = await this.buscarDadosApuracao();

            if (dados && dados.possuiRegistros) {
                this.carregarDados(dados);
                this.mostrarEstado(this.estados.DADOS);
            } else {
                this.mostrarEstado(this.estados.VAZIO);
            }
        } catch (error) {
            console.error('Erro na apuração:', error);
            this.mostrarMensagem('Erro ao processar apuração. Tente novamente.', 'error');
            this.mostrarEstado(this.estados.INICIAL);
        }
    }

    async buscarDadosApuracao() {
        // MOCK - Substitua pela chamada real à sua API Django
        const dataInicio = document.getElementById('data-inicio').value;
        const dataFim = document.getElementById('data-fim').value;
        const contrato = document.getElementById('contract-name-input').value;

        // Simulação de busca - na implementação real, faça fetch para sua view
        return {
            possuiRegistros: true,
            contrato: contrato,
            periodo: { dataInicio, dataFim },
            entradas: this.getMockEntradasHTML(),
            devolucoes: this.getMockDevolucoesHTML(),
            totais: {
                entradas: 4830.75,
                devolucoes: 565.75,
                liquido: 4265.00
            }
        };
    }

    carregarDados(dados) {
        // Carregar tabelas
        document.getElementById('table-entradas').innerHTML = dados.entradas;
        document.getElementById('table-devolucoes').innerHTML = dados.devolucoes;

        // Atualizar totais
        document.getElementById('summary-entradas').textContent = this.formatAsBRL(dados.totais.entradas);
        document.getElementById('summary-devolucoes').textContent = this.formatAsBRL(dados.totais.devolucoes);
        document.getElementById('summary-final').textContent = this.formatAsBRL(dados.totais.liquido);

        // Configurar cálculos
        this.setupTableCalculations();
    }

    voltarParaInicio() {
        this.mostrarEstado(this.estados.INICIAL);
        this.limparFormulario();
    }

    limparFormulario() {
        document.getElementById('data-inicio').value = '';
        document.getElementById('data-fim').value = '';
        document.getElementById('contract-name-input').value = '';
    }

    // --- EVENT LISTENERS ---
    setupEventListeners() {
        // Toggle icons (expand/collapse) - delegated
        document.body.addEventListener('click', (e) => {
            if (e.target.classList.contains('toggle-icon')) {
                this.handleToggleClick(e.target);
            }
        });

        // Botão apurar
        const btnApurar = document.getElementById('btn-apurar');
        if (btnApurar) {
            btnApurar.addEventListener('click', () => {
                this.processarApuracao();
            });
        }

        // Checkboxes "marcar todos" - delegated
        document.body.addEventListener('change', (e) => {
            if (e.target.classList.contains('check-all')) {
                this.toggleAllCheckboxes(e.target);
            }
        });

        // Enter nos campos executa apuração
        document.querySelectorAll('.filter-group input').forEach(input => {
            input.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    this.processarApuracao();
                }
            });
        });

        // Tabs - delegated
        document.body.addEventListener('click', (e) => {
            if (e.target.classList.contains('tab-button')) {
                this.handleTabClick(e.target);
            }
        });

        // Modal
        this.setupModal();
    }

    // Métodos de cálculo de tabela
    setupTableCalculations() {
        document.body.addEventListener('input', (e) => {
            if (e.target.classList.contains('valor-acordado')) {
                this.calcularValores(e.target);
            }
        });
    }

    calcularValores(inputElement) {
        const row = inputElement.closest('tr');
        const valorOriginal = this.parseBRL(row.querySelector('.valor-original').textContent);
        const valorAcordado = parseFloat(inputElement.value) || 0;
        const valorCalculado = valorAcordado > 0 ? valorAcordado : valorOriginal;

        row.querySelector('.valor-calculado').textContent = this.formatAsBRL(valorCalculado);
        this.atualizarTotais();
    }

    formatAsBRL(value) {
        return new Intl.NumberFormat('pt-BR', {
            style: 'currency',
            currency: 'BRL'
        }).format(value);
    }

    parseBRL(value) {
        return parseFloat(value.replace('R$', '').replace('.', '').replace(',', '.').trim()) || 0;
    }

    toggleAllCheckboxes(checkboxElement) {
        const associateId = checkboxElement.dataset.associateId;
        const isChecked = checkboxElement.checked;
        
        // Marcar/desmarcar todos os checkboxes do associado
        document.querySelectorAll(`.check-invoice[data-associate-id="${associateId}"]`).forEach(checkbox => {
            checkbox.checked = isChecked;
        });
    }

    atualizarTotais() {
        // Atualizar totais de cada associado
        document.querySelectorAll('.associate-total-row').forEach(totalRow => {
            const associateId = totalRow.dataset.associateId;
            const invoiceRows = document.querySelectorAll(`.invoice-row[data-parent-associate="${associateId}"]`);
            
            let totalOriginal = 0;
            let totalAcordado = 0;
            let totalCalculado = 0;

            invoiceRows.forEach(row => {
                if (!row.classList.contains('hidden')) {
                    totalOriginal += this.parseBRL(row.querySelector('.valor-original').textContent);
                    const inputAcordado = row.querySelector('.valor-acordado input');
                    if (inputAcordado && inputAcordado.value) {
                        totalAcordado += parseFloat(inputAcordado.value) || 0;
                    }
                    totalCalculado += this.parseBRL(row.querySelector('.valor-calculado').textContent);
                }
            });

            totalRow.querySelector('.total-original').textContent = this.formatAsBRL(totalOriginal);
            totalRow.querySelector('.total-acordado').textContent = this.formatAsBRL(totalAcordado);
            totalRow.querySelector('.total-calculado').textContent = this.formatAsBRL(totalCalculado);
        });

        // Atualizar totais de contrato
        document.querySelectorAll('.contract-total-row').forEach(contractRow => {
            const contractId = contractRow.querySelector('.toggle-icon').dataset.targetId;
            const associateRows = document.querySelectorAll(`.associate-total-row[data-parent-contract="${contractId}"]`);
            
            let totalOriginal = 0;
            let totalAcordado = 0;
            let totalCalculado = 0;

            associateRows.forEach(row => {
                totalOriginal += this.parseBRL(row.querySelector('.total-original').textContent);
                totalAcordado += this.parseBRL(row.querySelector('.total-acordado').textContent);
                totalCalculado += this.parseBRL(row.querySelector('.total-calculado').textContent);
            });

            contractRow.querySelector('.total-original').textContent = this.formatAsBRL(totalOriginal);
            contractRow.querySelector('.total-acordado').textContent = this.formatAsBRL(totalAcordado);
            contractRow.querySelector('.total-calculado').textContent = this.formatAsBRL(totalCalculado);
        });

        // Atualizar resumo geral
        this.atualizarResumoGeral();
    }

    atualizarResumoGeral() {
        // Calcular total de entradas
        let totalEntradas = 0;
        document.querySelectorAll('#table-entradas .contract-total-row .total-calculado').forEach(el => {
            totalEntradas += this.parseBRL(el.textContent);
        });

        // Calcular total de devoluções
        let totalDevolucoes = 0;
        document.querySelectorAll('#table-devolucoes .contract-total-row .total-calculado').forEach(el => {
            totalDevolucoes += this.parseBRL(el.textContent);
        });

        // Atualizar resumo
        document.getElementById('summary-entradas').textContent = this.formatAsBRL(totalEntradas);
        document.getElementById('summary-devolucoes').textContent = this.formatAsBRL(totalDevolucoes);
        document.getElementById('summary-final').textContent = this.formatAsBRL(totalEntradas - totalDevolucoes);
    }

    handleToggleClick(icon) {
        const level = icon.dataset.targetLevel;
        const id = icon.dataset.targetId;
        const isExpanding = icon.textContent === '+';
        icon.textContent = isExpanding ? '−' : '+';

        let selector = `[data-parent-${level}="${id}"]`;
        document.querySelectorAll(selector).forEach(child => {
            child.classList.toggle('hidden', !isExpanding);
        });

        if (!isExpanding && level !== 'invoice') {
            this.collapseChildren(selector);
        }
    }

    collapseChildren(parentSelector) {
        const childrenIcons = document.querySelectorAll(`${parentSelector} .toggle-icon`);
        childrenIcons.forEach(childIcon => {
            childIcon.textContent = '+';
            const grandchildSelector = `[data-parent-${childIcon.dataset.targetLevel}="${childIcon.dataset.targetId}"]`;
            document.querySelectorAll(grandchildSelector).forEach(gc => gc.classList.add('hidden'));
        });
    }

    handleTabClick(tabButton) {
        const tabId = tabButton.dataset.tab;
        document.querySelectorAll('.tab-button, .tab-content').forEach(el => {
            el.classList.remove('active');
        });
        tabButton.classList.add('active');
        document.getElementById(tabId).classList.add('active');
    }

    setupModal() {
        const modal = document.getElementById('save-modal');
        const openModalBtn = document.getElementById('open-save-modal-btn');
        const closeModalElements = document.querySelectorAll('#close-modal-btn, #cancel-save-btn');

        openModalBtn.addEventListener('click', () => this.openModal());
        closeModalElements.forEach(el => el.addEventListener('click', () => this.closeModal()));

        modal.addEventListener('click', (e) => {
            if (e.target === modal) this.closeModal();
        });

        document.getElementById('confirm-save-btn').addEventListener('click', () => {
            this.confirmSave();
        });

        window.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') this.closeModal();
        });
    }

    openModal() {
        const modal = document.getElementById('save-modal');
        document.getElementById('modal-contract-name').textContent =
            document.getElementById('contract-name-input').value;
        document.getElementById('modal-summary-entradas').textContent =
            document.getElementById('summary-entradas').textContent;
        document.getElementById('modal-summary-devolucoes').textContent =
            document.getElementById('summary-devolucoes').textContent;
        document.getElementById('modal-summary-final').textContent =
            document.getElementById('summary-final').textContent;
        modal.style.display = 'flex';
    }

    closeModal() {
        document.getElementById('save-modal').style.display = 'none';
    }

    confirmSave() {
        alert('Apuração gravada com sucesso!');
        this.closeModal();
    }

    // --- MOCK DATA ---
    loadMockData() {
        const mockEntradasHTML = this.getMockEntradasHTML();
        const mockDevolucoesHTML = this.getMockDevolucoesHTML();

        document.getElementById('table-entradas').innerHTML = mockEntradasHTML;
        document.getElementById('table-devolucoes').innerHTML = mockDevolucoesHTML;

        // Re-inicializar cálculos após carregar mock data
        this.setupTableCalculations();
    }

    getMockEntradasHTML() {
        return `<thead><tr><th style="width: 5%;">OK?</th> <th style="width: 30%;">Descrição</th> <th style="width: 10%;">Emissão</th><th class="text-right" style="width: 15%;">Valor Original</th><th class="text-right" style="width: 15%;">Valor Acordado</th><th class="text-right" style="width: 15%;">Valor Calculado</th><th style="width: 10%;">Obs.</th></tr></thead>
<tbody>
  <tr class="contract-total-row">
    <td></td>
    <td><span class="toggle-icon" data-target-level="contract" data-target-id="c1">+</span>TOTAL ENTRADAS - CONTRATO A</td>
    <td></td>
    <td class="text-right total-original">0,00</td>
    <td class="text-right total-acordado">0,00</td>
    <td class="text-right total-calculado">0,00</td>
    <td></td>
  </tr>

  <!-- Associado A1 -->
  <tr class="associate-header-row hidden" data-parent-contract="c1">
    <td><input class="check-all checkbox-ok" data-associate-id="a1" type="checkbox"></td>
    <td><span class="toggle-icon" data-target-level="associate" data-target-id="a1">+</span>Associado A1 - Loja Matriz</td>
    <td colspan="5"></td>
  </tr>
  <tr class="invoice-row hidden" data-parent-associate="a1">
    <td><input class="check-invoice checkbox-ok" data-associate-id="a1" type="checkbox"></td>
    <td><span class="toggle-icon" data-target-level="invoice" data-target-id="nf101">+</span> NF 12345</td>
    <td>01/10/2025</td>
    <td class="valor-original text-right">1.500,00</td>
    <td class="valor-acordado"><input step="0.01" type="number"></td>
    <td class="valor-calculado text-right">0,00</td>
    <td><input style="width: 100%;" type="text"></td>
  </tr>
  <tr class="invoice-row hidden" data-parent-associate="a1">
    <td><input class="check-invoice checkbox-ok" data-associate-id="a1" type="checkbox"></td>
    <td><span class="toggle-icon" data-target-level="invoice" data-target-id="nf102">+</span> NF 12346</td>
    <td>05/10/2025</td>
    <td class="valor-original text-right">2.350,00</td>
    <td class="valor-acordado"><input step="0.01" type="number"></td>
    <td class="valor-calculado text-right">0,00</td>
    <td><input style="width: 100%;" type="text"></td>
  </tr>
  <tr class="associate-total-row hidden" data-parent-contract="c1" data-associate-id="a1">
    <td colspan="3">TOTAL DO ASSOCIADO:</td>
    <td class="total-original">0,00</td>
    <td class="total-acordado">0,00</td>
    <td class="total-calculado">0,00</td>
    <td></td>
  </tr>

  <!-- Associado A2 -->
  <tr class="associate-header-row hidden" data-parent-contract="c1">
    <td><input class="check-all checkbox-ok" data-associate-id="a2" type="checkbox"></td>
    <td><span class="toggle-icon" data-target-level="associate" data-target-id="a2">+</span>Associado A2 - Filial Sul</td>
    <td colspan="5"></td>
  </tr>
  <tr class="invoice-row hidden" data-parent-associate="a2">
    <td><input class="check-invoice checkbox-ok" data-associate-id="a2" type="checkbox"></td>
    <td><span class="toggle-icon" data-target-level="invoice" data-target-id="nf201">+</span> NF 22301</td>
    <td>08/10/2025</td>
    <td class="valor-original text-right">980,75</td>
    <td class="valor-acordado"><input step="0.01" type="number"></td>
    <td class="valor-calculado text-right">0,00</td>
    <td><input style="width: 100%;" type="text"></td>
  </tr>
  <tr class="associate-total-row hidden" data-parent-contract="c1" data-associate-id="a2">
    <td colspan="3">TOTAL DO ASSOCIADO:</td>
    <td class="total-original">0,00</td>
    <td class="total-acordado">0,00</td>
    <td class="total-calculado">0,00</td>
    <td></td>
  </tr>

  <!-- CONTRATO B -->
  <tr class="contract-total-row">
    <td></td>
    <td><span class="toggle-icon" data-target-level="contract" data-target-id="c2">+</span>TOTAL ENTRADAS - CONTRATO B</td>
    <td></td>
    <td class="text-right total-original">0,00</td>
    <td class="text-right total-acordado">0,00</td>
    <td class="text-right total-calculado">0,00</td>
    <td></td>
  </tr>

  <!-- Associado B1 -->
  <tr class="associate-header-row hidden" data-parent-contract="c2">
    <td><input class="check-all checkbox-ok" data-associate-id="b1" type="checkbox"></td>
    <td><span class="toggle-icon" data-target-level="associate" data-target-id="b1">+</span>Associado B1 - Loja Norte</td>
    <td colspan="5"></td>
  </tr>
  <tr class="invoice-row hidden" data-parent-associate="b1">
    <td><input class="check-invoice checkbox-ok" data-associate-id="b1" type="checkbox"></td>
    <td><span class="toggle-icon" data-target-level="invoice" data-target-id="nf301">+</span> NF 33001</td>
    <td>12/09/2025</td>
    <td class="valor-original text-right">4.200,00</td>
    <td class="valor-acordado"><input step="0.01" type="number"></td>
    <td class="valor-calculado text-right">0,00</td>
    <td><input style="width: 100%;" type="text"></td>
  </tr>
  <tr class="invoice-row hidden" data-parent-associate="b1">
    <td><input class="check-invoice checkbox-ok" data-associate-id="b1" type="checkbox"></td>
    <td><span class="toggle-icon" data-target-level="invoice" data-target-id="nf302">+</span> NF 33002</td>
    <td>15/09/2025</td>
    <td class="valor-original text-right">1.125,50</td>
    <td class="valor-acordado"><input step="0.01" type="number"></td>
    <td class="valor-calculado text-right">0,00</td>
    <td><input style="width: 100%;" type="text"></td>
  </tr>
  <tr class="associate-total-row hidden" data-parent-contract="c2" data-associate-id="b1">
    <td colspan="3">TOTAL DO ASSOCIADO:</td>
    <td class="total-original">0,00</td>
    <td class="total-acordado">0,00</td>
    <td class="total-calculado">0,00</td>
    <td></td>
  </tr>

  <!-- Associado B2 -->
  <tr class="associate-header-row hidden" data-parent-contract="c2">
    <td><input class="check-all checkbox-ok" data-associate-id="b2" type="checkbox"></td>
    <td><span class="toggle-icon" data-target-level="associate" data-target-id="b2">+</span>Associado B2 - Loja Centro</td>
    <td colspan="5"></td>
  </tr>
  <tr class="invoice-row hidden" data-parent-associate="b2">
    <td><input class="check-invoice checkbox-ok" data-associate-id="b2" type="checkbox"></td>
    <td><span class="toggle-icon" data-target-level="invoice" data-target-id="nf401">+</span> NF 44001</td>
    <td>20/08/2025</td>
    <td class="valor-original text-right">675,00</td>
    <td class="valor-acordado"><input step="0.01" type="number"></td>
    <td class="valor-calculado text-right">0,00</td>
    <td><input style="width: 100%;" type="text"></td>
  </tr>
  <tr class="associate-total-row hidden" data-parent-contract="c2" data-associate-id="b2">
    <td colspan="3">TOTAL DO ASSOCIADO:</td>
    <td class="total-original">0,00</td>
    <td class="total-acordado">0,00</td>
    <td class="total-calculado">0,00</td>
    <td></td>
  </tr>
</tbody>`;
    }

    getMockDevolucoesHTML() {
        return `<thead><tr><th style="width: 5%;">OK?</th> <th style="width: 30%;">Descrição</th> <th style="width: 10%;">Emissão</th><th class="text-right" style="width: 15%;">Valor Original</th><th class="text-right" style="width: 15%;">Valor Acordado</th><th class="text-right" style="width: 15%;">Valor Calculado</th><th style="width: 10%;">Obs.</th></tr></thead>
<tbody>
  <tr class="contract-total-row">
    <td></td>
    <td><span class="toggle-icon" data-target-level="contract" data-target-id="d1">+</span>TOTAL DEVOLUÇÕES - CONTRATO A</td>
    <td></td>
    <td class="text-right total-original">0,00</td>
    <td class="text-right total-acordado">0,00</td>
    <td class="text-right total-calculado">0,00</td>
    <td></td>
  </tr>

  <!-- Associado AD1 -->
  <tr class="associate-header-row hidden" data-parent-contract="d1">
    <td><input class="check-all checkbox-ok" data-associate-id="ad1" type="checkbox"></td>
    <td><span class="toggle-icon" data-target-level="associate" data-target-id="ad1">+</span>Associado AD1 - Loja Matriz</td>
    <td colspan="5"></td>
  </tr>
  <tr class="invoice-row hidden" data-parent-associate="ad1">
    <td><input class="check-invoice checkbox-ok" data-associate-id="ad1" type="checkbox"></td>
    <td><span class="toggle-icon" data-target-level="invoice" data-target-id="nf_dev_1">+</span> NF-Dev 501</td>
    <td>10/10/2025</td>
    <td class="valor-original text-right">95,50</td>
    <td class="valor-acordado"><input step="0.01" type="number"></td>
    <td class="valor-calculado text-right">0,00</td>
    <td><input style="width: 100%;" type="text"></td>
  </tr>
  <tr class="invoice-row hidden" data-parent-associate="ad1">
    <td><input class="check-invoice checkbox-ok" data-associate-id="ad1" type="checkbox"></td>
    <td><span class="toggle-icon" data-target-level="invoice" data-target-id="nf_dev_2">+</span> NF-Dev 502</td>
    <td>11/10/2025</td>
    <td class="valor-original text-right">150,00</td>
    <td class="valor-acordado"><input step="0.01" type="number"></td>
    <td class="valor-calculado text-right">0,00</td>
    <td><input style="width: 100%;" type="text"></td>
  </tr>
  <tr class="associate-total-row hidden" data-parent-contract="d1" data-associate-id="ad1">
    <td colspan="3">TOTAL DO ASSOCIADO:</td>
    <td class="total-original">0,00</td>
    <td class="total-acordado">0,00</td>
    <td class="total-calculado">0,00</td>
    <td></td>
  </tr>

  <!-- Associado AD2 -->
  <tr class="associate-header-row hidden" data-parent-contract="d1">
    <td><input class="check-all checkbox-ok" data-associate-id="ad2" type="checkbox"></td>
    <td><span class="toggle-icon" data-target-level="associate" data-target-id="ad2">+</span>Associado AD2 - Filial Sul</td>
    <td colspan="5"></td>
  </tr>
  <tr class="invoice-row hidden" data-parent-associate="ad2">
    <td><input class="check-invoice checkbox-ok" data-associate-id="ad2" type="checkbox"></td>
    <td><span class="toggle-icon" data-target-level="invoice" data-target-id="nf_dev_3">+</span> NF-Dev 601</td>
    <td>02/10/2025</td>
    <td class="valor-original text-right">320,25</td>
    <td class="valor-acordado"><input step="0.01" type="number"></td>
    <td class="valor-calculado text-right">0,00</td>
    <td><input style="width: 100%;" type="text"></td>
  </tr>
  <tr class="associate-total-row hidden" data-parent-contract="d1" data-associate-id="ad2">
    <td colspan="3">TOTAL DO ASSOCIADO:</td>
    <td class="total-original">0,00</td>
    <td class="total-acordado">0,00</td>
    <td class="total-calculado">0,00</td>
    <td></td>
  </tr>

  <!-- CONTRATO D2 -->
  <tr class="contract-total-row">
    <td></td>
    <td><span class="toggle-icon" data-target-level="contract" data-target-id="d2">+</span>TOTAL DEVOLUÇÕES - CONTRATO B</td>
    <td></td>
    <td class="text-right total-original">0,00</td>
    <td class="text-right total-acordado">0,00</td>
    <td class="text-right total-calculado">0,00</td>
    <td></td>
  </tr>

  <!-- Associado BD1 -->
  <tr class="associate-header-row hidden" data-parent-contract="d2">
    <td><input class="check-all checkbox-ok" data-associate-id="bd1" type="checkbox"></td>
    <td><span class="toggle-icon" data-target-level="associate" data-target-id="bd1">+</span>Associado BD1 - Loja Norte</td>
    <td colspan="5"></td>
  </tr>
  <tr class="invoice-row hidden" data-parent-associate="bd1">
    <td><input class="check-invoice checkbox-ok" data-associate-id="bd1" type="checkbox"></td>
    <td><span class="toggle-icon" data-target-level="invoice" data-target-id="nf_dev_21">+</span> NF-Dev 701</td>
    <td>22/09/2025</td>
    <td class="valor-original text-right">1.200,00</td>
    <td class="valor-acordado"><input step="0.01" type="number"></td>
    <td class="valor-calculado text-right">0,00</td>
    <td><input style="width: 100%;" type="text"></td>
  </tr>
  <tr class="associate-total-row hidden" data-parent-contract="d2" data-associate-id="bd1">
    <td colspan="3">TOTAL DO ASSOCIADO:</td>
    <td class="total-original">0,00</td>
    <td class="total-acordado">0,00</td>
    <td class="total-calculado">0,00</td>
    <td></td>
  </tr>
</tbody>`;
    }
}

// Função global para voltar ao início
function voltarParaInicio() {
    if (window.apuracaoApp) {
        window.apuracaoApp.voltarParaInicio();
    }
}

// Inicializar quando o DOM estiver pronto
document.addEventListener('DOMContentLoaded', () => {
    window.apuracaoApp = new ApuracaoContrato();
});