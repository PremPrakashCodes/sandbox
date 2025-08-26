export interface SandboxResponse {
  message: string;
  version?: string;
}

export interface HealthResponse {
  status: string;
}

export interface ClientConfig {
  baseURL?: string;
  timeout?: number;
  headers?: Record<string, string>;
}

export interface RequestOptions {
  params?: Record<string, any>;
  headers?: Record<string, string>;
  data?: any;
}