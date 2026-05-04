# Sistema de Atendimento - SENAI Unidade Gama

Sistema full-stack para gestão de filas e chamadas de senhas, desenvolvido para otimizar o fluxo de alunos na unidade de atendimento.

## 🚀 Tecnologias Utilizadas
* **Backend:** Python com FastAPI
* **Banco de Dados:** MySQL com SQLAlchemy (ORM)
* **Frontend:** HTML5, CSS3 (Flexbox/Grid), JavaScript (ES6+)
* **Estilização:** Tailwind CSS & Lucide Icons
* **Servidor:** Uvicorn

## 📂 Estrutura de Pastas
Abaixo, a organização modular do projeto garantindo a separação de responsabilidades:
```text
/
├── main.py                # Ponto de entrada da aplicação e rotas FastAPI
├── atendente/             # Módulo principal do sistema
│   ├── database.py        # Configuração da conexão MySQL
│   ├── models.py          # Definição das tabelas (SQLAlchemy)
│   ├── schemas.py         # Modelos de validação (Pydantic)
│   ├── crud.py            # Operações de Banco de Dados
│   ├── static/            # Arquivos Estáticos (CSS, JS, Audio)
│   │   ├── css/           # painel.css, totem.css, atendente.css
│   │   ├── js/            # painel.js, totem.js, atendente.js
│   │   └── audio/         # chamada.wav
│   └── templates/         # Arquivos HTML (Jinja2)
│       ├── totem.html
│       ├── painel.html
│       └── atendente.html
└── .gitignore             # Arquivos ignorados pelo Git