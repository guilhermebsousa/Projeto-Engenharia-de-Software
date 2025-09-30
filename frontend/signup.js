document.getElementById('signupForm').addEventListener('submit', function (e) {
  e.preventDefault();

  const username = document.getElementById('username').value.trim();
  const password = document.getElementById('password').value.trim();
  const email = document.getElementById('email').value.trim();
  const full_name = document.getElementById('full_name').value.trim();

  if (!username || !password || !email) {
    alert("Preencha todos os campos obrigatórios (*)");
    return;
  }

  fetch('/api/signup', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password, email, full_name })
  })
    .then(res => res.json())
    .then(data => {
      if (data.detail) {
        alert('Erro: ' + data.detail);
      } else {
        alert('Conta criada com sucesso!');
        window.location.href = "/"; // volta para login
      }
    })
    .catch(err => {
      console.error(err);
      alert("Erro ao comunicar com servidor");
    });
});
