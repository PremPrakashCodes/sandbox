# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Architecture Overview

This is a monorepo containing:

- **Frontend** (apps/frontend): Next.js 15 application with TypeScript and Tailwind CSS v4
- **Backend** (apps/backend): FastAPI application with SQLAlchemy ORM, Alembic migrations, and Redis caching
- **Python SDK** (packages/sdk/python): Python client for the API using httpx
- **TypeScript SDK** (packages/sdk/typescript): TypeScript client for the API using axios

## Tech Stack

- **Node.js 18+** with npm for frontend and build tooling
- **Python 3.12** with uv for backend services
- **PostgreSQL** for primary database
- **Redis** for caching and session management
- **SQLAlchemy 2.0+** for ORM with async support
- **Alembic** for database migrations

## Common Development Commands

### Full Stack Development

```bash
# Run frontend, backend, and Redis concurrently
npm run dev

# Run services individually
npm run dev:frontend  # Next.js on http://localhost:3000
npm run backend       # FastAPI on http://localhost:8000
npm run redis         # Redis via Docker Compose
npm run database      # PostgreSQL via Docker Compose
```

### Frontend Commands

```bash
npm run build:frontend  # Production build
npm run lint:frontend   # Lint Next.js code
```

### Backend Commands

```bash
# Run backend server
cd apps/backend && uv run sandbox

# Database migrations
cd apps/backend
alembic revision --autogenerate -m "Description"  # Create migration
alembic upgrade head                               # Apply migrations
alembic downgrade -1                               # Rollback one migration
```

### SDK Development

```bash
# TypeScript SDK
npm run build:sdk       # Build SDK
npm run dev:sdk         # Watch mode
cd packages/sdk/typescript && npm run type-check

# Python SDK
cd packages/sdk/python && uv sync
```

### Docker Development

```bash
# Development with Docker
make dev               # Start development environment with hot reload
make prod             # Start production environment  
make build            # Build all Docker images in parallel
make build-backend    # Build specific service
make logs             # Show all logs (use SERVICE=name for specific service)
make health           # Check service health status
make status           # Show service status
make shell-backend    # Open shell in backend container
make shell-frontend   # Open shell in frontend container  
make test             # Run tests in containers
make clean            # Clean up containers, volumes, and images
```

### SSL Certificate Management

```bash
# SSL setup and management
make ssl-init DOMAIN=yourdomain.com SSL_EMAIL=you@yourdomain.com  # Initialize SSL certificates
make ssl-renew        # Manually renew SSL certificates
make ssl-status DOMAIN=yourdomain.com  # Check certificate status
make prod-ssl         # Start production with SSL enabled

# SSL environment variables
export DOMAIN=yourdomain.com
export SSL_EMAIL=you@yourdomain.com
export SSL_STAGING=0  # Set to 1 for Let's Encrypt staging
```

## Database Architecture

### Authentication & Authorization Models

The backend implements a complete authentication system based on Auth.js/NextAuth patterns:

- **User**: Core user model with UUID primary keys
- **Account**: OAuth provider accounts (Google, GitHub, etc.)
- **Session**: User session management
- **VerificationToken**: Email verification tokens
- **Authenticator**: WebAuthn/passkey support
- **ApiKey**: API key management with SHA-256 hashing

### Organization System

Multi-tenant organization structure:

- **Organization**: Core organization entity
- **OrganizationMember**: User-organization relationships with roles (Owner, Admin, Member, Viewer)
- **OrganizationInvitation**: Email-based invitations with expiration
- **ApiKey**: Can be scoped to either user or organization level

### Security Features

- API keys use one-way SHA-256 hashing (never stored in plain text)
- Scoped permissions using `ApiScope` enum (sandbox, snapshots, registries, volumes operations)
- Organization roles using `OrganizationRole` enum
- Foreign key cascade deletes for data integrity

## Configuration

### Backend Settings (apps/backend/app/core/config.py)

- Database URL: `postgresql://postgres:password@localhost:5432/sandbox`
- Redis URL: `redis://localhost:6379`
- CORS origins: localhost:3000 and localhost:8000
- Environment variables loaded from `.env` file

### API Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- Health check: http://localhost:8000/health

## SDK Usage

### Python SDK

```python
from sandbox import Sandbox, AsyncSandbox

# Sync client
with Sandbox(base_url="http://localhost:8000") as client:
    response = client.get_root()
    health = client.health_check()

# Async client
async with AsyncSandbox(base_url="http://localhost:8000") as client:
    response = await client.get_root()
```

### TypeScript SDK

```typescript
import { Sandbox } from '@sandbox/sdk';

const client = new Sandbox({ baseURL: 'http://localhost:8000' });
const response = await client.getRoot();
```
