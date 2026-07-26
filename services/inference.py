import os
import httpx
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from config.settings import settings

class ILLMProvider(ABC):
    """
    Interface for LLM Model Provider adapters.
    All adapters must implement the async generate_completion method.
    """
    @abstractmethod
    async def generate_completion(
        self, 
        messages: List[Dict[str, str]], 
        temperature: float = 0.2, 
        max_tokens: int = 2048,
        **kwargs
    ) -> Dict[str, Any]:
        pass

class OpenAIAdapter(ILLMProvider):
    def __init__(self, api_key: str, model: str = "gpt-4o"):
        self.api_key = api_key
        self.model = model
        self.endpoint = "https://api.openai.com/v1/chat/completions"

    async def generate_completion(self, messages: List[Dict[str, str]], temperature: float = 0.2, max_tokens: int = 2048, **kwargs) -> Dict[str, Any]:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(self.endpoint, json=payload, headers=headers, timeout=60.0)
            response.raise_for_status()
            data = response.json()
            return {
                "text": data["choices"][0]["message"]["content"],
                "model": self.model,
                "usage": data["usage"]
            }

class GoogleAdapter(ILLMProvider):
    def __init__(self, api_key: str, model: str = "gemini-1.5-flash"):
        self.api_key = api_key
        self.model = model
        self.endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"

    async def generate_completion(self, messages: List[Dict[str, str]], temperature: float = 0.2, max_tokens: int = 2048, **kwargs) -> Dict[str, Any]:
        # Translate messaging structure to Gemini format
        contents = []
        for msg in messages:
            role = "user" if msg["role"] == "user" else "model"
            contents.append({
                "role": role,
                "parts": [{"text": msg["content"]}]
            })
        
        payload = {
            "contents": contents,
            "generationConfig": {
                "temperature": temperature,
                "maxOutputTokens": max_tokens
            }
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(self.endpoint, json=payload, timeout=60.0)
            response.raise_for_status()
            data = response.json()
            return {
                "text": data["candidates"][0]["content"]["parts"][0]["text"],
                "model": self.model,
                "usage": {"total_tokens": 0} # Gemini free tier may not return exact token counts
            }

class OllamaAdapter(ILLMProvider):
    def __init__(self, host: str = "http://localhost:11434", model: str = "llama3.1"):
        self.host = host
        self.model = model
        self.endpoint = f"{host}/api/chat"

    async def generate_completion(self, messages: List[Dict[str, str]], temperature: float = 0.2, max_tokens: int = 2048, **kwargs) -> Dict[str, Any]:
        payload = {
            "model": self.model,
            "messages": messages,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens
            },
            "stream": False
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(self.endpoint, json=payload, timeout=90.0)
            response.raise_for_status()
            data = response.json()
            return {
                "text": data["message"]["content"],
                "model": self.model,
                "usage": {"total_tokens": data.get("eval_count", 0)}
            }

class LLMProviderFactory:
    """
    Factory to dynamically resolve provider adapters based on runtime configurations.
    """
    @staticmethod
    def get_provider(provider_name: Optional[str] = None, model_name: Optional[str] = None) -> ILLMProvider:
        prov = provider_name or settings.DEFAULT_LLM_PROVIDER
        model = model_name or settings.DEFAULT_LLM_MODEL
        
        if prov == "openai":
            return OpenAIAdapter(api_key=os.getenv("OPENAI_API_KEY", "mock-key"), model=model)
        elif prov == "google":
            return GoogleAdapter(api_key=os.getenv("GEMINI_API_KEY", "mock-key"), model=model)
        elif prov == "ollama":
            return OllamaAdapter(host=os.getenv("OLLAMA_HOST", "http://localhost:11434"), model=model)
        else:
            # Return a simple mock provider for sandbox environments
            class MockProvider(ILLMProvider):
                async def generate_completion(self, messages, temperature=0.2, max_tokens=2048, **kwargs):
                    return {
                        "text": f"Mock execution using model '{model}' for prompt: '{messages[-1]['content']}'",
                        "model": model,
                        "usage": {"total_tokens": 12}
                    }
            return MockProvider()
