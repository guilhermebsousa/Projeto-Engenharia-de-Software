// frontend/utils.js

// ===== Constantes e Sessão (Reutilizáveis) =====
const API_BASE = window.location.origin;
const user = JSON.parse(sessionStorage.getItem('stokUser') || 'null');

// Função para verificar se o usuário está logado e redirecionar se não estiver
function verificarSessao() {
  if (!user) {
    console.warn('Nenhum usuário logado. Redirecionando para /index.html');
    window.location.href = '/index.html';
  }
  return user;
}

// Função para fazer logout
function fazerLogout() {
  sessionStorage.removeItem('stokUser');
  window.location.href = '/index.html';
}

// ===== Funções da API (Reutilizáveis) =====

/**
 * Busca produtos da API para um determinado usuário.
 * @param {string} userId - O ID do usuário.
 * @param {string} [term=''] - Um termo de busca opcional.
 * @returns {Promise<Array>} - Uma promessa que resolve para a lista de produtos.
 */
async function fetchProdutos(userId, term = '') {
  const url = term
    ? `${API_BASE}/api/users/${userId}/products?search=${encodeURIComponent(term)}`
    : `${API_BASE}/api/users/${userId}/products`;
  const response = await fetch(url);
  if (!response.ok) {
    throw new Error('Falha ao carregar produtos da API.');
  }
  return response.json();
}

// ===== Funções de Renderização (Reutilizáveis) =====

/**
 * Renderiza a tabela de produtos na página de edição.
 * @param {Array} lista - A lista de produtos a ser renderizada.
 * @param {HTMLElement} tbodyElement - O elemento <tbody> da tabela.
 */
function desenharTabelaEdicao(lista, tbodyElement) {
  tbodyElement.innerHTML = '';
  if (!lista || !lista.length) {
    tbodyElement.innerHTML = `<tr><td colspan="6" style="padding:14px;">Nenhum produto encontrado.</td></tr>`;
    return;
  }
  for (const p of lista) {
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td>${p.name}</td>
      <td>${p.brand ?? '—'}</td>
      <td>${p.barcode}</td>
      <td class="qty">${p.current_quantity ?? 0} ${p.unit || 'un'}</td>
      <td>${p.suggested_price != null ? 'R$ ' + Number(p.suggested_price).toFixed(2) : '—'}</td>
      <td>
        <button class="edit-btn" data-id="${p.id}">Editar</button>
      </td>
    `;
    tbodyElement.appendChild(tr);
  }
}