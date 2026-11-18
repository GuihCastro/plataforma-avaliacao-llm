# Análise dos Erros de Classificação dos Modelos

## 1. Objetivo

Analisar os erros de classificação dos três modelos utilizados no projeto, identificando categorias com maior incidência de erros, confusões entre categorias e diferenças de comportamento entre os modelos.

## 2. Base analisada

Foi utilizado o arquivo `eval/results/results_100_metrics.csv`, contendo 300 registros.

Cada modelo possui 100 casos de teste:

- Qwen 2.5:1.5b
- Llama 3.2:3b
- Gemma 3:1b

## 3. Desempenho geral

| Modelo | Acertos | Erros | Acurácia | Taxa de erro |
|---|---:|---:|---:|---:|
| Qwen 2.5:1.5b | 46 | 54 | 46% | 54% |
| Llama 3.2:3b | 24 | 76 | 24% | 76% |
| Gemma 3:1b | 32 | 68 | 32% | 68% |
| **Total** | **102** | **198** | **34%** | **66%** |

O Qwen apresentou o melhor resultado geral, enquanto o Llama apresentou a maior quantidade de erros.

## 4. Erros por categoria esperada

| Categoria | Quantidade de erros |
|---|---:|
| Software | 46 |
| Hardware | 42 |
| Instalação | 39 |
| Configuração | 29 |
| Rede | 27 |
| Acesso | 15 |
| **Total** | **198** |

Software, Hardware e Instalação concentraram a maior quantidade de erros.

## 5. Respostas incorretas mais frequentes

Após a normalização da pontuação final, foram identificadas as seguintes respostas incorretas:

| Resposta | Ocorrências |
|---|---:|
| Acesso | 81 |
| Rede | 48 |
| Configuração | 24 |
| Instalação | 17 |
| Software | 13 |
| Hardware | 9 |

A categoria Acesso foi a resposta incorreta mais frequente.

## 6. Principais confusões entre categorias

| Categoria esperada | Resposta do modelo | Ocorrências |
|---|---|---:|
| Rede | Acesso | 20 |
| Hardware | Acesso | 19 |
| Software | Acesso | 16 |
| Software | Rede | 15 |
| Configuração | Acesso | 15 |
| Hardware | Rede | 13 |
| Instalação | Acesso | 11 |
| Instalação | Configuração | 10 |

Os resultados mostram que os modelos apresentam dificuldades recorrentes para diferenciar determinadas categorias, principalmente Acesso, Rede, Hardware e Software.

## 7. Padrões de erro por modelo

### Llama 3.2:3b

- 76 erros em 100 casos.
- Principal resposta incorreta: Acesso.
- 48 ocorrências de respostas classificadas como Acesso.

### Gemma 3:1b

- 68 erros em 100 casos.
- Principal resposta incorreta: Rede.
- 40 ocorrências de respostas classificadas como Rede.

### Qwen 2.5:1.5b

- 54 erros em 100 casos.
- Apresentou erros distribuídos entre diferentes categorias.
- Obteve a melhor acurácia entre os três modelos.

## 8. Recomendações de melhoria

Com base nos padrões encontrados, recomenda-se:

- Revisar os exemplos utilizados para diferenciar Acesso e Rede.
- Reforçar as diferenças entre Hardware e Software.
- Melhorar os exemplos de Instalação e Configuração.
- Avaliar ajustes nos prompts de classificação.
- Realizar novas avaliações após possíveis melhorias.

## 9. Limitações

Esta análise utiliza os resultados registrados no arquivo de métricas do projeto.

Os erros foram identificados a partir da comparação entre a categoria esperada e o campo `correct`. Não foi realizada uma nova validação humana individual dos 300 registros.

As recomendações são hipóteses de melhoria baseadas nos padrões observados e precisam ser testadas em avaliações futuras.

## 10. Conclusão

A análise identificou 198 erros nos 300 resultados avaliados, correspondendo a uma taxa de erro de 66%.

O Qwen 2.5:1.5b apresentou a melhor acurácia, com 46%, enquanto o Llama 3.2:3b apresentou a maior taxa de erro, com 76%.

Também foram identificadas confusões recorrentes entre categorias, especialmente envolvendo Acesso e Rede.

Esses resultados podem orientar futuras melhorias nos prompts, nos exemplos de classificação e no processo de avaliação dos modelos.

---

**Responsável pela análise:** Dados e Qualidade  
**Arquivo analisado:** `eval/results/results_100_metrics.csv`
