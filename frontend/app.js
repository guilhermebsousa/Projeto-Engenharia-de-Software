// Controle do menu (abrir/fechar com acessibilidade)
(function () {
  const btn = document.getElementById('menuBtn');
  const menu = document.getElementById('menuList');

  function setOpen(open) {
    menu.dataset.open = open ? "true" : "false";
    btn.setAttribute('aria-expanded', open ? "true" : "false");
  }

  btn.addEventListener('click', (e) => {
    e.stopPropagation();
    setOpen(menu.dataset.open !== "true");
  });

  document.addEventListener('click', (e) => {
    if (!menu.contains(e.target) && e.target !== btn) setOpen(false);
  });

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') setOpen(false);
  });
})();

document.getElementById('loginForm').addEventListener('submit', async function (e) {
  e.preventDefault();
  const username = this.login.value.trim();
  const password = this.senha.value.trim();

  if (!username || !password) {
    alert('Preencha login e senha.');
    return;
  }

  try {
    const API_BASE = window.location.origin; // tudo em :8000
    const r = await fetch(`${API_BASE}/api/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password })
    });

    if (!r.ok) {
      const t = await r.text().catch(() => '');
      alert(`Login inválido.\n${t || ''}`);
      return;
    }

    const user = await r.json();               // {id, username, role, ...}
    sessionStorage.setItem('stokUser', JSON.stringify(user));
    window.location.href = "/inicial.html";
  } catch (err) {
    console.error(err);
    alert('Não foi possível conectar à API. Verifique se o backend está rodando.');
  }
});


// Ações de links auxiliares (placeholders)
document.getElementById('forgot').addEventListener('click', (e) => {
  e.preventDefault();
  alert('Fluxo de recuperação de senha em breve.');
});

// Fluxo de criação de conta
document.getElementById('signup').addEventListener('click', function (e) {
  e.preventDefault();
  const username = prompt('Digite o nome de usuário:');
  const password = prompt('Digite a senha:');
  if (!username || !password) return;

  fetch('api/signup', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password })
  })
    .then(res => res.json())
    .then(data => {
      if (data.detail) {
        alert('Erro: ' + data.detail);
      } else {
        alert('Conta criada com sucesso!');
      }
    });
});

// Botão voltar
document.getElementById('btnBack').onclick = () => window.location.href = '/editar.html';

// Carregar dados do produto
const params = new URLSearchParams(window.location.search);
const productId = params.get('id');
const user = JSON.parse(sessionStorage.getItem('stokUser') || 'null');
if (!user) window.location.href = '/index.html';

async function carregarProduto() {
  const r = await fetch(`${window.location.origin}/api/users/${user.id}/products/${productId}`);
  if (!r.ok) return alert('Produto não encontrado!');
  const p = await r.json();
  for (const k in p) {
    const el = document.getElementById(k);
    if (el) el.value = p[k] ?? '';
  }
}
carregarProduto();

// Salvar alterações
document.getElementById('formEditarProduto').addEventListener('submit', async function (e) {
  e.preventDefault();
  const dados = Object.fromEntries(new FormData(this));

  dados.package_quantity = dados.package_quantity ? parseFloat(dados.package_quantity) : null;
  dados.minimum_stock = dados.minimum_stock ? parseFloat(dados.minimum_stock) : 0;
  dados.suggested_price = dados.suggested_price ? parseFloat(dados.suggested_price) : null;
  dados.current_quantity = dados.current_quantity ? parseFloat(dados.current_quantity) : 0;

  if (!dados.expiration_date) {
    dados.expiration_date = null;
  }

  // A constante `API_BASE` agora vem de utils.js
  const r = await fetch(`${API_BASE}/api/users/${user.id}/products/${productId}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(dados)
  });

  if (r.ok) {
    alert('Produto atualizado!');
    window.location.href = '/editar.html';
  } else {
    const error = await r.json().catch(() => ({ detail: 'Erro ao conectar com a API.' }));
    alert(`Erro ao atualizar produto: ${error.detail}`);
  }
});