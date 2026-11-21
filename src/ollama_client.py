import os
import time
import requests
from typing import Optional
from urllib.parse import urlsplit, urlunsplit


DEFAULT_OLLAMA_URL = "http://localhost:11434"


def _normalize_base_url(base_url: str) -> str:
    """Normaliza o endereço usado pelo Ollama em ambiente local ou Docker."""
    host = base_url.strip()
    if not host:
        return DEFAULT_OLLAMA_URL
    if not host.startswith("http://") and not host.startswith("https://"):
        host = f"http://{host}"

    parsed = urlsplit(host)
    userinfo, separator, hostport = parsed.netloc.rpartition("@")
    prefix = f"{userinfo}@" if separator else ""

    if hostport == "0.0.0.0":
        hostport = "localhost"
    elif hostport.startswith("0.0.0.0:"):
        hostport = f"localhost:{hostport[len('0.0.0.0:'):]}"

    normalized = urlunsplit((
        parsed.scheme,
        f"{prefix}{hostport}",
        parsed.path,
        parsed.query,
        parsed.fragment,
    ))
    return normalized.rstrip("/") if parsed.path == "" else normalized


def _resolve_base_url(base_url: Optional[str] = None) -> str:
    if base_url:
        return _normalize_base_url(base_url)

    configured = os.getenv("OLLAMA_BASE_URL")
    if configured:
        return _normalize_base_url(configured)

    configured = os.getenv("OLLAMA_HOST")
    if configured:
        return _normalize_base_url(configured)

    return DEFAULT_OLLAMA_URL


class OllamaClient:
    def __init__(self, base_url: Optional[str] = None):
        self.base_url = _resolve_base_url(base_url)

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


OLLAMA_URL = _resolve_base_url()


def gerar_classificacao(modelo: str, prompt: str) -> dict:
    """Envia um prompt ao Ollama e retorna a resposta, latência e tokens."""
    url = f"{_resolve_base_url()}/api/generate"
    payload = {
        "model": modelo,
        "prompt": prompt,
        "stream": False,
    }

    inicio = time.time()
    resposta_http = requests.post(url, json=payload, timeout=60)
    resposta_http.raise_for_status()
    fim = time.time()

    dados = resposta_http.json()

    return {
        "response": dados.get("response", "").strip(),
        "latency_seconds": round(fim - inicio, 3),
        "tokens": dados.get("eval_count", 0),
    }
