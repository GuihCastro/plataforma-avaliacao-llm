import os
import requests
from typing import Optional


class OllamaClient:
    def __init__(self, base_url: Optional[str] = None):
        self.base_url = base_url or os.getenv(
            "OLLAMA_BASE_URL",
            "http://localhost:11434"
        )

    def generate(self, model: str, prompt: str) -> Optional[str]:
        """Envia uma mensagem e retorna somente o texto da resposta."""
        result = self.generate_with_metrics(model, prompt)

        if result is None:
            return None

        return result["response"]

    def generate_with_metrics(self, model: str, prompt: str):
        """Envia uma mensagem e retorna resposta e métricas de uso."""

        supported_models = [
            "qwen2.5:1.5b",
            "llama3.2:3b",
            "gemma3:1b",
            "qwen2.5:3b"
        ]

        if model not in supported_models:
            raise ValueError(
                f"Modelo {model} não suportado. "
                f"Modelos disponíveis: {', '.join(supported_models)}"
            )

        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": model,
                    "prompt": prompt,
                    "stream": False
                },
                timeout=120
            )

            response.raise_for_status()
            data = response.json()

            return {
                "response": data.get("response", ""),
                "prompt_tokens": data.get("prompt_eval_count", 0),
                "completion_tokens": data.get("eval_count", 0),
                "total_tokens": (
                    data.get("prompt_eval_count", 0)
                    + data.get("eval_count", 0)
                ),
                "total_duration_ns": data.get("total_duration", 0),
                "load_duration_ns": data.get("load_duration", 0),
                "prompt_eval_duration_ns": data.get(
                    "prompt_eval_duration", 0
                ),
                "eval_duration_ns": data.get("eval_duration", 0)
            }

        except requests.exceptions.RequestException as e:
            print(f"Erro de conexão: {str(e)}")
            return None