# Sandbox Backend

FastAPI backend service for the Sandbox application.

## Features

- FastAPI web framework
- SQLAlchemy ORM with PostgreSQL  
- Redis caching
- Alembic database migrations
- API versioning (v1, v2)
- Health check endpoints

## Development

```bash
# Install dependencies
uv sync

# Run the server
uv run sandbox

# Run migrations
alembic upgrade head
```

## API Documentation

- Swagger UI: http://localhost:8000/docs
- Health check: http://localhost:8000/api/v1/health
