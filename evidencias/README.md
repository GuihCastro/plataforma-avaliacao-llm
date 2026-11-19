# Índice de evidências — T17

Este índice liga as afirmações da documentação técnica às fontes do repositório e indica como conferi-las. A documentação é uma primeira versão: observações marcadas como pendentes precisam de confirmação ou de evidência anexada.

## Afirmações verificadas

| Afirmação | Fonte | Como conferir |
|---|---|---|
| A branch de documentação parte do merge do PR #9 (`3b9e07c`). | Histórico Git local; lista de arquivos alterados no merge. | Na raiz, execute `git log -1 --oneline --decorate`, `git show --stat 3b9e07c` e `git merge-base --is-ancestor 3b9e07c HEAD`. Nesta revisão, o último comando terminou com código 0. |
| O dataset contém 100 chamados e seis categorias; sua distribuição é 17, 17, 17, 17, 16 e 16. | [`eval/datasets/test_cases.csv`](../eval/datasets/test_cases.csv), [`eval/generate_test_cases.py`](../eval/generate_test_cases.py), [`docs/relatorio_qualidade_dados.md`](../docs/relatorio_qualidade_dados.md). | Conte as linhas de dados e agrupe por `expected`; confira também as asserções de quantidade e distribuição no gerador. |
| `results_100_metrics.csv` tem 300 registros, 100 por modelo, para 100 chamados distintos. | [`eval/results/results_100_metrics.csv`](../eval/results/results_100_metrics.csv), [`eval/model_comparison.py`](../eval/model_comparison.py). | Ler o CSV com `csv.DictReader`; contar as linhas, agrupar por `model` e contar valores distintos de `input`. Nesta rodada foram obtidos 100 / 100 / 100 e 100 chamados. |
| Os acertos do CSV atual são 46, 24 e 32 para Qwen, Llama e Gemma, respectivamente. | [`eval/results/results_100_metrics.csv`](../eval/results/results_100_metrics.csv), [`docs/analise_erros_classificacao.md`](../docs/analise_erros_classificacao.md). | Contar linhas com `correct=true` por `model`; conferir com a análise de erros. O arquivo [`docs/Metricas_consumo.md`](../docs/Metricas_consumo.md) diverge (49, 22, 37) e precisa ser reconciliado antes de citar esses valores como definitivos. |
| O CSV de regressão arquivado contém 20 pares distintos, 10 acertos originais e 3 degradados, diferença de −35 p.p. | [`eval/results/results_old/regression_results_prompt_comparison.csv`](../eval/results/results_old/regression_results_prompt_comparison.csv), [`tests/test_results_csv.py`](../tests/test_results_csv.py), [`src/results_csv.py`](../src/results_csv.py). | Contar linhas, chamados distintos e valores `true` em `original_correct` e `degraded_correct`; calcular `100 * (3/20 - 10/20)`. Os testes de regressão conferem esses números. |
| A regressão arquivada não deve ser confundida com a execução futura ou com a bateria que a equipe escolherá para o relatório. | [`PROMPTS.md`](../PROMPTS.md), seções da T11; [`eval/regression_test.py`](../eval/regression_test.py). | A preparação da T11 registra a decisão da equipe como pendente. O script atual grava em `eval/results/regression_results_prompt_comparison.csv`, fora de `results_old`. |
| O relatório publicado para a regressão diverge do CSV arquivado: relata 9 e 3 acertos, enquanto o CSV contém 10 e 3. | [`docs/Teste_regressao.md`](../docs/Teste_regressao.md), [`eval/results/results_old/regression_results_prompt_comparison.csv`](../eval/results/results_old/regression_results_prompt_comparison.csv), [`PROMPTS.md`](../PROMPTS.md). | Comparar a tabela do relatório com uma contagem das colunas de veredito no arquivo arquivado. O histórico da T11 já sinaliza a discrepância. |
| A revisão humana tem 30 linhas, 10 por modelo, mas apenas 10 chamados distintos repetidos entre os modelos. | [`eval/results/human_review_30.csv`](../eval/results/human_review_30.csv), [`eval/results/human_review_30_calibrated.csv`](../eval/results/human_review_30_calibrated.csv), [`docs/LLM_judge_calibracao.md`](../docs/LLM_judge_calibracao.md). | Contar linhas por `model` e valores distintos de `input`; ambos os CSVs apresentam 10 linhas por modelo e 10 entradas distintas. Não descrever como 30 chamados independentes. |
| O painel e o leitor CSV têm testes locais registrados na T11. | [`tests/test_app.py`](../tests/test_app.py), [`tests/test_results_csv.py`](../tests/test_results_csv.py), [`PROMPTS.md`](../PROMPTS.md), seção 5. | O registro da T11 contém o comando `.\.venv\Scripts\python.exe -m pytest -q tests/test_app.py tests/test_results_csv.py` e a saída reportada de 17 testes e 16 subtestes aprovados. A mesma execução foi repetida nesta rodada. |
| O teste do cliente Ollama inclui uma geração de sucesso dependente do serviço local. | [`tests/test_ollama_client.py`](../tests/test_ollama_client.py), [`src/ollama_client.py`](../src/ollama_client.py). | Inspecione `test_ollama_client_success` e execute-o apenas com Ollama e o modelo configurados. Os testes focados de painel/CSV não fazem chamadas a modelos. |
| O código documentado usa Streamlit, CSVs e Ollama HTTP; o juiz aplica comparação direta antes da chamada ao modelo. | [`src/app.py`](../src/app.py), [`src/results_csv.py`](../src/results_csv.py), [`src/ollama_client.py`](../src/ollama_client.py), [`src/llm_judge.py`](../src/llm_judge.py). | Inspecione as fontes e compare os nomes de arquivos padrão e as chamadas mencionadas na documentação. |
| `eval.calibration` seleciona um CSV calibrado localmente e calcula concordância sem chamar modelos. | [`eval/calibration.py`](../eval/calibration.py), [`eval/rejudge_results.py`](../eval/rejudge_results.py), [`eval/rejudge_human_review.py`](../eval/rejudge_human_review.py). | `calibration.py` usa `input()` para escolher arquivo e lê CSV; não importa `LLMJudge`/`OllamaClient`. Os scripts `rejudge_*` usam `LLMJudge`, que pode chamar `qwen2.5:3b` via Ollama. |
| As origens e os tratamentos documentados distinguem bateria, resultados, regressão e revisão humana. | [`eval/generate_test_cases.py`](../eval/generate_test_cases.py), [`eval/model_comparison.py`](../eval/model_comparison.py), [`eval/regression_test.py`](../eval/regression_test.py), [`eval/human_review.py`](../eval/human_review.py), [`PROMPTS.md`](../PROMPTS.md). | Compare o código e o histórico de solicitações; autoria/fonte externa por registro não é declarada e continua pendente de confirmação. |
| A licença MIT do repositório não prova a licença dos dados nem dos pesos externos. | [`LICENSE`](../LICENSE), arquivos CSV e [`src/ollama_client.py`](../src/ollama_client.py). | A licença do repositório é MIT; não há licença individual para CSVs/modelos nem versões dos pesos registradas. Verificar os termos upstream e o escopo dos dados antes de redistribuir. |
| A cobertura de testes ainda não foi medida. | [`tests/`](../tests), [`PROMPTS.md`](../PROMPTS.md). | O histórico registra quantidade de testes, não porcentagem de cobertura; não foi encontrado relatório gerado por ferramenta de coverage. |
| SQLite, avaliação disparada pelo painel e identificação/versionamento dos prompts são pendências. | [`src/app.py`](../src/app.py), [`src/results_csv.py`](../src/results_csv.py), [`eval/results/results_100_metrics.csv`](../eval/results/results_100_metrics.csv). | O painel lê arquivos locais; não há uso de SQLite nem chamada de execução da avaliação. Parser admite `prompt_version` opcional, mas o CSV atual não tem essa coluna. |

### Resultado da verificação dos CSVs nesta rodada

Contagens calculadas a partir dos arquivos locais:

- Dataset: 100 linhas e 100 mensagens distintas.
- Resultados de modelos: 300 linhas, 100 por modelo; 100 mensagens distintas; acertos 46 / 24 / 32.
- Regressão arquivada: 20 linhas e mensagens distintas; 10 acertos originais e 3 degradados.
- Revisão humana e versão calibrada: 30 linhas cada; 10 por modelo e 10 mensagens distintas.

Essas contagens verificam a estrutura e os campos registrados; não reexecutam os modelos nem validam manualmente cada classificação.

## Evidências pendentes

| Evidência a obter | Situação nesta branch |
|---|---|
| Vídeo de 3–5 minutos, com a tela inteira, iniciando o projeto por `docker compose up` e percorrendo o fluxo principal. | Nenhum arquivo de vídeo foi identificado. O Compose atual só executa testes e não inicia o painel; integrar primeiro um serviço Streamlit, depois gravar e anexar a captura real de tela inteira. |
| Logs completos de uma execução dos modelos e da regressão. | Não há log persistido identificado. Salvar saída de terminal, parâmetros, versões do modelo, data e arquivos de saída em uma execução controlada. |
| CI verde na tag `v1.0`, com link direto e captura da execução. | A branch local não contém a tag `v1.0`; a consulta GitHub à tag não encontrou commit, a API de Actions retornou zero workflows e zero execuções filtradas para `v1.0`. A página [GitHub Actions](https://github.com/GuihCastro/plataforma-avaliacao-llm/actions) é apenas o local de consulta, não substitui o link da execução. Criar/confirmar tag e workflow, executar CI e anexar link mais captura. |
| Integração do Compose para abrir o painel. | [`compose.yaml`](../compose.yaml) define apenas `testes`, e [`Dockerfile`](../Dockerfile) executa pytest. `docker compose up` não inicializa Streamlit; adicionar serviço/porta/comando do painel é pendência. |
| Confirmação da bateria que a equipe escolherá para o relatório. | O CSV de 20 pares é arquivado e a T11 registra a decisão como pendente; obter decisão explícita da equipe e identificador/versão da bateria. |
| Captura real da interface e confirmação das escolhas arquiteturais. | Esta documentação foi conferida por leitura de código e AppTest; não foi feita captura visual nesta rodada. Confirmar com Guilherme/equipe motivações e alternativas arquiteturais que não constam nos registros. |
| Reconciliação dos números dos relatórios com os CSVs. | `Metricas_consumo.md` diverge dos resultados em CSV; `Teste_regressao.md` diverge do CSV arquivado. Definir a fonte da versão final e corrigir ou contextualizar os relatórios após aprovação. |
| Licenças específicas dos conjuntos de dados e versões dos modelos. | [`LICENSE`](../LICENSE) declara MIT para o projeto; não foi encontrada licença por dataset nem referência com versão/digest e licença dos modelos usados. Verificar origem/termos de cada fonte antes da publicação. |

## Falhas analisadas e contribuições/revisões do grupo

### Falhas

O relatório [`docs/Analise_erros.md`](../docs/Analise_erros.md) descreve quatro casos individuais. Links diretos para três deles:

- [Caso 1 — Qwen 2.5 1.5B: webcam classificada como Instalação](https://github.com/GuihCastro/plataforma-avaliacao-llm/blob/main/docs/Analise_erros.md#L11).
- [Caso 2 — Qwen 2.5 1.5B: monitor com faixa preta classificado como Instalação](https://github.com/GuihCastro/plataforma-avaliacao-llm/blob/main/docs/Analise_erros.md#L20).
- [Caso 3 — Llama 3.2 3B: conexão cabeada classificada como Acesso](https://github.com/GuihCastro/plataforma-avaliacao-llm/blob/main/docs/Analise_erros.md#L29).
- [Caso 4 — Llama 3.2 3B: Wi-Fi ausente classificado como Configuração](https://github.com/GuihCastro/plataforma-avaliacao-llm/blob/main/docs/Analise_erros.md#L38).

### Contribuições e revisões

Links públicos de contribuições e revisões encontrados no histórico do repositório:

| Registro | Contribuição/revisão verificável |
|---|---|
| [PR #4 — implementação da plataforma](https://github.com/GuihCastro/plataforma-avaliacao-llm/pull/4) | Contribuição de Hugo (`HugoM-Git`). |
| [PR #5 — relatório de qualidade dos dados](https://github.com/GuihCastro/plataforma-avaliacao-llm/pull/5) | Contribuição de Johnny (`Jviudes-hub`). |
| [PR #7 — calibração do Judge e análise de erros](https://github.com/GuihCastro/plataforma-avaliacao-llm/pull/7) | Contribuição de Johnny; [revisão aprovada por Guilherme](https://github.com/GuihCastro/plataforma-avaliacao-llm/pull/7#pullrequestreview-5966642984). |
| [PR #8 — comparação dos resultados no painel](https://github.com/GuihCastro/plataforma-avaliacao-llm/pull/8) | Contribuição de Guilherme. A consulta de reviews deste PR não retornou revisão registrada. |
| [PR #9 — regressão de prompts no painel](https://github.com/GuihCastro/plataforma-avaliacao-llm/pull/9) | Contribuição de Guilherme. A consulta de reviews deste PR não retornou revisão registrada. |

## Verificações da versão inicial da T17

Na raiz do repositório:

```powershell
.\.venv\Scripts\python.exe -m pytest -q tests/test_app.py tests/test_results_csv.py
```

Saída final observada: `17 passed, 16 subtests passed in 4.65s`.

Também foram contadas as linhas e distribuições dos CSVs com `csv.DictReader` no Python da `.venv`, e conferido o histórico Git para confirmar o merge do PR #9. Não foram executados Ollama, a comparação completa de modelos, a CI ou uma captura de vídeo.

## Revisão de evidências em 19/11/2026

- `git merge-base --is-ancestor 3b9e07c HEAD` terminou com código 0.
- A conferência automática dos links relativos dos documentos encontrou 61 destinos e nenhum link quebrado.
- `git diff --check HEAD` não apontou problemas de whitespace.
- A consulta GitHub retornou zero workflows e zero execuções de Actions filtradas pela branch/tag `v1.0`; a consulta da tag não encontrou commit. Não foi anexado link de execução verde ou captura.
- A verificação foi documental: não foram reexecutados testes, modelos ou avaliações nesta revisão.
