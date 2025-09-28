# sTOCK - Projeto Engenharia de Software

## Resumo

O projeto consiste em desenvolver um aplicativo mobile para controle de estoque voltado a mercados de pequeno e médio porte. A solução busca ser acessível, moderna e dinâmica, permitindo que os usuários cadastrem produtos de forma simples por meio da leitura de código de barras pelo celular, com armazenamento automático em banco de dados.

O sistema emitirá alertas inteligentes em situações críticas, como falta de itens, proximidade da validade ou produtos de alta demanda. Nesses casos, um agente de inteligência artificial (LLM) entrará em contato com redes de distribuição previamente cadastradas, fará a comparação de preços e deixará um pedido pré-preparado, cabendo ao usuário apenas revisar e confirmar.

A proposta traz praticidade, economia e eficiência para pequenos e médios mercados, que muitas vezes não têm acesso a sistemas de gestão sofisticados.


## Guia de Execução

### ╰┈➤ 1) Criar e ativar o ambiente virtual (venv)

#### Windows (PowerShell)
```powershell
py -3.11 -m venv .venv          # ou: python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

#### Linux/macOS
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### ╰┈➤ 2) Instalar dependências

O projeto já tem `requirements.txt`:
```bash
pip install -r requirements.txt
```

### ╰┈➤ 3) Configurar o app (DB)

Fazer num file .env (trocando user e password pelo seu):    
```bash
DATABASE_URL = "postgresql+psycopg2://user:password@localhost:5432/controle_estoque"
```
- Checar .env.example
- Rodar python alimentando_database_temp.py

### ╰┈➤ 4) Subir o servidor (API + Frontend)

Na raiz do projeto (venv ativo):
```bash
uvicorn api.main:app --reload --port 8000
```
- A API ficará em **http://localhost:8000**
- A documentação Swagger em **http://localhost:8000/docs**
- O frontend (HTML/JS) é servido pela própria API a partir da pasta `frontend/` (ex.: **http://localhost:8000/**).


### ╰┈➤ 5) Criar usuário inicial (seed) — PowerShell

Para criar um usuário padrão de teste, execute:

```powershell
Invoke-RestMethod -Method POST http://localhost:8000/api/users/seed
```

Esse *seed* garante a existência de um usuário inicial, tipo o 'dono do mercadinho 1':

* **Usuário:** `op_front`
* **Senha:** `123`

Esse usuário serve como operador padrão, mas ao logar com `op_front`, o relatório pode aparecer **vazio**.
Isso acontece porque o script `alimentando_database_temp.py` popula a base com dados vinculados a outro usuário (o administrador, por exemplo o dono do mercadinho 2).

#### Usuário criado pelo script de população temporária

O script `alimentando_database_temp.py` limpa o banco e cria um **usuário administrador**, junto com dezenas de produtos e movimentações:

* **Usuário:** `admin`
* **Senha:** `admin123`

Quando você loga como `admin`, todo o estoque populado pelo script fica visível nos relatórios.
Essa divergência foi mantida **de propósito** para simular diferentes perfis de cliente (operador sem estoque inicial vs. administrador com estoque cheio).


### ╰┈➤ 6) Acessar o app

- Abra **http://localhost:8000** no navegador → **Login**
- Entre com **admin/admin123** ou **op_front / 123**
- Use o menu para **Cadastrar produto**, **Relatório** etc. (por agora, está apenas o front sem integração completa com a base - exceto por relatório!)
- A documentação da API está em **http://localhost:8000/docs** (você pode testar os endpoints por lá também).


### Estrutura do projeto

```
.
├── api/
│   ├── main.py
│   ├── deps.py
│   └── schemas.py
├── database/
│   ├── database.py
│   ├── models/
│   │   ├── users.py
│   │   ├── products.py
│   │   └── movements.py
│   └── services/
│       ├── users_service.py
│       ├── products_service.py
│       └── movements_service.py
├── frontend/
│   ├── index.html
│   ├── inicial.html
│   ├── assets/
│   └── ...
├── barcode_scanner/  
│   └── scanner.py
├── config.py
├── alimentando_database_temp.py
├── exemplo_uso_db.py
├── requirements.txt
└── README.md
```
