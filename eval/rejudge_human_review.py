
import csv
from pathlib import Path

from src.llm_judge import LLMJudge


PROJECT_DIR = Path(__file__).resolve().parent.parent
RESULTS_DIR = PROJECT_DIR / "eval" / "results"


def find_review_files():
    """Localiza avaliações humanas, ignorando arquivos já calibrados."""

    return sorted(
        path
        for path in RESULTS_DIR.glob("human_review_*.csv")
        if not path.stem.endswith("_calibrated")
    )


def choose_review_file(files):
    """Permite selecionar qual avaliação humana será reavaliada."""

    if not files:
        print("Nenhum arquivo de avaliação humana encontrado.")
        print("Execute primeiro: python -m eval.human_review")
        return None

    print("\nAvaliações humanas disponíveis:")

    for index, path in enumerate(files, start=1):
        print(f"{index} - {path.name}")

    while True:
        choice = input("\nEscolha o arquivo que deseja reavaliar: ").strip()

        try:
            selected = int(choice)

            if 1 <= selected <= len(files):
                return files[selected - 1]

        except ValueError:
            pass

        print(f"Digite um número entre 1 e {len(files)}.")


def main():
    review_files = find_review_files()
    input_path = choose_review_file(review_files)

    if input_path is None:
        return

    output_path = input_path.with_name(
        f"{input_path.stem}_calibrated.csv"
    )

    if output_path.exists():
        answer = input(
            f"\nO arquivo {output_path.name} já existe. "
            "Deseja substituí-lo? (s/n): "
        ).strip().lower()

        if answer != "s":
            print("Operação cancelada. Nenhum arquivo foi alterado.")
            return

    with open(input_path, "r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        rows = list(reader)
        original_fields = reader.fieldnames or []

    if not rows:
        print("Nenhuma avaliação encontrada.")
        return

    required_fields = {"model", "input", "expected", "response"}
    missing_fields = required_fields - set(original_fields)

    if missing_fields:
        print(f"Colunas obrigatórias ausentes: {', '.join(sorted(missing_fields))}")
        return

    fieldnames = [
        field
        for field in original_fields
        if field not in (
            "judge_correct",
            "judge_reason",
            "judge_correct_previous",
            "judge_reason_previous",
            "judge_version",
        )
    ]

    fieldnames += [
        "judge_correct_previous",
        "judge_reason_previous",
        "judge_correct",
        "judge_reason",
        "judge_version",
    ]

    judge = LLMJudge()

    for index, row in enumerate(rows, start=1):
        print(
            f"\nReavaliando {index}/{len(rows)}: "
            f"{row['model']}"
        )

        # Preserva a avaliação anterior do juiz.
        row["judge_correct_previous"] = row.get("judge_correct", "")
        row["judge_reason_previous"] = row.get("judge_reason", "")

        result = judge.evaluate(
            row["input"],
            row["expected"],
            row["response"],
        )

        row["judge_correct"] = str(result["correct"]).lower()
        row["judge_reason"] = result["reason"]
        row["judge_version"] = "hybrid_qwen2.5:3b"

    with open(output_path, "w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print("\nReavaliação concluída!")
    print(f"Total de registros: {len(rows)}")
    print(f"Arquivo original preservado: {input_path.name}")
    print(f"Novo arquivo: {output_path.name}")


if __name__ == "__main__":
    main()
