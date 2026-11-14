# Métricas de Desempenho e Consumo dos Modelos

## 1. Objetivo

Esta etapa tem como objetivo medir o desempenho dos três modelos de linguagem utilizados na plataforma, considerando a quantidade de acertos, o tempo de execução e o consumo de tokens.

Foram utilizados os mesmos 100 casos de teste do conjunto `eval/datasets/test_cases.csv`, totalizando 300 avaliações.

## 2. Modelos avaliados

- Qwen 2.5 1.5B
- Llama 3.2 3B
- Gemma 3 1B

## 3. Resultados

| Modelo | Acertos | Erros | Precisão |
|---|---:|---:|---:|
| Qwen 2.5 1.5B | 49 | 51 | 49% |
| Llama 3.2 3B | 22 | 78 | 22% |
| Gemma 3 1B | 37 | 63 | 37% |

## 4. Tempo de execução

| Modelo | Tempo total | Tempo médio por caso |
|---|---:|---:|
| Qwen 2.5 1.5B | 207,82 s | 2,0782 s |
| Llama 3.2 3B | 210,40 s | 2,1040 s |
| Gemma 3 1B | 208,85 s | 2,0885 s |

O tempo total somado das três avaliações foi de aproximadamente 627,07 segundos, equivalente a 10 minutos e 27 segundos.

## 5. Consumo de tokens

| Modelo | Tokens de entrada | Tokens de saída | Total |
|---|---:|---:|---:|
| Qwen 2.5 1.5B | 9.325 | 326 | 9.651 |
| Llama 3.2 3B | 8.928 | 376 | 9.304 |
| Gemma 3 1B | 6.439 | 307 | 6.746 |
| **Total** | **24.692** | **1.009** | **25.701** |

Os valores foram obtidos diretamente das métricas retornadas pela API local do Ollama, considerando os tokens de entrada (`prompt_eval_count`) e de saída (`eval_count`).

## 6. Análise dos resultados

O Qwen 2.5 1.5B apresentou a maior precisão, com 49 acertos em 100 casos. O Gemma 3 1B obteve 37% de precisão, enquanto o Llama 3.2 3B apresentou 22%.

Em relação ao consumo, o Gemma 3 1B apresentou o menor total de tokens, com 6.746. O Qwen 2.5 1.5B consumiu 9.651 tokens e o Llama 3.2 3B consumiu 9.304.

Os tempos de execução foram próximos entre os três modelos, ficando em torno de 208 a 210 segundos para cada bateria de 100 casos.

Os resultados indicam que o modelo com maior número de parâmetros não necessariamente apresenta a melhor precisão na tarefa avaliada. Nesta execução, o Qwen 2.5 1.5B apresentou o melhor resultado de classificação.

## 7. Limitações

Os resultados representam uma execução específica e podem apresentar pequenas variações em novas execuções.

A precisão foi calculada comparando a resposta gerada com a categoria esperada, após normalização textual. Portanto, respostas semanticamente corretas, mas diferentes do nome exato da categoria, podem ser contabilizadas como incorretas.

O consumo de tokens e os tempos apresentados correspondem às chamadas de geração dos três modelos avaliados. O consumo do LLM Judge não está incluído nesses totais.

## 8. Reprodutibilidade

Para executar novamente a comparação, com o Ollama em funcionamento e os modelos instalados, utilizar:

```bash
python -m eval.model_comparison
```

O arquivo gerado é:

`eval/results/results_100_metrics.csv`

Ele contém os resultados individuais, tempos, tokens e informações da avaliação pelo LLM Judge.