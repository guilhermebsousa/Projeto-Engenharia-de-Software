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
      headers: { 'Content-Type':'application/json' },
      body: JSON.stringify({ username, password })
    });

    if (!r.ok) {
      const t = await r.text().catch(()=> '');
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
document.getElementById('signup').addEventListener('click', function(e) {
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