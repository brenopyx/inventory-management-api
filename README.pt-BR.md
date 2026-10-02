# API de Gestão de Estoque

[![Tests](https://github.com/brenopyx/inventory-management-api/actions/workflows/tests.yml/badge.svg)](https://github.com/brenopyx/inventory-management-api/actions/workflows/tests.yml)

<img src="https://flagcdn.com/24x18/gb.png" height="12" valign="middle"> [Read in English](README.md)

Sistema completo de gestão de estoque, construído como projeto de portfólio com foco em backend, simulando o controle de estoque real de uma padaria ("Padaria Central"). O projeto cobre o ciclo completo de uma API de nível profissional: modelagem de dados relacional, validação de regras de negócio, autenticação, testes automatizados, containerização e CI/CD.

## Visão Geral

O sistema permite que um pequeno negócio gerencie categorias de produtos, produtos e movimentações de estoque (entradas/saídas), com cálculo de estoque em tempo real derivado do histórico completo de movimentações não um contador editável. A regra de negócio central impede qualquer saída de estoque maior do que o disponível, validada na camada de serviço e coberta por testes automatizados.

Um frontend leve (HTML/CSS/TypeScript) consome a API diretamente, demonstrando a integração ponta a ponta: autenticação, operações CRUD e consultas reais de estoque.

## Stack Tecnológica

**Backend**
- Python 3.12, FastAPI
- SQLAlchemy 2.0 (ORM) + Alembic (migrations)
- PostgreSQL
- Pydantic (validação)
- Autenticação JWT (python-jose, passlib/bcrypt)

**Testes e CI**
- Pytest, com banco de dados de teste isolado no PostgreSQL
- GitHub Actions (suíte de testes automatizada a cada push)

**Infraestrutura**
- Docker + Docker Compose (API, banco de dados, e criação automática do banco de testes)

**Frontend**
- HTML, CSS, TypeScript (puro, compilado com `tsc`)

## Decisões de Arquitetura

- **O estoque nunca é armazenado, sempre é calculado.** O estoque atual é derivado somando entradas e subtraindo saídas de todo o histórico de movimentações não é uma coluna editável. Isso garante que o número de estoque nunca pode divergir do histórico de auditoria.
- **Separação entre Router e Service.** Os routers lidam só com a parte HTTP; a lógica de negócio (validação de estoque, cálculos) fica isolada numa camada de serviço dedicada.
- **Movimentações são apenas de inserção (append-only).** Não existe `PUT`/`DELETE` em movimentações corrigir um erro significa registrar uma nova movimentação de ajuste, preservando a auditoria completa.
- **Integridade referencial é garantida nas duas direções.** Excluir uma categoria com produtos vinculados, ou um produto com movimentações vinculadas, é explicitamente bloqueado com uma resposta `400` clara não um erro cru de banco de dados.
- **Endpoints de escrita exigem autenticação; endpoints de leitura são públicos** uma decisão deliberada para o escopo deste projeto.

## Como Executar

### Requisitos
- Docker e Docker Compose

### Rodando o projeto

```bash
git clone https://github.com/brenopyx/Stock_System_API.git
cd Stock_System_API
cp .env.example .env
```

Abra o `.env` e preencha com seus próprios valores (credenciais do banco de dados e uma `SECRET_KEY` gerada). Para gerar uma chave secreta segura:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Depois, sobe os containers:
```bash
docker compose up --build
```

Isso sobe a API, o PostgreSQL, e cria automaticamente tanto o banco principal quanto o banco de testes, usando as credenciais do seu arquivo `.env`.

Aplicar as migrations do banco:
```bash
docker compose exec api alembic upgrade head
```

API disponível em: `http://localhost:8000`
Documentação interativa (Swagger UI): `http://localhost:8000/docs`

### Rodando o frontend

Sirva a pasta `frontend/` com qualquer servidor estático (ex: Live Server do VS Code) e abra `pages/login.html`. Confirme que a API está rodando em `localhost:8000`.

## Rodando os Testes

```bash
pytest -v
```

Os testes rodam contra um banco de dados PostgreSQL isolado, com fixtures cuidando automaticamente de autenticação, criação de schema e limpeza a cada teste.

## Principais Endpoints

| Método | Endpoint | Descrição | Autenticação |
|---|---|---|---|
| POST | `/usuarios/` | Cadastrar usuário | Não |
| POST | `/usuarios/login` | Login (retorna JWT) | Não |
| GET | `/categorias/`, `/produtos/`, `/movimentacoes/` | Listar recursos | Não |
| GET | `/produtos/{id}/estoque` | Estoque atual de um produto | Não |
| POST / PUT / DELETE | `/categorias/`, `/produtos/` | Gerenciar recursos | Sim |
| POST | `/movimentacoes/` | Registrar movimentação (entrada/saída) | Sim |

Documentação completa com os schemas de requisição/resposta disponível via Swagger em `/docs`.

## Possíveis Melhorias Futuras

- Autorização baseada em papéis (administrador vs. usuário comum)
- Cache de nível de estoque com consistência transacional, para grandes volumes de movimentação
- Paginação nos endpoints de listagem
- Exclusão lógica (soft-delete) para categorias/produtos

## Sobre o Projeto

Construído como projeto de portfólio orientado a aprendizado, para praticar fundamentos de engenharia de backend, desde a modelagem de banco até o deploy. Cada decisão de arquitetura acima foi tomada de forma deliberada e está documentada aqui para refletir trade-offs reais de engenharia, não uma estrutura padrão genérica.