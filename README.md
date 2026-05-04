
📚 Documentação Técnica: Sistema de Atendimento SENAI Gama

Este projeto foi desenvolvido para gerenciar o fluxo de atendimento da Unidade Gama do SENAI, utilizando uma arquitetura moderna, segura e escalável.
🏗️ Arquitetura do Sistema

O sistema utiliza uma arquitetura Client-Server (Cliente-Servidor) baseada em um Monolito Modular. Isso significa que, embora o código esteja centralizado, as responsabilidades de interface, lógica e dados estão bem separadas.
Visualização da Arquitetura de Componentes
Plaintext

+----------------+       HTTP/JSON       +-------------------+
|   FRONTEND     | <-------------------> |      BACKEND      |
| (Totem/Painel) |                       |     (FastAPI)     |
+----------------+                       +---------+---------+
                                                   |
                                                   | SQLAlchemy ORM
                                                   v
                                         +-------------------+
                                         |  BANCO DE DADOS   |
                                         |      (MySQL)      |
                                         +-------------------+

Estrutura de Pastas (Design de Projeto)

A organização segue o padrão de módulos do Python, facilitando a manutenção e o reaproveitamento de código.
Plaintext

/
├── main.py                # Orquestrador: Inicia o servidor e define as rotas da API
├── .env                   # Segurança: Armazena credenciais sensíveis (ignorado pelo Git)
├── .gitignore             # Controle: Define arquivos que não devem subir para o GitHub
├── atendente/             # Módulo Centralizado (Lógica de Negócio)
│   ├── database.py        # Configuração da conexão e SessionLocal
│   ├── models.py          # Arquitetura de dados (Tabelas do Banco)
│   ├── schemas.py         # Validação de dados (Contratos da API)
│   ├── crud.py            # Operações de Criar, Ler, Atualizar e Deletar
│   ├── static/            # Ativos estáticos (CSS Flexbox, JS, Áudio)
│   └── templates/         # Interfaces HTML (Jinja2)

🗄️ Arquitetura de Dados

O banco de dados utiliza um modelo Relacional, garantindo que cada atendimento seja único e rastreável para futuras métricas de produtividade.
Diagrama da Tabela atendimentos
Atributo	Função Técnica
Status	Máquina de estados que controla se a senha está 'aguardando' ou 'chamada'.
Data/Hora	Essencial para o cálculo do Tempo Médio de Atendimento (TMA).
Código	Identificador visual para o aluno (Ex: N-001).
🛠️ Próximas Implementações (Roadmap)

    UX/UI - Ciclo de Vida do Totem: Implementação de botão "Voltar" para correção de escolha e sistema de auto-reset (voltar à tela inicial automaticamente após 7 segundos de emissão da senha).

    WebSockets: Evolução da API para atualização em tempo real do painel sem necessidade de recarregar a página.

    Métricas em Dashboard: Gráficos para a coordenação do SENAI com horários de pico e volume de atendimentos.

📖 Referências e Guia de Estudos

Para desenvolver este projeto, foram aplicados conceitos fundamentais de engenharia que recomendamos para estudo:
1. Tecnologias Base

    FastAPI Documentation: Framework moderno e de alta performance. Essencial entender o conceito de Path Operations e Dependency Injection.

    SQLAlchemy ORM: Estude como transformar tabelas de banco de dados em classes Python.

2. Padrões de Código e Qualidade

    PEP 8 – Style Guide for Python: O guia oficial de estilo para código Python. Ensina a importância da indentação, espaços e nomenclatura de variáveis.

    Clean Code (Código Limpo): Técnicas aplicadas neste projeto para tornar o código legível e fácil de manter.

        Nomes Significativos: Variáveis que explicam o que fazem (ex: get_db em vez de func1).

        Funções Pequenas: Cada função deve fazer apenas uma coisa e fazê-la bem.

    Variáveis de Ambiente (.env): O uso do python-dotenv é uma prática recomendada para evitar o vazamento de segredos em sistemas de produção.
