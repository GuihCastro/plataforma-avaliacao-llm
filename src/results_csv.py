"""Leitura dos resultados gravados por eval/model_comparison.py."""

import csv
import math
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from io import StringIO
from typing import Literal, TypeVar


Number = TypeVar("Number", int, float)


class ResultsCSVError(ValueError):
    """O arquivo não segue o formato de resultados do projeto."""


@dataclass(frozen=True)
class CaseResult:
    record: int
    ticket: str
    expected: str
    response: str
    correct: bool
    latency_seconds: float | None
    prompt_tokens: int | None
    completion_tokens: int | None
    total_tokens: int | None
    judge_correct: bool | None
    judge_reason: str


@dataclass(frozen=True)
class PromptRegressionCase:
    record: int
    ticket: str
    expected: str
    original_response: str
    original_correct: bool
    degraded_response: str
    degraded_correct: bool


def _boolean(value: str, column: str, line: int) -> bool:
    normalized = value.strip().lower()
    if normalized in ("true", "false"):
        return normalized == "true"
    raise ResultsCSVError(f"Linha {line}: '{column}' deve conter true ou false.")


def _metric(row: dict[str, str], column: str, line: int, kind: type[Number]) -> Number | None:
    value = row.get(column, "").strip()
    if not value:
        return None
    try:
        number = kind(value)
        if number < 0 or (isinstance(number, float) and not math.isfinite(number)):
            raise ValueError
        return number
    except ValueError as exc:
        raise ResultsCSVError(f"Linha {line}: valor inválido em '{column}'.") from exc


def read_results_csv(content: bytes | str) -> dict[str | None, dict[str, list[CaseResult]]]:
    """Agrupa os registros por versão do prompt e, dentro dela, por modelo."""
    try:
        text = content.decode("utf-8-sig") if isinstance(content, bytes) else content.lstrip("\ufeff")
    except UnicodeDecodeError as exc:
        raise ResultsCSVError("Salve o CSV com codificação UTF-8.") from exc

    groups = {}
    reader = csv.DictReader(StringIO(text, newline=""), strict=True)
    try:
        columns = reader.fieldnames or []
        missing = {"model", "input", "expected", "response", "correct"} - set(columns)
        if missing:
            raise ResultsCSVError("Colunas obrigatórias ausentes: " + ", ".join(sorted(missing)))
        if len(columns) != len(set(columns)):
            raise ResultsCSVError("Há nomes de coluna repetidos no CSV.")

        for record, row in enumerate(reader, start=1):
            line = reader.line_num
            if None in row or None in row.values():
                raise ResultsCSVError(f"Linha {line}: número de campos diferente do cabeçalho.")
            for name in ("model", "input", "expected"):
                if not row[name].strip():
                    raise ResultsCSVError(f"Linha {line}: o campo '{name}' está vazio.")
            correct = _boolean(row["correct"], "correct", line)
            if correct and not row["response"].strip():
                raise ResultsCSVError(f"Linha {line}: acerto com resposta vazia.")
            verdict = row.get("judge_correct", "").strip()
            case = CaseResult(
                record=record,
                ticket=row["input"],
                expected=row["expected"],
                response=row["response"] if row["response"].strip() else "",
                correct=correct,
                latency_seconds=_metric(row, "latency_seconds", line, float),
                prompt_tokens=_metric(row, "prompt_tokens", line, int),
                completion_tokens=_metric(row, "completion_tokens", line, int),
                total_tokens=_metric(row, "total_tokens", line, int),
                judge_correct=_boolean(verdict, "judge_correct", line) if verdict else None,
                judge_reason=row.get("judge_reason", ""),
            )
            version = row.get("prompt_version", "").strip() or None
            groups.setdefault(version, {}).setdefault(row["model"].strip(), []).append(case)
    except csv.Error as exc:
        raise ResultsCSVError(f"CSV inválido perto da linha {reader.line_num}: {exc}") from exc
    if not groups:
        raise ResultsCSVError("O CSV não contém resultados.")
    return groups


def _complete_total(values: Iterable[int | float | None]) -> int | float | None:
    total = 0
    for value in values:
        if value is None:
            return None
        total += value
    return total


def summarize(cases: Sequence[CaseResult]) -> dict:
    """Todos os registros entram na acurácia. Totais incompletos ficam ausentes."""
    if not cases:
        raise ResultsCSVError("Não há casos para resumir.")
    correct = sum(case.correct for case in cases)
    return {
        "count": len(cases),
        "correct": correct,
        "accuracy": correct / len(cases),
        "latency_seconds": _complete_total(c.latency_seconds for c in cases),
        "total_tokens": _complete_total(c.total_tokens for c in cases),
    }


def read_prompt_regression_csv(content: bytes | str) -> list[PromptRegressionCase]:
    """Lê pares do experimento arquivado de regressão de prompts."""
    try:
        text = content.decode("utf-8-sig") if isinstance(content, bytes) else content.lstrip("\ufeff")
    except UnicodeDecodeError as exc:
        raise ResultsCSVError("Salve o CSV com codificação UTF-8.") from exc

    reader = csv.DictReader(StringIO(text, newline=""), strict=True)
    required = {
        "input",
        "expected",
        "original_response",
        "original_correct",
        "degraded_response",
        "degraded_correct",
    }
    cases: list[PromptRegressionCase] = []
    try:
        columns = reader.fieldnames or []
        missing = required - set(columns)
        if missing:
            raise ResultsCSVError("Colunas obrigatórias ausentes: " + ", ".join(sorted(missing)))
        if len(columns) != len(set(columns)):
            raise ResultsCSVError("Há nomes de coluna repetidos no CSV.")

        for record, row in enumerate(reader, start=1):
            line = reader.line_num
            if None in row or None in row.values():
                raise ResultsCSVError(f"Linha {line}: número de campos diferente do cabeçalho.")
            for name in ("input", "expected"):
                if not row[name].strip():
                    raise ResultsCSVError(f"Linha {line}: o campo '{name}' está vazio.")
            original_correct = _boolean(row["original_correct"], "original_correct", line)
            degraded_correct = _boolean(row["degraded_correct"], "degraded_correct", line)
            if original_correct and not row["original_response"].strip():
                raise ResultsCSVError(f"Linha {line}: veredito original true com resposta vazia.")
            if degraded_correct and not row["degraded_response"].strip():
                raise ResultsCSVError(f"Linha {line}: veredito degradado true com resposta vazia.")
            cases.append(PromptRegressionCase(
                record=record,
                ticket=row["input"].strip(),
                expected=row["expected"].strip(),
                original_response=row["original_response"].strip(),
                original_correct=original_correct,
                degraded_response=row["degraded_response"].strip(),
                degraded_correct=degraded_correct,
            ))
    except csv.Error as exc:
        raise ResultsCSVError(f"CSV inválido perto da linha {reader.line_num}: {exc}") from exc
    if not cases:
        raise ResultsCSVError("O CSV não contém pares de prompts.")
    return cases


def summarize_prompt_regression(
    cases: Sequence[PromptRegressionCase],
) -> dict[str, int | float | Literal["queda", "estabilidade", "melhora"]]:
    if not cases:
        raise ResultsCSVError("Não há pares de prompts para comparar.")
    original_correct = sum(case.original_correct for case in cases)
    degraded_correct = sum(case.degraded_correct for case in cases)
    original_accuracy = original_correct / len(cases)
    degraded_accuracy = degraded_correct / len(cases)
    difference = 100 * (degraded_accuracy - original_accuracy)
    status: Literal["queda", "estabilidade", "melhora"]
    if difference < 0:
        status = "queda"
    elif difference > 0:
        status = "melhora"
    else:
        status = "estabilidade"
    return {
        "count": len(cases),
        "original_correct": original_correct,
        "original_accuracy": original_accuracy,
        "degraded_correct": degraded_correct,
        "degraded_accuracy": degraded_accuracy,
        "difference_points": difference,
        "status": status,
    }
