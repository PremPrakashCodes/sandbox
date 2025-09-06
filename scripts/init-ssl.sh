#!/bin/bash

# SSL Certificate Initialization Script
# This script sets up Let's Encrypt SSL certificates for your domain

set -e

# Configuration
DOMAIN=${DOMAIN:-"localhost"}
EMAIL=${SSL_EMAIL:-""}
STAGING=${SSL_STAGING:-0}

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Helper functions
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if domain is provided
if [ "$DOMAIN" = "localhost" ] || [ -z "$DOMAIN" ]; then
    log_error "Domain not set. Please set DOMAIN environment variable."
    log_info "Example: DOMAIN=yourdomain.com SSL_EMAIL=you@yourdomain.com ./scripts/init-ssl.sh"
    exit 1
fi

# Check if email is provided
if [ -z "$EMAIL" ]; then
    log_error "Email not set. Please set SSL_EMAIL environment variable."
    log_info "Example: DOMAIN=yourdomain.com SSL_EMAIL=you@yourdomain.com ./scripts/init-ssl.sh"
    exit 1
fi

log_info "Initializing SSL certificates for domain: $DOMAIN"
log_info "Email: $EMAIL"
log_info "Staging mode: $STAGING"

# Create necessary directories locally
log_info "Creating certificate directories..."
mkdir -p ./ssl-temp

# Download recommended TLS parameters to local temp directory
log_info "Downloading recommended TLS parameters..."
curl -s https://raw.githubusercontent.com/certbot/certbot/master/certbot-nginx/certbot_nginx/_internal/tls_configs/options-ssl-nginx.conf > ./ssl-temp/options-ssl-nginx.conf
curl -s https://raw.githubusercontent.com/certbot/certbot/master/certbot/certbot/ssl-dhparams.pem > ./ssl-temp/ssl-dhparams.pem

# Copy TLS parameters to certbot volume
docker-compose run --rm --entrypoint "\
    mkdir -p /etc/letsencrypt && \
    mkdir -p /var/www/certbot" certbot

# Copy the files from local temp to docker volume
docker-compose run --rm -v "$(pwd)/ssl-temp:/temp" --entrypoint "\
    cp /temp/options-ssl-nginx.conf /etc/letsencrypt/ && \
    cp /temp/ssl-dhparams.pem /etc/letsencrypt/" certbot

# Clean up temp directory
rm -rf ./ssl-temp

# Create dummy certificate for the domain
log_info "Creating dummy certificate for $DOMAIN..."
docker-compose run --rm --entrypoint "\
    mkdir -p /etc/letsencrypt/live/$DOMAIN && \
    openssl req -x509 -nodes -newkey rsa:2048 -days 1 \
    -keyout '/etc/letsencrypt/live/$DOMAIN/privkey.pem' \
    -out '/etc/letsencrypt/live/$DOMAIN/fullchain.pem' \
    -subj '/CN=localhost'" certbot

# Start nginx
log_info "Starting nginx..."
docker-compose up --force-recreate -d nginx

# Delete dummy certificate
log_info "Deleting dummy certificate for $DOMAIN..."
docker-compose run --rm --entrypoint "\
    rm -Rf /etc/letsencrypt/live/$DOMAIN && \
    rm -Rf /etc/letsencrypt/archive/$DOMAIN && \
    rm -Rf /etc/letsencrypt/renewal/$DOMAIN.conf" certbot

# Request Let's Encrypt certificate
log_info "Requesting Let's Encrypt certificate for $DOMAIN..."

# Set staging flag
staging_arg=""
if [ $STAGING != "0" ]; then
    staging_arg="--staging"
    log_warn "Running in staging mode. Use SSL_STAGING=0 for production certificates."
fi

# Join domains for multi-domain support
domain_args=""
for domain in $(echo $DOMAIN | tr "," "\n"); do
    domain_args="$domain_args -d $domain"
done

docker-compose run --rm --entrypoint "\
    certbot certonly --webroot -w /var/www/certbot \
    $staging_arg \
    --email $EMAIL \
    $domain_args \
    --rsa-key-size 4096 \
    --agree-tos \
    --force-renewal \
    --non-interactive" certbot

# Reload nginx
log_info "Reloading nginx..."
docker-compose exec nginx nginx -s reload

log_info "SSL certificate successfully obtained and nginx reloaded!"
log_info ""
log_info "Next steps:"
log_info "1. Update your DNS to point to this server"
log_info "2. Test your SSL configuration at https://$DOMAIN"
log_info "3. Certificates will auto-renew every 12 hours"
log_info ""
log_info "To view certificate info: openssl x509 -in data/certbot/conf/live/$DOMAIN/fullchain.pem -text -noout"