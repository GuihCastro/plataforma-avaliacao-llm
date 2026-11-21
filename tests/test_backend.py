import csv
import os
import subprocess
import sys
from pathlib import Path


def test_executar_avaliacao_gera_csv(tmp_path):
    source_dir = Path(__file__).resolve().parent.parent / "src"
    script = """
from unittest.mock import patch

with patch("ollama_client.gerar_classificacao") as mock_gerar:
    mock_gerar.return_value = {
        "response": "Suporte Técnico",
        "latency_seconds": 0.45,
        "tokens": 12,
    }

    from avaliador import executar_avaliacao
    executar_avaliacao(modelo="modelo-teste", prompt_version="v1-test")
    assert mock_gerar.call_count == 3
"""
    environment = os.environ.copy()
    existing_pythonpath = environment.get("PYTHONPATH")
    environment["PYTHONPATH"] = (
        str(source_dir)
        if not existing_pythonpath
        else str(source_dir) + os.pathsep + existing_pythonpath
    )

    subprocess.run(
        [sys.executable, "-c", script],
        cwd=tmp_path,
        env=environment,
        check=True,
        capture_output=True,
        text=True,
        timeout=30,
    )

    csv_path = tmp_path / "eval" / "results" / "resultados_backend.csv"
    log_path = tmp_path / "evidencias" / "execucao_backend.log"
    assert csv_path.is_file()
    assert log_path.is_file()
    with csv_path.open(encoding="utf-8", newline="") as result_file:
        rows = list(csv.DictReader(result_file))
    assert len(rows) == 3
    assert all(row["model"] == "modelo-teste" for row in rows)
    assert all(row["prompt_version"] == "v1-test" for row in rows)
