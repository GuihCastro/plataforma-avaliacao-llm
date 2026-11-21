import pytest
from unittest.mock import Mock, patch

import requests

from src.ollama_client import (
    OllamaClient,
    gerar_classificacao,
)


def mock_response(payload, status_error=None):
    response = Mock()
    response.json.return_value = payload
    if status_error is not None:
        response.raise_for_status.side_effect = status_error
    else:
        response.raise_for_status.return_value = None
    return response


@patch("src.ollama_client.requests.post")
def test_generate_preserves_string_contract(post):
    post.return_value = mock_response({"response": "Rede"})

    result = OllamaClient(base_url="http://ollama.test:11434").generate(
        "qwen2.5:1.5b",
        "Classifique",
    )

    assert result == "Rede"
    post.assert_called_once_with(
        "http://ollama.test:11434/api/generate",
        json={
            "model": "qwen2.5:1.5b",
            "prompt": "Classifique",
            "stream": False,
        },
        timeout=120,
    )


@patch("src.ollama_client.requests.post")
def test_generate_with_metrics_preserves_metrics_contract(post):
    post.return_value = mock_response({
        "response": "Hardware",
        "prompt_eval_count": 11,
        "eval_count": 7,
        "total_duration": 123,
        "load_duration": 45,
        "prompt_eval_duration": 30,
        "eval_duration": 48,
    })

    result = OllamaClient(base_url="http://localhost:11434").generate_with_metrics(
        "llama3.2:3b",
        "Classifique",
    )

    assert result == {
        "response": "Hardware",
        "prompt_tokens": 11,
        "completion_tokens": 7,
        "total_tokens": 18,
        "total_duration_ns": 123,
        "load_duration_ns": 45,
        "prompt_eval_duration_ns": 30,
        "eval_duration_ns": 48,
    }


@patch("src.ollama_client.requests.post")
def test_gerar_classificacao_preserves_backend_contract(post):
    post.return_value = mock_response({
        "response": "  Software  ",
        "eval_count": 5,
    })

    result = gerar_classificacao("gemma3:1b", "Classifique")

    assert result["response"] == "Software"
    assert result["tokens"] == 5
    assert isinstance(result["latency_seconds"], float)


def test_base_url_priority(monkeypatch):
    monkeypatch.setenv("OLLAMA_BASE_URL", "base.internal:9999")
    monkeypatch.setenv("OLLAMA_HOST", "host.internal:11434")

    assert OllamaClient().base_url == "http://base.internal:9999"
    assert OllamaClient(base_url="0.0.0.0:8080").base_url == "http://localhost:8080"


def test_only_exact_unspecified_hostname_is_normalized(monkeypatch):
    monkeypatch.delenv("OLLAMA_BASE_URL", raising=False)
    monkeypatch.delenv("OLLAMA_HOST", raising=False)

    assert OllamaClient(base_url="http://10.0.0.0:11434").base_url == "http://10.0.0.0:11434"
    assert OllamaClient(
        base_url="http://node-0.0.0.0.example:11434"
    ).base_url == "http://node-0.0.0.0.example:11434"


def test_ollama_host_is_used_after_base_url(monkeypatch):
    monkeypatch.delenv("OLLAMA_BASE_URL", raising=False)
    monkeypatch.setenv("OLLAMA_HOST", "http://ollama:11434")

    assert OllamaClient().base_url == "http://ollama:11434"


def test_local_default_address(monkeypatch):
    monkeypatch.delenv("OLLAMA_BASE_URL", raising=False)
    monkeypatch.delenv("OLLAMA_HOST", raising=False)

    assert OllamaClient().base_url == "http://localhost:11434"


def test_ollama_client_invalid_model():
    client = OllamaClient()
    with pytest.raises(ValueError, match="Modelo modelo_invalido não suportado"):
        client.generate("modelo_invalido", "Teste")


@patch("src.ollama_client.requests.post")
def test_ollama_client_connection_error(post, capsys):
    post.side_effect = requests.exceptions.ConnectionError("sem conexão")

    result = OllamaClient(base_url="http://localhost:9999").generate(
        "qwen2.5:1.5b",
        "Teste",
    )

    assert result is None
    assert "Erro de conexão: sem conexão" in capsys.readouterr().out


@patch("src.ollama_client.requests.post")
def test_ollama_client_http_error(post, capsys):
    post.return_value = mock_response(
        {},
        requests.exceptions.HTTPError("500 Server Error"),
    )

    result = OllamaClient().generate_with_metrics(
        "qwen2.5:1.5b",
        "Teste",
    )

    assert result is None
    assert "Erro de conexão: 500 Server Error" in capsys.readouterr().out
