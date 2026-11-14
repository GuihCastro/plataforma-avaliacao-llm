
import csv
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parent.parent
RESULTS_DIR = PROJECT_DIR / "eval" / "results"


def find_calibrated_files():
    """Localiza todos os arquivos de avaliações calibradas."""

    return sorted(
        RESULTS_DIR.glob("human_review_*_calibrated.csv")
    )


def choose_file(files):
    """Permite selecionar o arquivo que será analisado."""

    if not files:
        print("Nenhum arquivo calibrado encontrado.")
        print("Execute primeiro: python -m eval.rejudge_human_review")
        return None

    print("\nAvaliações calibradas disponíveis:")

    for index, path in enumerate(files, start=1):
        print(f"{index} - {path.name}")

    while True:
        choice = input("\nEscolha o arquivo para analisar: ").strip()

        try:
            selected = int(choice)

            if 1 <= selected <= len(files):
                return files[selected - 1]

        except ValueError:
            pass

        print(f"Digite um número entre 1 e {len(files)}.")


def calculate_kappa(rows):
    total = len(rows)

    if total == 0:
        raise ValueError("Não existem avaliações para calcular o Kappa.")

    agreements = 0
    human_true = 0
    judge_true = 0

    for row in rows:
        human = row["human_correct"].strip().lower() == "true"
        judge = row["judge_correct"].strip().lower() == "true"

        if human == judge:
            agreements += 1

        if human:
            human_true += 1

        if judge:
            judge_true += 1

    observed = agreements / total

    expected = (
        (human_true / total) * (judge_true / total)
        + ((total - human_true) / total)
        * ((total - judge_true) / total)
    )

    if expected == 1:
        kappa = None
    else:
        kappa = (observed - expected) / (1 - expected)

    return observed, kappa, agreements, total


def main():
    files = find_calibrated_files()
    csv_path = choose_file(files)

    if csv_path is None:
        return

    with open(csv_path, encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        rows = list(reader)

    if not rows:
        print("Nenhuma avaliação encontrada.")
        return

    required_fields = {
        "human_correct",
        "judge_correct",
        "model",
        "input",
        "expected",
        "response",
        "judge_reason",
    }

    if not required_fields.issubset(rows[0].keys()):
        print("O arquivo não possui todas as colunas necessárias.")
        return

    if any(
        not row["human_correct"].strip()
        or not row["judge_correct"].strip()
        for row in rows
    ):
        print("Existem avaliações humanas ou do juiz em branco.")
        return

    agreement, kappa, agreements, total = calculate_kappa(rows)

    print("\n--- CALIBRAÇÃO DO LLM JUDGE ---")
    print(f"Arquivo analisado: {csv_path.name}")
    print(f"Total de avaliações: {total}")
    print(f"Concordâncias: {agreements}")
    print(f"Discordâncias: {total - agreements}")
    print(f"Concordância percentual: {agreement * 100:.2f}%")

    if kappa is None:
        print("Kappa de Cohen: indefinido")
    else:
        print(f"Kappa de Cohen: {kappa:.4f}")

    print("\n--- CASOS DE DISCORDÂNCIA ---")

    discordances = []

    for row in rows:
        human = row["human_correct"].strip().lower() == "true"
        judge = row["judge_correct"].strip().lower() == "true"

        if human != judge:
            discordances.append(row)

    if not discordances:
        print("Nenhuma discordância encontrada.")
    else:
        for row in discordances:
            print(f"\nModelo: {row['model']}")
            print(f"Mensagem: {row['input']}")
            print(f"Categoria esperada: {row['expected']}")
            print(f"Resposta: {row['response']}")
            print(f"Avaliação humana: {row['human_correct']}")
            print(f"Avaliação do juiz: {row['judge_correct']}")
            print(f"Motivo do juiz: {row['judge_reason']}")


if __name__ == "__main__":
    main()
