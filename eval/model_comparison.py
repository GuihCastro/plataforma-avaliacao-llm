
from src.ollama_client import OllamaClient
from src.llm_judge import LLMJudge
import time
import csv
from pathlib import Path


project_dir = Path(__file__).resolve().parent.parent
test_cases_path = project_dir / "eval" / "datasets" / "test_cases.csv"

with open(test_cases_path, "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    examples = [
        (row["input"], row["expected"])
        for row in reader
    ]

if len(examples) != 100:
    raise ValueError(f"Esperados 100 casos, encontrados {len(examples)}")

models = ["qwen2.5:1.5b", "llama3.2:3b", "gemma3:1b"]

results = {}
individual_results = []

judge = LLMJudge()

for model in models:
    client = OllamaClient()

    correct = 0
    errors = 0
    total_time = 0
    total_prompt_tokens = 0
    total_completion_tokens = 0
    total_tokens = 0

    print(f"\n--- Avaliando modelo: {model} ---")

    for prompt, expected in examples:
        start_time = time.time()

        response = ""
        model_error = None

        metrics = {
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "total_tokens": 0,
            "total_duration_ns": 0
        }

        instruction_prompt = (
            "Classifique a mensagem de suporte de TI em exatamente uma destas categorias: "
            "Hardware, Software, Rede, Acesso, Instalação ou Configuração. "
            "Responda somente com o nome da categoria, sem explicações. "
            f"{prompt}"
        )

        try:
            generated = client.generate_with_metrics(
                model,
                instruction_prompt
            )

            if generated is None:
                model_error = "Modelo não retornou resposta."
            else:
                response = generated["response"].strip()
                metrics = generated

        except Exception as e:
            model_error = str(e)

        latency = time.time() - start_time
        total_time += latency

        total_prompt_tokens += metrics["prompt_tokens"]
        total_completion_tokens += metrics["completion_tokens"]
        total_tokens += metrics["total_tokens"]

        normalized_response = (
            response.strip().lower().strip(".,!?;:")
        )
        normalized_expected = expected.lower()

        is_correct = (
            model_error is None
            and normalized_response == normalized_expected
        )

        if is_correct:
            correct += 1
        else:
            errors += 1

        if model_error is None:
            judge_result = judge.evaluate(
                prompt,
                expected,
                response
            )
        else:
            judge_result = {
                "correct": False,
                "reason": f"Modelo não pôde ser avaliado: {model_error}"
            }

        individual_results.append({
            "model": model,
            "input": prompt,
            "expected": expected,
            "response": response,
            "correct": is_correct,
            "latency_seconds": round(latency, 4),
            "prompt_tokens": metrics["prompt_tokens"],
            "completion_tokens": metrics["completion_tokens"],
            "total_tokens": metrics["total_tokens"],
            "ollama_duration_seconds": round(
                metrics["total_duration_ns"] / 1_000_000_000,
                4
            ),
            "judge_correct": judge_result["correct"],
            "judge_reason": judge_result["reason"]
        })

    avg_time = total_time / len(examples)

    results[model] = {
        "correct": correct,
        "errors": errors,
        "avg_time": avg_time,
        "total_time": total_time,
        "prompt_tokens": total_prompt_tokens,
        "completion_tokens": total_completion_tokens,
        "total_tokens": total_tokens
    }


print("\n--- Resultados Finais ---")

for model, data in results.items():
    print(f"\nModelo: {model}")
    print(f"Acertos: {data['correct']}")
    print(f"Erros: {data['errors']}")
    print(f"Tempo total: {data['total_time']:.2f} segundos")
    print(f"Tempo médio por caso: {data['avg_time']:.4f} segundos")
    print(f"Tokens de entrada: {data['prompt_tokens']}")
    print(f"Tokens de saída: {data['completion_tokens']}")
    print(f"Tokens totais: {data['total_tokens']}")


file_path = (
    project_dir
    / "eval"
    / "results"
    / "results_100_metrics.csv"
)

fieldnames = [
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
    "judge_reason"
]

with open(file_path, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(individual_results)

print(f"\nTotal de registros: {len(individual_results)}")
print(f"CSV salvo em: {file_path.resolve()}")
