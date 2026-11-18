# Relatório de Análise da Calibração do LLM Judge

## 1. Objetivo

Analisar a concordância entre as avaliações humanas e as avaliações realizadas pelo LLM Judge, verificando a consistência do processo de calibração nos três modelos utilizados pelo projeto.

## 2. Base analisada

Foi utilizado o arquivo `eval/results/human_review_30_calibrated.csv`, contendo 30 avaliações calibradas.

Distribuição dos registros:

| Modelo | Avaliações |
|---|---:|
| Qwen 2.5:1.5b | 10 |
| Llama 3.2:3b | 10 |
| Gemma 3:1b | 10 |
| **Total** | **30** |

## 3. Resultados da análise

| Indicador | Resultado |
|---|---:|
| Total de avaliações | 30 |
| Concordâncias | 30 |
| Divergências | 0 |
| Concordância percentual | 100% |
| Cohen's Kappa | 1,00 |

### Concordância por modelo

| Modelo | Concordâncias | Percentual |
|---|---:|---:|
| Qwen 2.5:1.5b | 10/10 | 100% |
| Llama 3.2:3b | 10/10 | 100% |
| Gemma 3:1b | 10/10 | 100% |

## 4. Interpretação

Os resultados demonstram concordância total entre as avaliações humanas e as avaliações realizadas pelo LLM Judge na amostra analisada.

O valor de Cohen's Kappa igual a 1,00 representa concordância perfeita entre os avaliadores, considerando também a concordância esperada ao acaso.

Não foram identificadas divergências nos 30 registros avaliados.

## 5. Limitações

Apesar do resultado positivo, a análise possui limitações:

- A amostra contém apenas 30 avaliações.
- Foram utilizados 10 registros de cada modelo.
- A concordância observada não garante o mesmo desempenho em avaliações futuras.
- É necessário ampliar a amostra para verificar a estabilidade da calibração.

## 6. Conclusão

A análise apresentou resultados positivos para a calibração do LLM Judge, com 100% de concordância em relação às avaliações humanas e Cohen's Kappa de 1,00.

Os resultados fornecem evidências de consistência do Judge na amostra analisada, mas devem ser interpretados considerando o tamanho limitado da base.

A ampliação da amostra e a realização de novas avaliações humanas poderão contribuir para uma validação mais abrangente.

---

**Responsável pela análise:** Dados e Qualidade  
**Arquivo analisado:** `eval/results/human_review_30_calibrated.csv`
