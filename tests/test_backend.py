import os
import sys
from unittest.mock import patch

# Permite importar os arquivos da pasta src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from avaliador import executar_avaliacao


@patch("avaliador.gerar_classificacao")
def test_executar_avaliacao_gera_csv(mock_gerar):
    # Simula a resposta do Ollama sem precisar do servidor ligado no GitHub Actions
    mock_gerar.return_value = {
        "response": "Suporte Técnico",
        "latency_seconds": 0.45,
        "tokens": 12,
    }

    executar_avaliacao(modelo="modelo-teste", prompt_version="v1-test")

    assert os.path.exists("eval/results/resultados_backend.csv")
    assert os.path.exists("evidencias/execucao_backend.log")
