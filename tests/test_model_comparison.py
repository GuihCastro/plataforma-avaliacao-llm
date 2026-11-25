import csv
import hashlib
import importlib.util
import json
from builtins import open as builtin_open
from pathlib import Path
from unittest.mock import Mock

import pytest
import requests

from eval import model_comparison
from src.llm_judge import LLMJudge as RealLLMJudge


MODEL_NAMES = (
    "qwen2.5:1.5b",
    "llama3.2:3b",
    "gemma3:1b",
    "qwen2.5:3b",
)


class FakeClient:
    base_url = "http://ollama.test:11434"

    def __init__(
        self,
        *,
        classifier_failure=False,
        judge_failure=False,
        classifier_response="Acesso",
    ):
        self.classifier_failure = classifier_failure
        self.judge_failure = judge_failure
        self.classifier_response = classifier_response
        self.last_error = None
        self.classifier_calls = 0
        self.judge_evaluations = 0
        self.output_path = None
        self.incremental_rows_seen = None

    def list_models(self):
        return [{"name": name, "digest": f"test-{name}"} for name in MODEL_NAMES]

    def generate(self, model, prompt):
        result = self.generate_with_metrics(model, prompt)
        return None if result is None else result["response"]

    def generate_with_metrics(self, model, prompt):
        self.last_error = None
        if model == "qwen2.5:3b":
            if self.judge_failure:
                self.last_error = "juiz indisponível"
                return None
            return self.metrics('{"correct": false, "reason": "simulado"}')

        self.classifier_calls += 1
        if self.output_path and self.classifier_calls == 2:
            with self.output_path.open(encoding="utf-8", newline="") as file:
                self.incremental_rows_seen = len(list(csv.DictReader(file)))
        if self.classifier_failure and self.classifier_calls == 1:
            self.last_error = "classificador indisponível"
            return None
        return self.metrics(self.classifier_response)

    @staticmethod
    def metrics(response):
        return {
            "response": response,
            "prompt_tokens": 11,
            "completion_tokens": 3,
            "total_tokens": 14,
            "total_duration_ns": 2_000_000_000,
        }


class FakeJudge:
    def __init__(self, client):
        self.client = client

    def evaluate(self, input_text, expected, response):
        self.client.judge_evaluations += 1
        if response.casefold() == expected.casefold():
            return {"correct": True, "reason": "correspondência exata"}
        self.client.generate("qwen2.5:3b", f"Juiz: {input_text}")
        return {"correct": False, "reason": "resultado simulado"}


@pytest.fixture
def prepared_run(tmp_path, monkeypatch):
    dataset_path = tmp_path / "test_cases.csv"
    with dataset_path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["input", "expected"])
        writer.writerows(
            (f"Chamado {index}", "Rede")
            for index in range(1, 101)
        )

    client = FakeClient()
    monkeypatch.setattr(model_comparison, "MODELS", ("qwen2.5:1.5b",))
    monkeypatch.setattr(
        model_comparison,
        "LLMJudge",
        lambda: FakeJudge(client),
    )
    return tmp_path, dataset_path, client


def test_import_has_no_evaluation_side_effects(tmp_path, monkeypatch, capsys):
    get = Mock()
    post = Mock()
    monkeypatch.setattr(requests, "get", get)
    monkeypatch.setattr(requests, "post", post)
    monkeypatch.chdir(tmp_path)

    module_path = (
        Path(model_comparison.__file__).resolve().parent
        / "model_comparison.py"
    )
    spec = importlib.util.spec_from_file_location(
        "model_comparison_import_check",
        module_path,
    )
    imported_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(imported_module)

    assert capsys.readouterr().out == ""
    get.assert_not_called()
    post.assert_not_called()
    assert list(tmp_path.iterdir()) == []


def test_existing_output_is_rejected_before_inference(
    prepared_run, monkeypatch
):
    tmp_path, dataset_path, client = prepared_run
    output_path = tmp_path / "already-there.csv"
    output_path.write_text("preserve me", encoding="utf-8")
    client.generate_with_metrics = Mock(
        side_effect=AssertionError("inferência não pode começar")
    )
    monkeypatch.setattr(
        model_comparison,
        "LLMJudge",
        lambda: FakeJudge(client),
    )

    with pytest.raises(FileExistsError, match="já existe"):
        model_comparison.run_evaluation(output_path, dataset_path)

    assert output_path.read_text(encoding="utf-8") == "preserve me"
    client.generate_with_metrics.assert_not_called()


def test_missing_model_stops_before_creating_output_or_inference(
    prepared_run, monkeypatch
):
    tmp_path, dataset_path, client = prepared_run
    output_path = tmp_path / "missing-model.csv"
    monkeypatch.setattr(
        model_comparison,
        "MODELS",
        ("qwen2.5:1.5b", "llama3.2:3b", "gemma3:1b"),
    )
    client.list_models = lambda: [
        {"name": name} for name in MODEL_NAMES if name != "gemma3:1b"
    ]
    client.generate_with_metrics = Mock(
        side_effect=AssertionError("inferência não pode começar")
    )

    with pytest.raises(RuntimeError, match="gemma3:1b"):
        model_comparison.run_evaluation(output_path, dataset_path)

    assert not output_path.exists()
    assert not Path(f"{output_path}.metadata.json").exists()
    client.generate_with_metrics.assert_not_called()


def test_metadata_created_during_preflight_is_preserved(
    prepared_run, monkeypatch
):
    tmp_path, dataset_path, client = prepared_run
    output_path = tmp_path / "racing.csv"
    metadata_path = Path(f"{output_path}.metadata.json")
    preserved_content = '{"owner":"another process"}\n'
    original_path_open = Path.open

    def create_sidecar_before_exclusive_open(path, mode="r", *args, **kwargs):
        if path == metadata_path and mode == "x":
            with builtin_open(path, "w", encoding="utf-8") as file:
                file.write(preserved_content)
        return original_path_open(path, mode, *args, **kwargs)

    monkeypatch.setattr(Path, "open", create_sidecar_before_exclusive_open)

    with pytest.raises(FileExistsError):
        model_comparison.run_evaluation(output_path, dataset_path)

    with builtin_open(metadata_path, encoding="utf-8") as file:
        assert file.read() == preserved_content
    assert not output_path.exists()
    assert client.classifier_calls == 0


def test_csv_is_flushed_incrementally_and_metadata_records_run(
    prepared_run,
):
    tmp_path, dataset_path, client = prepared_run
    output_path = tmp_path / "incremental.csv"
    client.output_path = output_path

    result_path, metadata_path = model_comparison.run_evaluation(
        output_path,
        dataset_path,
    )

    with result_path.open(encoding="utf-8", newline="") as file:
        rows = list(csv.DictReader(file))
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    assert client.incremental_rows_seen == 1
    assert len(rows) == 100
    assert {
        "model", "input", "expected", "response", "correct",
        "latency_seconds", "prompt_tokens", "completion_tokens",
        "total_tokens", "ollama_duration_seconds",
        "judge_correct", "judge_reason",
    }.issubset(rows[0])
    assert rows[0]["prompt_tokens"] == "11"
    assert rows[0]["judge_prompt_tokens"] == "11"
    assert rows[0]["judge_calls"] == "1"
    assert metadata["status"] == "completed"
    assert metadata["completed_cases"] == 100
    assert metadata["dataset"]["sha256"] == hashlib.sha256(
        dataset_path.read_bytes()
    ).hexdigest()
    assert metadata["started_at_utc"].endswith("Z")
    assert metadata["finished_at_utc"].endswith("Z")
    assert len(metadata["prompts"]["classifier_calls"]) == 100
    assert len(metadata["prompts"]["judge_calls"]) == 100


@pytest.mark.parametrize("failure_type", ["classifier", "judge"])
def test_failures_are_explicit_and_missing_metrics_are_blank(
    prepared_run, monkeypatch, failure_type
):
    tmp_path, dataset_path, client = prepared_run
    output_path = tmp_path / f"{failure_type}-failure.csv"
    if failure_type == "classifier":
        client.classifier_failure = True
    else:
        client.judge_failure = True

    _, metadata_path = model_comparison.run_evaluation(
        output_path,
        dataset_path,
    )
    with output_path.open(encoding="utf-8", newline="") as file:
        first_row = next(csv.DictReader(file))
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))

    if failure_type == "classifier":
        assert first_row["model_error"] == "classificador indisponível"
        assert first_row["response"] == ""
        assert first_row["prompt_tokens"] == ""
        assert first_row["total_tokens"] == ""
        assert first_row["judge_calls"] == "0"
        assert metadata["prompts"]["classifier_calls"][0]["status"] == "failed"
    else:
        assert first_row["model_error"] == ""
        assert first_row["prompt_tokens"] == "11"
        assert first_row["judge_error"] == "juiz indisponível"
        assert first_row["judge_prompt_tokens"] == ""
        assert first_row["judge_total_tokens"] == ""
        assert metadata["prompts"]["judge_calls"][0]["status"] == "failed"


@pytest.mark.parametrize("response", ["", " \t\n"])
def test_empty_classifier_response_is_a_failure_without_judge(
    prepared_run, response
):
    tmp_path, dataset_path, client = prepared_run
    client.classifier_response = response
    output_path = tmp_path / "empty-classifier.csv"

    _, metadata_path = model_comparison.run_evaluation(
        output_path,
        dataset_path,
    )
    with output_path.open(encoding="utf-8", newline="") as file:
        first_row = next(csv.DictReader(file))
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))

    assert first_row["response"] == ""
    assert first_row["correct"] == "False"
    assert first_row["model_error"] == "Modelo retornou resposta vazia."
    assert first_row["prompt_tokens"] == "11"
    assert first_row["completion_tokens"] == "3"
    assert first_row["total_tokens"] == "14"
    assert first_row["judge_calls"] == "0"
    assert first_row["judge_correct"] == ""
    assert client.judge_evaluations == 0
    assert metadata["prompts"]["classifier_calls"][0]["status"] == "failed"


@pytest.mark.parametrize(
    ("judge_response", "expected_error"),
    [
        ("", "Resposta do juiz está vazia"),
        ("não-json", "Resposta do juiz não é um JSON válido"),
        (
            '{"correct": "false", "reason": "tipo inválido"}',
            "'correct' deve ser um booleano",
        ),
        (
            '{"correct": false, "reason": 1}',
            "'reason' deve ser uma string",
        ),
        ('{"correct": false, "reason": "Negativa válida"}', None),
    ],
)
def test_real_judge_interpretation_errors_have_no_verdict(
    prepared_run,
    monkeypatch,
    judge_response,
    expected_error,
):
    tmp_path, dataset_path, _ = prepared_run
    output_path = tmp_path / "real-judge.csv"
    monkeypatch.setattr(model_comparison, "LLMJudge", RealLLMJudge)
    monkeypatch.setattr(
        model_comparison,
        "_read_examples",
        lambda _: ([("Chamado simulado", "Rede")], "sha256-simulado"),
    )
    monkeypatch.setenv("OLLAMA_BASE_URL", "http://ollama.test:11434")

    tags_response = Mock()
    tags_response.raise_for_status.return_value = None
    tags_response.json.return_value = {
        "models": [{"name": name, "digest": f"test-{name}"} for name in MODEL_NAMES]
    }
    monkeypatch.setattr(requests, "get", Mock(return_value=tags_response))

    def simulated_generation(url, json, timeout):
        if json["model"] == "qwen2.5:3b":
            response_text = judge_response
            prompt_tokens, completion_tokens, duration = 7, 2, 4_000_000
        else:
            response_text = "Acesso"
            prompt_tokens, completion_tokens, duration = 5, 1, 3_000_000
        response = Mock()
        response.raise_for_status.return_value = None
        response.json.return_value = {
            "response": response_text,
            "prompt_eval_count": prompt_tokens,
            "eval_count": completion_tokens,
            "total_duration": duration,
        }
        return response

    monkeypatch.setattr(
        requests,
        "post",
        Mock(side_effect=simulated_generation),
    )

    model_comparison.run_evaluation(output_path, dataset_path)
    with output_path.open(encoding="utf-8", newline="") as file:
        row = next(csv.DictReader(file))

    assert row["model_error"] == ""
    assert row["prompt_tokens"] == "5"
    assert row["judge_prompt_tokens"] == "7"
    assert row["judge_completion_tokens"] == "2"
    assert row["judge_total_tokens"] == "9"
    if expected_error is None:
        assert row["judge_correct"] == "False"
        assert row["judge_error"] == ""
    else:
        assert row["judge_correct"] == ""
        assert expected_error in row["judge_error"]
