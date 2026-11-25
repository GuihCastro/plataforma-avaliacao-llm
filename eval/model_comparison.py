import argparse
import csv
import hashlib
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from src.llm_judge import LLMJudge
from src.ollama_client import OllamaClient


PROJECT_DIR = Path(__file__).resolve().parent.parent
DATASET_PATH = PROJECT_DIR / "eval" / "datasets" / "test_cases.csv"
MODELS = ("qwen2.5:1.5b", "llama3.2:3b", "gemma3:1b")
JUDGE_MODEL = "qwen2.5:3b"
CSV_FIELDS = [
    "model",
    "input",
    "expected",
    "response",
    "correct",
    "latency_seconds",
    "prompt_tokens",
    "completion_tokens",
    "total_tokens",
    "ollama_duration_seconds",
    "judge_correct",
    "judge_reason",
    "model_error",
    "judge_calls",
    "judge_prompt_tokens",
    "judge_completion_tokens",
    "judge_total_tokens",
    "judge_ollama_duration_seconds",
    "judge_error",
]

CLASSIFIER_PROMPT_PREFIX = (
    "Classifique a mensagem de suporte de TI em exatamente uma destas categorias: "
    "Hardware, Software, Rede, Acesso, Instalação ou Configuração. "
    "Responda somente com o nome da categoria, sem explicações. "
)


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _read_examples(dataset_path: Path) -> tuple[list[tuple[str, str]], str]:
    dataset_bytes = dataset_path.read_bytes()
    reader = csv.DictReader(dataset_bytes.decode("utf-8").splitlines())
    examples = [(row["input"], row["expected"]) for row in reader]
    if len(examples) != 100:
        raise ValueError(f"Esperados 100 casos, encontrados {len(examples)}")
    return examples, hashlib.sha256(dataset_bytes).hexdigest()


def _model_name(model: dict) -> Optional[str]:
    name = model.get("name") or model.get("model")
    return name if isinstance(name, str) else None


def _check_model_availability(
    client: OllamaClient,
) -> dict[str, dict]:
    try:
        installed_models = client.list_models()
    except Exception as exc:
        raise RuntimeError(
            f"Não foi possível consultar os modelos no Ollama "
            f"({client.base_url}): {exc}"
        ) from exc

    identified_models = {
        name: model
        for model in installed_models
        if (name := _model_name(model)) is not None
    }
    required = (*MODELS, JUDGE_MODEL)
    missing = [model for model in required if model not in identified_models]
    if missing:
        raise RuntimeError(
            "Modelos necessários indisponíveis no Ollama "
            f"({client.base_url}): {', '.join(missing)}. "
            "Nenhuma inferência foi iniciada."
        )
    return {model: identified_models[model] for model in required}


def _write_metadata(metadata_path: Path, metadata: dict) -> None:
    metadata["updated_at_utc"] = _utc_now()
    with metadata_path.open("w", encoding="utf-8") as file:
        json.dump(metadata, file, ensure_ascii=False, indent=2)
        file.write("\n")


def _sum_measurements(calls: list[dict], field: str):
    if not calls:
        return None
    values = [
        (call.get("metrics") or {}).get(field)
        for call in calls
    ]
    if any(value is None for value in values):
        return None
    return sum(values)


def _csv_measurement(value):
    return "" if value is None else value


def _format_seconds(nanoseconds):
    if nanoseconds is None:
        return ""
    return round(nanoseconds / 1_000_000_000, 4)


def run_evaluation(
    output_path: Path,
    dataset_path: Path = DATASET_PATH,
) -> tuple[Path, Path]:
    output_path = Path(output_path).resolve()
    metadata_path = Path(f"{output_path}.metadata.json")
    if output_path.exists():
        raise FileExistsError(f"O arquivo de saída já existe: {output_path}")
    if metadata_path.exists():
        raise FileExistsError(f"O arquivo de metadados já existe: {metadata_path}")
    if not output_path.parent.is_dir():
        raise FileNotFoundError(
            f"A pasta de saída não existe: {output_path.parent}"
        )

    examples, dataset_hash = _read_examples(Path(dataset_path))
    run_started_at = _utc_now()

    judge = LLMJudge()
    client = judge.client
    identified_models = _check_model_availability(client)

    metadata = {
        "status": "in_progress",
        "started_at_utc": run_started_at,
        "finished_at_utc": None,
        "updated_at_utc": run_started_at,
        "ollama_base_url": client.base_url,
        "dataset": {
            "path": str(Path(dataset_path).resolve()),
            "sha256": dataset_hash,
            "case_count": len(examples),
        },
        "models": {
            "classifiers": list(MODELS),
            "judge": JUDGE_MODEL,
            "identified": identified_models,
        },
        "requests": {
            "classifier": {
                "payload_fields": ["model", "prompt", "stream"],
                "stream": False,
                "timeout_seconds": 120,
                "sampling_options_sent": False,
            },
            "judge": {
                "payload_fields": ["model", "prompt", "stream"],
                "stream": False,
                "timeout_seconds": 120,
                "sampling_options_sent": False,
            },
        },
        "prompts": {
            "classifier_template_prefix": CLASSIFIER_PROMPT_PREFIX,
            "classifier_template_suffix": "",
            "classifier_calls": [],
            "judge_calls": [],
        },
        "metrics": {
            "classifier_generation": (
                "latency_seconds, prompt_tokens, completion_tokens, "
                "total_tokens, ollama_duration_seconds"
            ),
            "additional_judge_calls": (
                "judge_* metrics include only requests made by LLMJudge; "
                "exact matches resolved by Python produce no judge request"
            ),
        },
        "completed_cases": 0,
        "current_model": None,
        "current_case": None,
    }

    output_created = False
    metadata_created = False
    try:
        with output_path.open("x", newline="", encoding="utf-8") as csv_file:
            output_created = True
            writer = csv.DictWriter(csv_file, fieldnames=CSV_FIELDS)
            writer.writeheader()
            csv_file.flush()

            try:
                with metadata_path.open("x", encoding="utf-8") as metadata_file:
                    metadata_created = True
                    json.dump(metadata, metadata_file, ensure_ascii=False, indent=2)
                    metadata_file.write("\n")
                judge_generate_with_metrics = client.generate_with_metrics

                for model in MODELS:
                    print(f"\n--- Avaliando modelo: {model} ---", flush=True)
                    model_total_time = 0.0
                    model_correct = 0

                    for case_index, (prompt, expected) in enumerate(examples, 1):
                        print(
                            f"[{model}] Caso {case_index}/{len(examples)}",
                            flush=True,
                        )
                        metadata["current_model"] = model
                        metadata["current_case"] = case_index
                        instruction_prompt = CLASSIFIER_PROMPT_PREFIX + prompt
                        classifier_call = {
                            "model": model,
                            "prompt": instruction_prompt,
                            "stream": False,
                            "status": "in_progress",
                            "metrics": None,
                            "error": None,
                        }
                        metadata["prompts"]["classifier_calls"].append(
                            classifier_call
                        )
                        _write_metadata(metadata_path, metadata)

                        started = time.perf_counter()
                        response = ""
                        model_error = None
                        classifier_metrics = None
                        try:
                            generated = client.generate_with_metrics(
                                model,
                                instruction_prompt,
                            )
                            if generated is None:
                                model_error = (
                                    getattr(client, "last_error", None)
                                    or "Modelo não retornou resposta."
                                )
                            else:
                                classifier_metrics = generated
                                generated_response = generated.get("response")
                                if not isinstance(generated_response, str):
                                    model_error = (
                                        "Resposta do modelo não é uma string."
                                    )
                                else:
                                    response = generated_response.strip()
                                    if not response:
                                        model_error = (
                                            "Modelo retornou resposta vazia."
                                        )
                        except Exception as exc:
                            model_error = str(exc)
                        latency = time.perf_counter() - started
                        model_total_time += latency
                        classifier_call["status"] = (
                            "failed" if model_error else "completed"
                        )
                        classifier_call["error"] = model_error
                        classifier_call["metrics"] = classifier_metrics

                        normalized_response = response.strip().lower().strip(
                            ".,!?;:"
                        )
                        normalized_expected = expected.lower()
                        is_correct = (
                            model_error is None
                            and normalized_response == normalized_expected
                        )
                        model_correct += int(is_correct)

                        judge_calls_start = len(metadata["prompts"]["judge_calls"])
                        judge_evaluation_error = None

                        def capture_judge_request(
                            judge_model: str,
                            judge_prompt: str,
                        ):
                            call = {
                                "model": judge_model,
                                "prompt": judge_prompt,
                                "stream": False,
                                "status": "in_progress",
                                "metrics": None,
                                "error": None,
                            }
                            metadata["prompts"]["judge_calls"].append(call)
                            _write_metadata(metadata_path, metadata)
                            try:
                                result = judge_generate_with_metrics(
                                    judge_model,
                                    judge_prompt,
                                )
                            except Exception as exc:
                                call["status"] = "failed"
                                call["error"] = str(exc)
                                _write_metadata(metadata_path, metadata)
                                raise
                            if result is None:
                                call["status"] = "failed"
                                call["error"] = (
                                    getattr(client, "last_error", None)
                                    or "Juiz não retornou resposta."
                                )
                            else:
                                call["status"] = "completed"
                                call["metrics"] = result
                            _write_metadata(metadata_path, metadata)
                            return result

                        client.generate_with_metrics = capture_judge_request
                        try:
                            if model_error is None:
                                try:
                                    judge_result = judge.evaluate(
                                        prompt,
                                        expected,
                                        response,
                                    )
                                except Exception as exc:
                                    judge_evaluation_error = (
                                        f"Erro ao avaliar: {exc}"
                                    )
                                    judge_result = {
                                        "correct": False,
                                        "reason": judge_evaluation_error,
                                    }
                                else:
                                    judge_evaluation_error = getattr(
                                        judge,
                                        "evaluation_error",
                                        None,
                                    )
                            else:
                                judge_result = {
                                    "correct": False,
                                    "reason": (
                                        "Modelo não pôde ser avaliado: "
                                        f"{model_error}"
                                    ),
                                }
                        finally:
                            client.generate_with_metrics = (
                                judge_generate_with_metrics
                            )

                        case_judge_calls = metadata["prompts"]["judge_calls"][
                            judge_calls_start:
                        ]
                        judge_errors = [
                            call["error"]
                            for call in case_judge_calls
                            if call["error"]
                        ]
                        if judge_evaluation_error:
                            judge_errors.append(judge_evaluation_error)
                            for call in case_judge_calls:
                                call["evaluation_error"] = (
                                    judge_evaluation_error
                                )
                        prompt_tokens = (
                            classifier_metrics.get("prompt_tokens")
                            if classifier_metrics
                            else ""
                        )
                        completion_tokens = (
                            classifier_metrics.get("completion_tokens")
                            if classifier_metrics
                            else ""
                        )
                        total_tokens = (
                            classifier_metrics.get("total_tokens")
                            if classifier_metrics
                            else ""
                        )
                        duration_ns = (
                            classifier_metrics.get("total_duration_ns")
                            if classifier_metrics
                            else None
                        )
                        writer.writerow({
                            "model": model,
                            "input": prompt,
                            "expected": expected,
                            "response": response,
                            "correct": str(is_correct),
                            "latency_seconds": round(latency, 4),
                            "prompt_tokens": _csv_measurement(prompt_tokens),
                            "completion_tokens": _csv_measurement(
                                completion_tokens
                            ),
                            "total_tokens": _csv_measurement(total_tokens),
                            "ollama_duration_seconds": _format_seconds(
                                duration_ns
                            ),
                            "judge_correct": (
                                ""
                                if model_error or judge_evaluation_error
                                else str(judge_result["correct"])
                            ),
                            "judge_reason": judge_result["reason"],
                            "model_error": model_error or "",
                            "judge_calls": len(case_judge_calls),
                            "judge_prompt_tokens": _csv_measurement(
                                _sum_measurements(
                                    case_judge_calls, "prompt_tokens"
                                )
                            ),
                            "judge_completion_tokens": _csv_measurement(
                                _sum_measurements(
                                    case_judge_calls, "completion_tokens"
                                )
                            ),
                            "judge_total_tokens": _csv_measurement(
                                _sum_measurements(
                                    case_judge_calls, "total_tokens"
                                )
                            ),
                            "judge_ollama_duration_seconds": _format_seconds(
                                _sum_measurements(
                                    case_judge_calls, "total_duration_ns"
                                )
                            ),
                            "judge_error": "; ".join(judge_errors),
                        })
                        csv_file.flush()
                        metadata["completed_cases"] += 1
                        _write_metadata(metadata_path, metadata)

                    print(
                        f"[{model}] Concluído: {model_correct}/"
                        f"{len(examples)} acertos; "
                        f"{model_total_time:.2f} s de geração.",
                        flush=True,
                    )

                metadata["status"] = "completed"
            except KeyboardInterrupt:
                metadata["status"] = "interrupted"
                raise
            except Exception:
                metadata["status"] = "failed"
                raise
            finally:
                if metadata_created:
                    metadata["finished_at_utc"] = _utc_now()
                    if metadata["status"] == "completed":
                        metadata["current_model"] = None
                        metadata["current_case"] = None
                    _write_metadata(metadata_path, metadata)
    except FileExistsError:
        if output_created and not metadata_created and output_path.exists():
            output_path.unlink()
        raise
    except Exception:
        if output_created and not metadata_created and output_path.exists():
            output_path.unlink()
        raise

    print(f"\nCSV salvo em: {output_path}", flush=True)
    print(f"Metadados salvos em: {metadata_path}", flush=True)
    return output_path, metadata_path


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Compara os modelos definidos com 100 casos de avaliação."
    )
    parser.add_argument(
        "--output",
        required=True,
        type=Path,
        help="Caminho para um novo arquivo CSV de resultados.",
    )
    args = parser.parse_args(argv)
    try:
        run_evaluation(args.output)
    except (FileExistsError, FileNotFoundError, RuntimeError, ValueError, OSError) as exc:
        print(f"Erro: {exc}", file=sys.stderr, flush=True)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
