import axios, { AxiosInstance, AxiosRequestConfig } from "axios";
import {
  SandboxResponse,
  HealthResponse,
  ClientConfig,
  RequestOptions,
} from "./types";

export class Sandbox {
  private client: AxiosInstance;

  constructor(config: ClientConfig = {}) {
    const baseURL = config.baseURL || "http://localhost:8000";
    const timeout = config.timeout || 30000;

    this.client = axios.create({
      baseURL,
      timeout,
      headers: {
        "Content-Type": "application/json",
        ...config.headers,
      },
    });

    // Request interceptor for logging or auth
    this.client.interceptors.request.use(
      (config) => config,
      (error) => Promise.reject(error)
    );

    // Response interceptor for error handling
    this.client.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response) {
          // Server responded with error status
          const message = error.response.data?.detail || error.message;
          throw new Error(`API Error: ${message}`);
        } else if (error.request) {
          // Request made but no response
          throw new Error("Network Error: No response from server");
        } else {
          // Something else happened
          throw error;
        }
      }
    );
  }

  async getRoot(): Promise<SandboxResponse> {
    const response = await this.client.get<SandboxResponse>("/");
    return response.data;
  }

  async healthCheck(): Promise<HealthResponse> {
    const response = await this.client.get<HealthResponse>("/health");
    return response.data;
  }

  async request<T = any>(
    method: string,
    path: string,
    options: RequestOptions = {}
  ): Promise<T> {
    const config: AxiosRequestConfig = {
      method,
      url: path,
      params: options.params,
      headers: options.headers,
      data: options.data,
    };

    const response = await this.client.request<T>(config);
    return response.data;
  }

  // Convenience methods
  async get<T = any>(path: string, options?: RequestOptions): Promise<T> {
    return this.request<T>("GET", path, options);
  }

  async post<T = any>(
    path: string,
    data?: any,
    options?: RequestOptions
  ): Promise<T> {
    return this.request<T>("POST", path, { ...options, data });
  }

  async put<T = any>(
    path: string,
    data?: any,
    options?: RequestOptions
  ): Promise<T> {
    return this.request<T>("PUT", path, { ...options, data });
  }

  async delete<T = any>(path: string, options?: RequestOptions): Promise<T> {
    return this.request<T>("DELETE", path, options);
  }

  async patch<T = any>(
    path: string,
    data?: any,
    options?: RequestOptions
  ): Promise<T> {
    return this.request<T>("PATCH", path, { ...options, data });
  }
}
