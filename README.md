# Sandbox Monorepo

A monorepo containing a Next.js frontend, FastAPI backend, and SDKs.

## Structure

```
.
├── apps/
│   ├── frontend/     # Next.js application
│   └── backend/      # FastAPI application
├── packages/
│   └── sdk/
│       ├── python/   # Python SDK
│       └── typescript/  # TypeScript SDK (future)
```

## Requirements

- Node.js 18+
- Python 3.12
- uv (for Python package management)

## Setup

### Install dependencies

```bash
# Install Node.js dependencies
npm install

# Install Python dependencies for backend
cd apps/backend
uv sync

# Install Python dependencies for SDK
cd packages/sdk/python
uv sync
```

## Development

### Run all services

```bash
npm run dev
```

### Run services individually

```bash
# Frontend only
npm run dev:frontend

# Backend only
npm run dev:backend
```

### Backend API

The FastAPI backend runs on http://localhost:8000 by default.

- API documentation: http://localhost:8000/docs
- Health check: http://localhost:8000/health

### Frontend

The Next.js frontend runs on http://localhost:3000 by default.

## Python SDK Usage

```python
from sandbox import SandboxClient

# Sync client
with SandboxClient(base_url="http://localhost:8000") as client:
    response = client.get_root()
    print(response.message)
    
    health = client.health_check()
    print(health.status)

# Async client
import asyncio
from sandbox import AsyncSandboxClient

async def main():
    async with AsyncSandboxClient(base_url="http://localhost:8000") as client:
        response = await client.get_root()
        print(response.message)

asyncio.run(main())
```