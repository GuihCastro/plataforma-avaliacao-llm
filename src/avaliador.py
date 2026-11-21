import csv
import os
from ollama_client import gerar_classificacao

CHAMADOS_EXEMPLO = [
    {"input": "Minha internet caiu e a luz vermelha está piscando no modem.", "expected": "Suporte Técnico"},
    {"input": "Cobraram duas vezes a fatura do meu cartão neste mês.", "expected": "Financeiro"},
    {"input": "Quero cancelar minha assinatura antes da renovação.", "expected": "Cancelamento"},
]


def executar_avaliacao(modelo: str = "llama3.2:1b", prompt_version: str = "v1"):
    resultados = []

    for item in CHAMADOS_EXEMPLO:
        prompt_completo = (
            "Classifique o chamado de suporte abaixo em APENAS UMA das categorias: "
            "Suporte Técnico, Financeiro ou Cancelamento.\n\n"
            f"Chamado: {item['input']}\nCategoria:"
        )

        saida = gerar_classificacao(modelo=modelo, prompt=prompt_completo)
        resposta_limpa = saida["response"]
        acertou = item["expected"].lower() in resposta_limpa.lower()

        resultados.append({
            "model": modelo,
            "input": item["input"],
            "expected": item["expected"],
            "response": resposta_limpa,
            "correct": str(acertou).lower(),
            "prompt_version": prompt_version,
            "latency_seconds": saida["latency_seconds"],
            "tokens": saida["tokens"],
        })

    os.makedirs("eval/results", exist_ok=True)
    caminho_csv = "eval/results/resultados_backend.csv"

    colunas = ["model", "input", "expected", "response", "correct", "prompt_version", "latency_seconds", "tokens"]
    with open(caminho_csv, mode="w", encoding="utf-8", newline="") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=colunas)
        escritor.writeheader()
        escritor.writerows(resultados)

    print(f"Avaliação concluída! Arquivo salvo em: {caminho_csv}")


if __name__ == "__main__":
    executar_avaliacao(modelo="llama3.2:1b", prompt_version="v1")
