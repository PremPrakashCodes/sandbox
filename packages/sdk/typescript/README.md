# Sandbox TypeScript SDK

TypeScript SDK for the Sandbox API.

## Installation

```bash
npm install @sandbox/sdk
```

## Usage

```typescript
import { SandboxClient } from '@sandbox/sdk';

// Initialize client
const client = new SandboxClient({
  baseURL: 'http://localhost:8000',
  timeout: 30000,
});

// Get root info
const rootInfo = await client.getRoot();
console.log(rootInfo.message); // "Welcome to Sandbox API"

// Health check
const health = await client.healthCheck();
console.log(health.status); // "healthy"

// Custom request
const data = await client.get('/api/custom-endpoint');

// POST request
const result = await client.post('/api/items', {
  name: 'Test Item',
  value: 123
});
```

## API Reference

### Constructor Options

```typescript
interface ClientConfig {
  baseURL?: string;  // Default: 'http://localhost:8000'
  timeout?: number;  // Default: 30000 (ms)
  headers?: Record<string, string>;
}
```

### Methods

- `getRoot()`: Get API root information
- `healthCheck()`: Check API health status
- `get(path, options?)`: Make GET request
- `post(path, data?, options?)`: Make POST request
- `put(path, data?, options?)`: Make PUT request
- `patch(path, data?, options?)`: Make PATCH request
- `delete(path, options?)`: Make DELETE request
- `request(method, path, options?)`: Make custom request

## Development

```bash
# Build the SDK
npm run build

# Watch mode for development
npm run dev

# Type checking
npm run type-check
```