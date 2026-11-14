import pytest
from src.ollama_client import OllamaClient


def test_ollama_client_success():
    client = OllamaClient()
    result = client.generate("qwen2.5:1.5b", "Classifique este chamado: ")
    assert result is not None
    assert isinstance(result, str)
    assert len(result) > 0


def test_ollama_client_invalid_model():
    client = OllamaClient()
    with pytest.raises(ValueError):
        client.generate("modelo_invalido", "Teste")


def test_ollama_client_connection_error():
    client = OllamaClient(base_url="http://localhost:9999")
    result = client.generate("qwen2.5:1.5b", "Teste")
    assert result is None