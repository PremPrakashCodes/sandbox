import httpx
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field


class SandboxResponse(BaseModel):
    message: str
    version: Optional[str] = None


class HealthResponse(BaseModel):
    status: str


class Sandbox:
    def __init__(self, base_url: str = "http://localhost:8000", timeout: float = 30.0):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.client = httpx.Client(timeout=timeout)
    
    def __enter__(self):
        return self
    
    def __exit__(self, *args):
        self.client.close()
    
    def close(self):
        self.client.close()
    
    def get_root(self) -> SandboxResponse:
        response = self.client.get(f"{self.base_url}/")
        response.raise_for_status()
        return SandboxResponse(**response.json())
    
    def health_check(self) -> HealthResponse:
        response = self.client.get(f"{self.base_url}/health")
        response.raise_for_status()
        return HealthResponse(**response.json())
    
    def request(self, method: str, path: str, **kwargs) -> Dict[str, Any]:
        url = f"{self.base_url}/{path.lstrip('/')}"
        response = self.client.request(method, url, **kwargs)
        response.raise_for_status()
        return response.json()


class AsyncSandbox:
    def __init__(self, base_url: str = "http://localhost:8000", timeout: float = 30.0):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.client = httpx.AsyncClient(timeout=timeout)
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, *args):
        await self.client.aclose()
    
    async def close(self):
        await self.client.aclose()
    
    async def get_root(self) -> SandboxResponse:
        response = await self.client.get(f"{self.base_url}/")
        response.raise_for_status()
        return SandboxResponse(**response.json())
    
    async def health_check(self) -> HealthResponse:
        response = await self.client.get(f"{self.base_url}/health")
        response.raise_for_status()
        return HealthResponse(**response.json())
    
    async def request(self, method: str, path: str, **kwargs) -> Dict[str, Any]:
        url = f"{self.base_url}/{path.lstrip('/')}"
        response = await self.client.request(method, url, **kwargs)
        response.raise_for_status()
        return response.json()