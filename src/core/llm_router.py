import os
import logging
from typing import Optional, Literal, Union
from langchain_openai import ChatOpenAI
from langchain_community.chat_models import ChatOllama
from langchain_core.language_models import BaseChatModel

logger = logging.getLogger(__name__)

COST_PER_1K_TOKENS = {
    "gpt-4-turbo-preview": 0.01,
    "gpt-3.5-turbo": 0.001,
}


class LLMRouter:
    """
    Routes LLM requests to either a local model (Ollama) or a cloud provider (OpenAI/Anthropic)
    based on the task complexity and privacy requirements.
    """
    
    def __init__(self):
        self.default_provider = os.getenv("DEFAULT_LLM_PROVIDER", "openai")
        self.ollama_base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        self.ollama_model = os.getenv("OLLAMA_MODEL", "llama3")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self._total_cost = 0.0
        
    def get_model(self, 
                  capability: Literal["fast", "smart", "private"] = "smart",
                  provider: Optional[str] = None) -> BaseChatModel:
        """
        Get an LLM instance based on the requested capability.
        
        Args:
            capability: 
                - 'fast': Optimized for speed (e.g., gpt-3.5-turbo, llama3-small).
                - 'smart': Optimized for quality (e.g., gpt-4, claude-3-opus).
                - 'private': Must run locally (e.g., llama3 via Ollama).
            provider: Override the default provider.
        
        Returns:
            A LangChain ChatModel instance.
        """
        target_provider = provider or self.default_provider
        
        if capability == "private":
            return self._get_ollama_model()
            
        if target_provider == "ollama":
            return self._get_ollama_model()
        elif target_provider == "openai":
            return self._get_openai_model(capability)
        else:
            if self.openai_api_key:
                return self._get_openai_model(capability)
            return self._get_ollama_model()
    
    def get_model_with_fallback(self,
                                capability: Literal["fast", "smart", "private"] = "smart",
                                provider: Optional[str] = None) -> BaseChatModel:
        """
        Get an LLM with failover: tries primary, falls back to Ollama on failure.
        """
        target_provider = provider or self.default_provider
        
        if target_provider == "openai" and self.openai_api_key:
            try:
                logger.info(f"Attempting OpenAI model with capability: {capability}")
                model = self._get_openai_model(capability)
                model.invoke("test")
                return model
            except Exception as e:
                logger.warning(f"OpenAI failed: {e}. Falling back to Ollama.")
                self._log_cost("openai-failover", 0)
                return self._get_ollama_model()
        
        return self.get_model(capability, provider)
    
    def _log_cost(self, model_name: str, tokens: int = 0):
        cost_per_1k = COST_PER_1K_TOKENS.get(model_name, 0)
        cost = (tokens / 1000) * cost_per_1k
        self._total_cost += cost
        logger.info(f"LLM Cost: ${cost:.4f} ({tokens} tokens) | Total: ${self._total_cost:.4f}")
    
    def get_total_cost(self) -> float:
        return self._total_cost
        
    def get_model(self, 
                  capability: Literal["fast", "smart", "private"] = "smart",
                  provider: Optional[str] = None) -> BaseChatModel:
        """
        Get an LLM instance based on the requested capability.
        
        Args:
            capability: 
                - 'fast': Optimized for speed (e.g., gpt-3.5-turbo, llama3-small).
                - 'smart': Optimized for quality (e.g., gpt-4, claude-3-opus).
                - 'private': Must run locally (e.g., llama3 via Ollama).
            provider: Override the default provider.
        
        Returns:
            A LangChain ChatModel instance.
        """
        target_provider = provider or self.default_provider
        
        # Force local provider if privacy is required
        if capability == "private":
            return self._get_ollama_model()
            
        if target_provider == "ollama":
            return self._get_ollama_model()
        elif target_provider == "openai":
            return self._get_openai_model(capability)
        else:
            # Fallback to OpenAI if configured, otherwise Ollama
            if self.openai_api_key:
                return self._get_openai_model(capability)
            return self._get_ollama_model()
    
    def _get_ollama_model(self) -> ChatOllama:
        return ChatOllama(
            base_url=self.ollama_base_url,
            model=self.ollama_model,
            temperature=0.1
        )
        
    def _get_openai_model(self, capability: str) -> ChatOpenAI:
        if not self.openai_api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables.")
            
        # Select model based on capability
        model_name = "gpt-4-turbo-preview" if capability == "smart" else "gpt-3.5-turbo"
        
        return ChatOpenAI(
            api_key=self.openai_api_key,
            model=model_name,
            temperature=0.7 if capability == "smart" else 0.1
        )

# Global router instance
llm_router = LLMRouter()
