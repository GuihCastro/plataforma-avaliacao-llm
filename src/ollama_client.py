import os
import time
import requests

# Pega o endereço do Ollama e garante que tenha http:// na frente
host_bruto = os.getenv("OLLAMA_HOST", "http://localhost:11434").strip()
if not host_bruto.startswith("http"):
    host_bruto = f"http://{host_bruto}"
OLLAMA_URL = host_bruto.replace("0.0.0.0", "localhost")


def gerar_classificacao(modelo: str, prompt: str) -> dict:
    """Envia um prompt ao Ollama e retorna a resposta, latência e tokens."""
    url = f"{OLLAMA_URL}/api/generate"
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
