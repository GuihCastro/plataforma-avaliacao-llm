
import csv
import random
from pathlib import Path

from src.ollama_client import OllamaClient


MODEL_NAME = "qwen2.5:1.5b"
SAMPLE_SIZE = 20

project_dir = Path(__file__).resolve().parent.parent
TEST_CASES_FILE = project_dir / "eval" / "datasets" / "test_cases.csv"
RESULTS_FILE = project_dir / "eval" / "results" / "regression_results_prompt_comparison.csv"


ORIGINAL_PROMPT = (
    "Classifique a mensagem de suporte de TI em exatamente uma destas categorias: "
    "Hardware, Software, Rede, Acesso, Instalação ou Configuração. "
    "Responda somente com o nome da categoria, sem explicações."
)

DEGRADED_PROMPT = (
    "Classifique a mensagem de suporte de TI. "
    "Independentemente do conteúdo da mensagem, responda sempre Hardware."
)


def normalize_response(response):
    return response.strip().lower().rstrip(".,!?;:")


def evaluate_case(client, input_text, expected, prompt):
    full_prompt = f"{prompt}\n\nMensagem: {input_text}"

    response = client.generate(MODEL_NAME, full_prompt)

    if response is None:
        response = ""

    is_correct = (
        normalize_response(response)
        == normalize_response(expected)
    )

    return response.strip(), is_correct


def main():
    # Carregar os casos de teste
    with open(TEST_CASES_FILE, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        examples = list(reader)

    if len(examples) < SAMPLE_SIZE:
        raise ValueError(
            f"São necessários pelo menos {SAMPLE_SIZE} casos. "
            f"Foram encontrados {len(examples)}."
        )

    # Selecionar os mesmos 20 casos nas duas avaliações
    sampled_examples = random.Random(42).sample(examples, SAMPLE_SIZE)

    client = OllamaClient()

    results = []

    print(f"Modelo utilizado: {MODEL_NAME}")
    print(f"Casos avaliados: {SAMPLE_SIZE}")

    for index, example in enumerate(sampled_examples, start=1):
        input_text = example["input"]
        expected = example["expected"]

        # Avaliação com prompt original
        original_response, original_correct = evaluate_case(
            client, input_text, expected, ORIGINAL_PROMPT
        )

        # Avaliação com prompt degradado
        degraded_response, degraded_correct = evaluate_case(
            client, input_text, expected, DEGRADED_PROMPT
        )

        results.append({
            "input": input_text,
            "expected": expected,
            "original_response": original_response,
            "original_correct": original_correct,
            "degraded_response": degraded_response,
            "degraded_correct": degraded_correct
        })

        print(f"Progresso: {index}/{SAMPLE_SIZE}")

    # Calcular acurácia
    original_correct_count = sum(
        row["original_correct"] for row in results
    )

    degraded_correct_count = sum(
        row["degraded_correct"] for row in results
    )

    original_accuracy = original_correct_count / SAMPLE_SIZE
    degraded_accuracy = degraded_correct_count / SAMPLE_SIZE

    # Salvar resultados
    fieldnames = [
        "input",
        "expected",
        "original_response",
        "original_correct",
        "degraded_response",
        "degraded_correct"
    ]

    with open(RESULTS_FILE, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    # Exibir métricas
    print("\n--- Resultados do Teste de Regressão ---")
    print(f"Acurácia original: {original_accuracy:.2%}")
    print(f"Acurácia degradada: {degraded_accuracy:.2%}")
    print(f"Queda de desempenho: {(original_accuracy - degraded_accuracy):.2%}")
    print(f"Resultados salvos em: {RESULTS_FILE}")


if __name__ == "__main__":
    main()
