import pytest

from src.app import (
    EvaluationFormatError,
    calculate_accuracy,
    format_measurement,
    load_evaluation,
)


def test_rejects_invalid_json() -> None:
    with pytest.raises(EvaluationFormatError, match="JSON inválido"):
        load_evaluation("{")


def test_rejects_empty_cases() -> None:
    content = (
        '{"execucao":{"modelo":{},"prompt":{}},"casos":[]}'
    )
    with pytest.raises(EvaluationFormatError, match="lista de casos está vazia"):
        load_evaluation(content)


def test_panel_opens_csv_results_and_switches_to_json_demo(tmp_path, monkeypatch):
    from streamlit.testing.v1 import AppTest

    from src import app

    saved = tmp_path / "saved.csv"
    saved.write_text(
        "model,input,expected,response,correct\n"
        "modelo-a,Chamado 1,Rede,Rede,true\n"
        "modelo-b,Chamado 1,Rede,Acesso,false\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(app, "RESULTS_FILE", saved)
    screen = AppTest.from_string(
        "from src.app import main\nmain()", default_timeout=30
    ).run()
    assert not screen.exception and not screen.error
    summary = screen.dataframe[0].value.set_index("Modelo")
    assert summary.loc["modelo-a", "Acertos"] == 1
    assert summary.loc["modelo-b", "Acertos"] == 0

    screen.radio[0].set_value("Demonstração JSON").run()
    assert not screen.exception and not screen.error
    assert any("dados sintéticos" in banner.value for banner in screen.info)


def test_accuracy_includes_failed_cases_in_denominator() -> None:
    cases = [
        {"acerto": True, "erro": None},
        {"acerto": False, "erro": {"codigo": "TIMEOUT"}},
    ]

    assert calculate_accuracy(cases) == 0.5


def test_null_measurements_remain_unmeasured() -> None:
    evaluation = load_evaluation(
        '{"execucao":{"modelo":{},"prompt":{}},"casos":'
        '[{"acerto":false,"tempo_ms":null,"tokens_entrada":null,"tokens_saida":null}]}'
    )

    case = evaluation["casos"][0]
    assert case["tempo_ms"] is None
    assert case["tokens_entrada"] is None
    assert case["tokens_saida"] is None
    assert format_measurement(case["tempo_ms"], " ms") == "Não medido"
    assert format_measurement(case["tokens_entrada"]) == "Não medido"


def test_rejects_execution_failure_marked_as_correct() -> None:
    content = (
        '{"execucao":{"modelo":{},"prompt":{}},"casos":'
        '[{"acerto":true,"erro":{"codigo":"TIMEOUT",'
        '"mensagem":"Tempo limite excedido."}}]}'
    )

    with pytest.raises(EvaluationFormatError, match="caso 1 registra uma falha de execução"):
        load_evaluation(content)
