document.addEventListener('DOMContentLoaded', () => {
    // --- CONFIGURAÇÃO INICIAL ---
    initializeDrilldown();
    initializeTabs();
    initializeModal();
    initializeCheckboxLogic();
    updateAllTotals(); // Garante que os totais sejam calculados na carga inicial

    // --- FUNÇÕES DE INICIALIZAÇÃO ---
    function initializeTabs() {
        const tabs = document.querySelectorAll('.tab-button');
        const tabContents = document.querySelectorAll('.tab-content');

        tabs.forEach(tab => {
            tab.addEventListener('click', () => {
                const target = document.getElementById(tab.dataset.tab);

                tabs.forEach(t => t.classList.remove('active'));
                tab.classList.add('active');

                tabContents.forEach(tc => tc.classList.remove('active'));
                if (target) {
                    target.classList.add('active');
                }
            });
        });
    }

    function initializeModal() {
        const modal = document.getElementById('save-modal');
        const openModalBtn = document.getElementById('open-save-modal-btn');
        const closeModalElements = document.querySelectorAll('#close-modal-btn, #cancel-save-btn');

        if (openModalBtn) {
            openModalBtn.addEventListener('click', (e) => {
                e.preventDefault(); // Prevenir envio do formulário
                if (!openModalBtn.disabled) {
                    updateModalSummary();
                    modal.style.display = 'flex';
                }
            });
        }

        closeModalElements.forEach(el => {
            el.addEventListener('click', () => {
                modal.style.display = 'none';
            });
        });

        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                modal.style.display = 'none';
            }
        });

        const confirmSaveBtn = document.getElementById('confirm-save-btn');
        if (confirmSaveBtn) {
            confirmSaveBtn.addEventListener('click', () => {
                alert('Apuração gravada com sucesso!');
                modal.style.display = 'none';
            });
        }

        window.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && modal.style.display === 'flex') {
                modal.style.display = 'none';
            }
        });
    }

    function initializeDrilldown() {
        const drilldownTables = document.querySelectorAll('.drilldown-table');
        drilldownTables.forEach(table => {
            const rows = table.querySelectorAll('.drilldown-row');
            rows.forEach(row => {
                if (!row.classList.contains('level-0')) {
                    row.style.display = 'none';
                }
            });

            table.addEventListener('click', (e) => {
                const target = e.target;
                if (target.type === 'checkbox') {
                    return;
                }

                const row = target.closest('.drilldown-row');
                if (row && (row.classList.contains('level-0') || row.classList.contains('level-1'))) {
                    const rowId = row.dataset.id;
                    row.classList.toggle('expanded');
                    const icon = row.querySelector('.fa-chevron-right, .fa-chevron-down');
                    if (icon) {
                        icon.classList.toggle('fa-chevron-right');
                        icon.classList.toggle('fa-chevron-down');
                    }

                    const children = table.querySelectorAll(`.drilldown-row[data-parent="${rowId}"]`);
                    children.forEach(child => {
                        const isExpanded = row.classList.contains('expanded');
                        child.style.display = isExpanded ? 'table-row' : 'none';

                        if (!isExpanded) {
                            child.classList.remove('expanded');
                            const childId = child.dataset.id;
                            const grandChildren = table.querySelectorAll(`.drilldown-row[data-parent="${childId}"]`);
                            grandChildren.forEach(gc => {
                                gc.style.display = 'none';
                            });
                        }
                    });
                }
            });
        });
    }

    function initializeCheckboxLogic() {
        document.querySelectorAll('.master-checkbox, .associate-checkbox, .note-checkbox').forEach(checkbox => {
            checkbox.addEventListener('change', (e) => {
                const target = e.target;

                if (target.classList.contains('master-checkbox')) {
                    const tableId = target.dataset.tableId;
                    const table = document.getElementById(tableId);
                    if (table) {
                        table.querySelectorAll('.associate-checkbox, .note-checkbox').forEach(cb => {
                            cb.checked = target.checked;
                        });
                    }
                } else if (target.classList.contains('associate-checkbox')) {
                    const associateId = target.dataset.associateId;
                    document.querySelectorAll(`.note-checkbox[data-associate-id="${associateId}"]`).forEach(noteCheckbox => {
                        noteCheckbox.checked = target.checked;
                    });
                } else if (target.classList.contains('note-checkbox')) {
                    const associateId = target.dataset.associateId;
                    const allNotes = document.querySelectorAll(`.note-checkbox[data-associate-id="${associateId}"]`);
                    const associateCheckbox = document.querySelector(`.associate-checkbox[data-associate-id="${associateId}"]`);
                    if (associateCheckbox) {
                        associateCheckbox.checked = Array.from(allNotes).every(cb => cb.checked);
                    }
                }

                updateAllTotals();
            });
        });
    }

    // --- LÓGICA DE CÁLCULO E ATUALIZAÇÃO ---
    function formatCurrency(value) {
        return value.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });
    }

    function updateAllTotals() {
        const totalEntradas = calculateTotalForTable('table-entradas');
        const totalDevolucoes = calculateTotalForTable('table-devolucoes');
        const finalTotal = totalEntradas - totalDevolucoes;

        document.getElementById('summary-entradas').textContent = formatCurrency(totalEntradas);
        document.getElementById('summary-devolucoes').textContent = formatCurrency(totalDevolucoes);
        document.getElementById('summary-final').textContent = formatCurrency(finalTotal);

        updateSubtotals('table-entradas');
        updateSubtotals('table-devolucoes');
    }

    function calculateTotalForTable(tableId) {
        let total = 0;
        document.querySelectorAll(`#${tableId} .note-checkbox:checked`).forEach(checkbox => {
            total += parseFloat(checkbox.dataset.value) || 0;
        });
        return total;
    }

    function updateSubtotals(tableId) {
        const table = document.getElementById(tableId);
        if (!table) return;

        table.querySelectorAll('.level-0').forEach(row => {
            const associateId = row.querySelector('.associate-checkbox')?.dataset.associateId;
            if (!associateId) return;

            let subtotal = 0;
            table.querySelectorAll(`.note-checkbox[data-associate-id="${associateId}"]:checked`).forEach(noteCheckbox => {
                subtotal += parseFloat(noteCheckbox.dataset.value) || 0;
            });

            const subtotalCell = row.querySelector('.subtotal-entradas, .subtotal-devolucoes');
            if (subtotalCell) {
                subtotalCell.innerHTML = `<strong>${formatCurrency(subtotal)}</strong>`;
            }
        });
    }

    function updateModalSummary() {
        const totalEntradasText = document.getElementById('summary-entradas').textContent;
        const totalDevolucoesText = document.getElementById('summary-devolucoes').textContent;

        const totalEntradas = parseFloat(totalEntradasText.replace(/[^0-9,-]+/g, '').replace('.', '').replace(',', '.')) || 0;
        const totalDevolucoes = parseFloat(totalDevolucoesText.replace(/[^0-9,-]+/g, '').replace('.', '').replace(',', '.')) || 0;
        const finalTotal = totalEntradas - totalDevolucoes;

        document.getElementById('modal-summary-entradas').textContent = formatCurrency(totalEntradas);
        document.getElementById('modal-summary-devolucoes').textContent = formatCurrency(totalDevolucoes);
        document.getElementById('modal-summary-final').textContent = formatCurrency(finalTotal);
    }
});

function voltarParaInicio() {
    window.location.href = "/apuracao/";
}