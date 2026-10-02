# Inventory Management API

[![Tests](https://github.com/brenopyx/inventory-management-api/actions/workflows/tests.yml/badge.svg)](https://github.com/brenopyx/inventory-management-api/actions/workflows/tests.yml)

<img src="https://flagcdn.com/24x18/br.png" height="12" valign="middle"> [Leia em Português](README.pt-BR.md)

A full-stack inventory management system built as a backend-focused portfolio project, simulating real stock control for a bakery. The project covers the complete lifecycle of a production-grade API: relational data modeling, business rule validation, authentication, automated testing, containerization, and CI/CD.

## Overview

This system lets a small business manage product categories, products, and stock movements (entries/exits), with real-time stock calculation derived from a full movement history not a mutable counter. The core business rule prevents any stock exit larger than what's currently available, enforced at the service layer and covered by automated tests.

A lightweight frontend (HTML/CSS/TypeScript) consumes the API directly, demonstrating end-to-end integration: authentication, CRUD operations, and real stock queries.

## Tech Stack

**Backend**
- Python 3.12, FastAPI
- SQLAlchemy 2.0 (ORM) + Alembic (migrations)
- PostgreSQL
- Pydantic (validation)
- JWT authentication (python-jose, passlib/bcrypt)

**Testing & CI**
- Pytest, with an isolated PostgreSQL test database
- GitHub Actions (automated test suite on every push)

**Infrastructure**
- Docker + Docker Compose (API, database, and automated test-db provisioning)

**Frontend**
- HTML, CSS, TypeScript (vanilla, compiled with `tsc`)

## Key Design Decisions

- **Stock is never stored, always calculated.** Current stock is derived by summing entries and subtracting exits from the full movement history not a mutable column. This guarantees the stock figure can never drift from the audit trail.
- **Router / Service separation.** Routers handle HTTP concerns only; business logic (stock validation, calculations) lives in a dedicated service layer.
- **Movements are append-only.** No `PUT`/`DELETE` on movements correcting a mistake means logging a new adjustment movement, preserving full auditability.
- **Referential integrity is enforced in both directions.** Deleting a category with linked products, or a product with linked movements, is explicitly blocked with a clear `400` response not a raw database error.
- **Write endpoints require authentication; read endpoints are public**  a deliberate trade-off for this project's scope.

## Getting Started

### Requirements
- Docker and Docker Compose

### Run the project

```bash
git clone https://github.com/brenopyx/Stock_System_API.git
cd Stock_System_API
cp .env.example .env
```

Open `.env` and fill in your own values (database credentials and a generated `SECRET_KEY`). To generate a secure secret key:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Then start the containers:
```bash
docker compose up --build
```

This starts the API, PostgreSQL, and automatically creates both the main and test databases using the credentials from your `.env` file.

Apply database migrations:
```bash
docker compose exec api alembic upgrade head
```

API available at: `http://localhost:8000`
Interactive docs (Swagger UI): `http://localhost:8000/docs`

### Running the frontend

Serve the `frontend/` folder with any static server (e.g., VS Code Live Server) and open `pages/login.html`. Make sure the API is running at `localhost:8000`.

## Running Tests

```bash
pytest -v
```

Tests run against an isolated PostgreSQL database, with fixtures handling authentication, schema setup, and teardown automatically for each test.

## Main Endpoints

| Method | Endpoint | Description | Auth |
|---|---|---|---|
| POST | `/usuarios/` | Register user | No |
| POST | `/usuarios/login` | Login (returns JWT) | No |
| GET | `/categorias/`, `/produtos/`, `/movimentacoes/` | List resources | No |
| GET | `/produtos/{id}/estoque` | Current stock for a product | No |
| POST / PUT / DELETE | `/categorias/`, `/produtos/` | Manage resources | Yes |
| POST | `/movimentacoes/` | Register stock movement (entry/exit) | Yes |

Full documentation with request/response schemas is available via Swagger at `/docs`.

## Possible Future Improvements

- Role-based authorization (admin vs. regular user)
- Stock-level caching with transactional consistency, for larger movement volumes
- Pagination on list endpoints
- Soft-delete for categories/products

## About This Project

Built as a learning-driven portfolio project to practice backend engineering fundamentals, from database design to deployment. Every architectural decision above was made deliberately and is documented here to reflect real engineering trade-offs, not default scaffolding.