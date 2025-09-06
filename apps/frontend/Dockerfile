# Multi-stage build for production optimization
FROM node:18-alpine as base

WORKDIR /app

# Install dependencies needed for node-gyp and security updates
RUN apk add --no-cache libc6-compat \
    && apk upgrade --no-cache

# Development stage
FROM base as development

# Copy package files first for better caching
COPY package*.json ./

# Install all dependencies with clean npm cache
RUN npm install --cache /tmp/.npm \
    && rm -rf /tmp/.npm

# Copy application code
COPY . .

# Expose port
EXPOSE 3000

# Run in development mode with hot reload
CMD ["npm", "run", "dev"]

# Builder stage
FROM base as builder

# Copy package files first for better caching
COPY package*.json ./

# Install dependencies with clean cache
RUN npm install --cache /tmp/.npm \
    && rm -rf /tmp/.npm

# Copy application code
COPY . .

# Build arguments
ARG NEXT_PUBLIC_API_BASE_URL
ENV NEXT_PUBLIC_API_BASE_URL=$NEXT_PUBLIC_API_BASE_URL

# Build the application
RUN npm run build \
    && npm prune --production

# Production stage
FROM node:18-alpine as production

WORKDIR /app

# Install curl for health checks and security updates
RUN apk add --no-cache curl dumb-init \
    && apk upgrade --no-cache

# Create non-root user for security
RUN addgroup --system --gid 1001 nodejs \
    && adduser --system --uid 1001 nextjs --ingroup nodejs

# Copy built application from builder stage
COPY --from=builder --chown=nextjs:nodejs /app/.next ./.next
COPY --from=builder --chown=nextjs:nodejs /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/package*.json ./
COPY --from=builder --chown=nextjs:nodejs /app/node_modules ./node_modules

# Switch to non-root user
USER nextjs

# Expose port
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:3000/ || exit 1

# Set environment to production
ENV NODE_ENV=production \
    NEXT_TELEMETRY_DISABLED=1

# Run the application with dumb-init
ENTRYPOINT ["/usr/bin/dumb-init", "--"]
CMD ["npm", "start"]