# Reavaliação das avaliações humanas

## Objetivo

O script `eval/rejudge_human_review.py` foi desenvolvido para reavaliar os registros presentes em `human_review.csv`, utilizando a versão híbrida do LLM Judge.

A finalidade é atualizar as avaliações do Judge e preservar os resultados anteriores, permitindo comparar as duas versões.

## Funcionamento

O script executa as seguintes etapas:

1. Lê os registros do arquivo `eval/results/human_review.csv`.
2. Verifica se existem avaliações para processar.
3. Preserva os valores anteriores de `judge_correct` e `judge_reason` nas colunas `judge_correct_previous` e `judge_reason_previous`.
4. Envia a mensagem original, a categoria esperada e a resposta do modelo para o método `evaluate()` da classe `LLMJudge`.
5. Registra o novo resultado e a justificativa retornada.
6. Identifica a versão utilizada na coluna `judge_version`, com o valor `hybrid_qwen2.5:3b`.
7. Salva os registros atualizados em um novo arquivo CSV.

## Arquivos utilizados

| Arquivo | Função |
|---|---|
| `eval/results/human_review.csv` | Arquivo de entrada, com as avaliações anteriores |
| `eval/results/human_review_calibrated.csv` | Arquivo de saída, com as novas avaliações |
| `src/llm_judge.py` | Implementação do LLM Judge utilizado |

O arquivo original é preservado, evitando a perda dos resultados anteriores.

## Como executar

Na pasta raiz do projeto, execute:

```bash
python eval/rejudge_human_review.py
```

Ao finalizar, o programa informa a quantidade de registros processados e o caminho do arquivo gerado.

## Resultado

A reavaliação produz um novo CSV que mantém os resultados anteriores e registra as novas avaliações do Judge. Esse arquivo pode ser utilizado posteriormente na etapa de calibração, para comparar as avaliações automáticas com as avaliações humanas.

A separação entre os arquivos permite manter o histórico e analisar as mudanças nas avaliações sem modificar os dados originais.