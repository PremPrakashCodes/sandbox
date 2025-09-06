.PHONY: help build up down logs dev prod clean restart health status shell-backend shell-frontend test ssl-init ssl-renew ssl-status

# Default target
help:
	@echo "Available commands:"
	@echo "  dev        - Start development environment (with hot reload)"
	@echo "  prod       - Start production environment"
	@echo "  build      - Build all images"
	@echo "  up         - Start services"
	@echo "  down       - Stop services"
	@echo "  restart    - Restart services"
	@echo "  logs       - Show logs (use SERVICE=name for specific service)"
	@echo "  health     - Check service health status"
	@echo "  status     - Show service status"
	@echo "  shell-backend  - Open shell in backend container"
	@echo "  shell-frontend - Open shell in frontend container"
	@echo "  test       - Run tests in containers"
	@echo "  clean      - Clean up containers, volumes, and images"
	@echo ""
	@echo "SSL Commands:"
	@echo "  ssl-init   - Initialize SSL certificates (requires DOMAIN and SSL_EMAIL)"
	@echo "  ssl-renew  - Manually renew SSL certificates"
	@echo "  ssl-status - Check SSL certificate status"

# Development environment (uses docker-compose.override.yml automatically)
dev:
	docker compose up --build

# Production environment
prod:
	docker compose --profile production up --build -d

# Build all images
build:
	docker compose build --parallel

# Build specific service
build-%:
	docker compose build $*

# Start services
up:
	docker compose up -d

# Stop services
down:
	docker compose down

# Stop services and remove volumes
down-volumes:
	docker compose down -v

# Restart services
restart:
	docker compose restart

# Restart specific service
restart-%:
	docker compose restart $*

# Show logs (use make logs SERVICE=backend for specific service)
logs:
ifdef SERVICE
	docker compose logs -f $(SERVICE)
else
	docker compose logs -f
endif

# Check service health
health:
	@echo "Checking service health..."
	@docker compose ps --format "table {{.Service}}\t{{.Status}}\t{{.Ports}}"

# Show service status
status:
	docker compose ps

# Open shell in backend container
shell-backend:
	docker compose exec backend /bin/bash

# Open shell in frontend container  
shell-frontend:
	docker compose exec frontend /bin/sh

# Run tests
test:
	docker compose exec backend uv run python -m pytest
	docker compose exec frontend npm test

# Clean up everything
clean:
	docker compose down -v --rmi all --remove-orphans
	docker system prune -af --volumes

# Pull latest images
pull:
	docker compose pull

# Show docker compose config
config:
	docker compose config

# SSL certificate management
ssl-init:
	@echo "Initializing SSL certificates..."
	@if [ -z "$(DOMAIN)" ]; then echo "Error: DOMAIN not set. Use: make ssl-init DOMAIN=yourdomain.com SSL_EMAIL=you@yourdomain.com"; exit 1; fi
	@if [ -z "$(SSL_EMAIL)" ]; then echo "Error: SSL_EMAIL not set. Use: make ssl-init DOMAIN=yourdomain.com SSL_EMAIL=you@yourdomain.com"; exit 1; fi
	./scripts/init-ssl.sh

# Renew SSL certificates
ssl-renew:
	@echo "Renewing SSL certificates..."
	docker compose --profile ssl run --rm certbot renew
	docker compose exec nginx nginx -s reload

# Check SSL certificate status
ssl-status:
	@echo "SSL Certificate Status:"
	@if [ -z "$(DOMAIN)" ]; then echo "Error: DOMAIN not set. Use: make ssl-status DOMAIN=yourdomain.com"; exit 1; fi
	@docker-compose run --rm --entrypoint "\
		if [ -f '/etc/letsencrypt/live/$(DOMAIN)/fullchain.pem' ]; then \
			echo 'Certificate exists for $(DOMAIN)'; \
			openssl x509 -in '/etc/letsencrypt/live/$(DOMAIN)/fullchain.pem' -text -noout | grep -A2 'Validity'; \
		else \
			echo 'No certificate found for $(DOMAIN)'; \
		fi" certbot

# Start production with SSL
prod-ssl:
	@echo "Starting production environment with SSL..."
	docker compose --profile ssl --profile production up -d
