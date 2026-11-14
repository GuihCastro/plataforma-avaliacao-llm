
import csv
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent
RESULTS_PATH = PROJECT_DIR / "eval" / "results" / "results_100_rejudged.csv"
RESULTS_DIR = PROJECT_DIR / "eval" / "results"

SAMPLE_SIZE = 10


def load_source_results():
    if not RESULTS_PATH.exists():
        raise FileNotFoundError(
            "Arquivo results_100_rejudged.csv não encontrado. "
            "Execute primeiro: python -m eval.rejudge_results"
        )

    with open(RESULTS_PATH, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        fieldnames = reader.fieldnames
        rows = list(reader)

    if not rows:
        raise ValueError("O arquivo de resultados está vazio.")

    required = {"model", "input", "expected", "response"}

    if not required.issubset(fieldnames or []):
        raise ValueError("O arquivo de resultados não possui todas as colunas necessárias.")

    return rows, fieldnames


def select_messages(rows, messages_per_model):
    models = list(dict.fromkeys(row["model"] for row in rows))
    all_inputs = list(dict.fromkeys(row["input"] for row in rows))

    results_by_model = {
        model: {
            row["input"]: row
            for row in rows
            if row["model"] == model
        }
        for model in models
    }

    common_inputs = [
        message
        for message in all_inputs
        if all(message in results_by_model[model] for model in models)
    ]

    if not common_inputs:
        raise ValueError("Não existem mensagens comuns entre os modelos.")

    if messages_per_model > len(common_inputs):
        raise ValueError(
            f"Quantidade máxima disponível: {len(common_inputs)} mensagens por modelo."
        )

    if messages_per_model == len(common_inputs):
        selected_inputs = common_inputs
    elif messages_per_model == 1:
        selected_inputs = [common_inputs[0]]
    else:
        indexes = [
            round(i * (len(common_inputs) - 1) / (messages_per_model - 1))
            for i in range(messages_per_model)
        ]
        selected_inputs = [common_inputs[index] for index in indexes]

    selected_rows = []

    for model in models:
        for message in selected_inputs:
            selected_rows.append(results_by_model[model][message].copy())

    return models, selected_rows, len(common_inputs)


def choose_quantity(available):
    print("\nComo deseja realizar a avaliação humana?")
    print(f"1 - Amostra ({SAMPLE_SIZE} mensagens por modelo)")
    print(f"2 - Avaliação completa ({available} mensagens por modelo)")
    print("3 - Escolher quantidade personalizada")

    while True:
        option = input("\nEscolha uma opção (1, 2 ou 3): ").strip()

        if option == "1":
            return min(SAMPLE_SIZE, available)

        if option == "2":
            return available

        if option == "3":
            while True:
                try:
                    quantity = int(
                        input(f"Quantas mensagens por modelo? (1 a {available}): ")
                    )

                    if 1 <= quantity <= available:
                        return quantity

                    print(f"Digite um número entre 1 e {available}.")

                except ValueError:
                    print("Digite um número válido.")

        print("Opção inválida. Escolha 1, 2 ou 3.")


def save_results(rows, fieldnames, output_path):
    with open(output_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def load_or_create_review(rows, fieldnames, output_path):
    if output_path.exists():
        with open(output_path, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            existing_fields = reader.fieldnames
            existing_rows = list(reader)

        expected_pairs = {(row["model"], row["input"]) for row in rows}
        existing_pairs = {(row["model"], row["input"]) for row in existing_rows}

        if len(existing_rows) != len(rows) or existing_pairs != expected_pairs:
            raise ValueError(
                f"O arquivo {output_path.name} já existe, mas contém uma "
                "seleção diferente. Preserve-o e escolha outro nome antes de "
                "iniciar uma nova avaliação."
            )

        print(f"\nAvaliação existente encontrada: {output_path.name}")
        print("As respostas anteriores serão preservadas.")
        return existing_rows, existing_fields

    review_fields = list(fieldnames)

    for column in ("human_correct", "human_reason"):
        if column not in review_fields:
            review_fields.append(column)

    for row in rows:
        row["human_correct"] = ""
        row["human_reason"] = ""

    save_results(rows, review_fields, output_path)

    print(f"\nArquivo criado: {output_path.name}")
    return rows, review_fields


def main():
    source_rows, fieldnames = load_source_results()

    # Descobre quantas mensagens estão disponíveis para todos os modelos.
    models = list(dict.fromkeys(row["model"] for row in source_rows))
    common_count = len(set(row["input"] for row in source_rows))

    quantity = choose_quantity(common_count)

    models, selected_rows, available = select_messages(
        source_rows, quantity
    )

    total = len(selected_rows)
    output_path = RESULTS_DIR / f"human_review_{total}.csv"

    print("\nResumo da avaliação:")
    print(f"Modelos: {len(models)}")
    print(f"Mensagens por modelo: {quantity}")
    print(f"Total de avaliações: {total}")

    rows, review_fields = load_or_create_review(
        selected_rows, fieldnames, output_path
    )

    pending = sum(
        1 for row in rows
        if not row.get("human_correct", "").strip()
    )

    print(f"Avaliações ainda pendentes: {pending}")

    for index, row in enumerate(rows):
        if row.get("human_correct", "").strip():
            continue

        print("\n" + "=" * 60)
        print(f"Avaliação {index + 1}/{len(rows)}")
        print(f"Modelo: {row['model']}")
        print(f"Mensagem: {row['input']}")
        print(f"Categoria esperada: {row['expected']}")
        print(f"Resposta do modelo: {row['response']}")

        while True:
            answer = input(
                "\nA resposta do modelo está correta? (s/n ou q para sair): "
            ).strip().lower()

            if answer in ("s", "n", "q"):
                break

            print("Digite s, n ou q.")

        if answer == "q":
            print("Avaliações salvas. Você pode continuar depois.")
            return

        row["human_correct"] = "true" if answer == "s" else "false"
        row["human_reason"] = input(
            "Justificativa (Enter para pular): "
        ).strip()

        save_results(rows, review_fields, output_path)
        print("Avaliação salva!")

    print("\nTodas as avaliações foram concluídas.")
    print(f"Arquivo atualizado: {output_path}")


if __name__ == "__main__":
    main()
