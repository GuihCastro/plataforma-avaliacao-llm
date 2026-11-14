import csv
from pathlib import Path
from src.llm_judge import LLMJudge

project_dir = Path(__file__).resolve().parent.parent

input_path = project_dir / "eval" / "results" / "results_100_metrics.csv"
output_path = project_dir / "eval" / "results" / "results_100_rejudged.csv"

judge = LLMJudge()

with open(input_path, "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    results = list(reader)

print(f"Total de respostas para reavaliar: {len(results)}")

for index, row in enumerate(results, start=1):
    result = judge.evaluate(
        row["input"],
        row["expected"],
        row["response"]
    )

    row["judge_correct"] = result["correct"]
    row["judge_reason"] = result["reason"]

    if index % 10 == 0:
        print(f"Reavaliadas: {index}/{len(results)}")

with open(output_path, "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=results[0].keys())
    writer.writeheader()
    writer.writerows(results)

print("\nReavaliação concluída!")
print(f"Arquivo salvo em: {output_path}")