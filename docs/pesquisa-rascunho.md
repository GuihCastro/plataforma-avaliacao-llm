# Avaliação de modelos de linguagem na classificação de chamados de suporte em português

**Documento:** rascunho de pesquisa — T17
**Versão:** para revisão da equipe
**Autores, ordem e afiliações:** pendentes de confirmação
**PDF final previsto:** `docs/pesquisa-abnt.pdf`

> Este arquivo organiza os textos e os resultados já disponíveis. Ainda não é a versão completa de 12–20 páginas textuais. Cada seção indica o que precisa de redação, conferência ou aprovação humana. Os números são associados aos arquivos consultados; divergências entre registros são mantidas explícitas.

## Resumo

Este estudo preliminar compara três modelos de linguagem na classificação de chamados de suporte de TI em português. A bateria local contém 100 chamados sintéticos, aplicados aos modelos `qwen2.5:1.5b`, `llama3.2:3b` e `gemma3:1b`, totalizando 300 registros. No CSV principal, os modelos obtiveram, respectivamente, 46, 24 e 32 acertos. A avaliação principal compara a resposta normalizada com a categoria esperada; o resultado de um juiz híbrido é armazenado separadamente. O juiz resolve correspondências textuais diretamente em Python e, nos demais casos, pode consultar `qwen2.5:3b`. Em um CSV arquivado de regressão de prompts, 20 pares produziram 50% de acurácia com o prompt original e 15% com o degradado, uma queda de 35 pontos percentuais. A revisão humana arquivada contém 30 avaliações, mas corresponde a 10 chamados distintos repetidos entre três modelos. Os dados indicam diferenças entre os modelos nesta amostra, mas o conjunto sintético, as divergências entre versões dos CSVs e a pequena revisão humana limitam qualquer generalização.

**Para a versão completa:** validar o objetivo e os termos do resumo com os autores; reconciliar as versões dos resultados e decidir quais números representam a execução final.

## Abstract

This preliminary study compares three language models on Portuguese IT support-ticket classification. A local synthetic dataset contains 100 tickets, evaluated with `qwen2.5:1.5b`, `llama3.2:3b`, and `gemma3:1b`, for 300 records. In the primary CSV, the models obtained 46, 24, and 32 exact-match correct classifications, respectively. The primary classifier metric is kept separate from the hybrid judge output. The judge resolves normalized exact matches in Python and may call `qwen2.5:3b` for other responses. An archived prompt-regression CSV contains 20 paired cases: accuracy was 50% with the original prompt and 15% with the degraded prompt, a 35-percentage-point decrease. The archived human review contains 30 evaluations of only 10 distinct tickets, repeated across three models. These results describe the available artifacts and do not support broad generalization because the dataset is synthetic and small, the repository contains conflicting result snapshots, and the human-review sample is limited.

**Para a versão completa:** revisar a tradução técnica, confirmar a terminologia estatística e atualizar o abstract depois da revisão do resumo e dos resultados.

## Palavras-chave

Modelos de linguagem; classificação de chamados; avaliação de modelos; juiz híbrido; regressão de prompts.

**Para a versão completa:** confirmar a lista e a forma exigida pelo evento ou pela instituição.

## 1 Introdução

A classificação de chamados de suporte de TI em categorias como Hardware, Software, Rede, Acesso, Instalação e Configuração é o problema aplicado neste projeto. A equipe reuniu uma bateria local de 100 exemplos sintéticos e registrou respostas de três modelos de linguagem. A pergunta provisória deste rascunho é: **como os três modelos se comparam, por correspondência textual com a categoria esperada, nessa bateria?**

O objetivo provisório é descrever os acertos observados e as limitações do procedimento. A comparação utiliza 300 registros do arquivo principal de resultados. Uma análise de erros já descreve confusões entre categorias, e uma regressão arquivada compara dois prompts nos mesmos 20 chamados. Esses experimentos são complementares, mas não devem ser tratados como uma única execução ou como amostras independentes da mesma dimensão.

O escopo é exploratório: os exemplos são sintéticos, a métrica principal é textual e os artefatos históricos apresentam resultados diferentes. Este rascunho não afirma que a diferença observada represente desempenho geral em chamados reais.

**Para a versão completa, a equipe deve:** redigir a motivação acadêmica e social com fontes verificadas; validar a pergunta, os objetivos geral e específicos e a contribuição pretendida; identificar autores, instituição, curso e contexto de realização.

## 2 Referencial teórico

O texto de apoio com as oito fontes foi fornecido pelo usuário nesta conversa; não foi encontrado um arquivo de apoio separado no workspace. As páginas de origem foram consultadas diretamente em 19 de novembro de 2026. Para os quatro artigos, foram conferidos os metadados e os resumos nas páginas do arXiv, não o texto integral. Portanto, as afirmações abaixo se limitam ao que esses resumos e metadados sustentam, e a leitura integral pelos integrantes continua pendente. As quatro páginas de documentação oficial foram abertas diretamente; quando o endereço não identifica uma versão fixa, isso é indicado nas referências.

### Avaliação comparativa e métricas

O HELM organiza a avaliação de modelos por cenários e por múltiplas métricas, incluindo acurácia, calibração, robustez, justiça, viés, toxicidade e eficiência. Os autores descrevem avaliações em condições padronizadas e a publicação de prompts e respostas, defendendo transparência e comparação de mais de uma dimensão (LIANG et al., 2023). Essa proposta sustenta a relevância metodológica de aplicar os mesmos chamados aos modelos e relatar medidas complementares. Não significa, porém, que este projeto implemente o HELM, cubra os cenários dele ou tenha medido todas essas dimensões: a métrica principal aqui é correspondência textual com a categoria esperada, e os tempos e tokens vêm dos artefatos locais.

### Juízes automáticos e critérios explícitos

Zheng et al. investigam modelos de linguagem usados como juízes de respostas abertas e discutem vieses de posição, verbosidade e autopreferência, além de limitações de raciocínio. O resumo também compara os juízes com preferências humanas em MT-Bench e Chatbot Arena (ZHENG et al., 2023). Isso fundamenta a necessidade de avaliar o juiz e explicitar suas limitações, mas os resultados do artigo — inclusive sua concordância quantitativa — não são resultados deste projeto. O juiz local é híbrido: a correspondência normalizada é resolvida em Python e só os demais casos podem seguir para `qwen2.5:3b`, conforme [o código do juiz](../src/llm_judge.py).

G-Eval propõe avaliar textos gerados com instruções e preenchimento de um formulário, estudando sumarização e diálogo e comparando os julgamentos com avaliações humanas (LIU et al., 2023). Essa fonte pode orientar a discussão sobre critérios explícitos e validação humana. O experimento publicado não é uma avaliação de classificação de chamados; tampouco se deve chamar a regra local de igualdade normalizada ou o juiz híbrido de implementação de G-Eval.

### Avaliação humana e diferença de tarefa

Chatbot Arena usa comparações pareadas de respostas e votos de uma comunidade ampla para avaliar preferências humanas (CHIANG et al., 2024). Essa abordagem ajuda a contextualizar o papel da avaliação humana, mas difere do procedimento local: a revisão arquivada contém 30 registros de 10 chamados distintos, distribuídos pelos três modelos, e considera avaliações de respostas para categorias esperadas; não é uma votação crowdsourced, nem uma comparação pareada de preferência. A metodologia e os resultados dessa plataforma não devem ser atribuídos à amostra da equipe.

### Documentação das ferramentas usadas ou planejadas

A documentação do endpoint `POST /api/generate` do Ollama descreve os campos `prompt_eval_count`, `eval_count` e durações em nanossegundos, entre outros. Isso dá contexto aos nomes das métricas consumidas pelo [cliente local](../src/ollama_client.py); a forma efetivamente agregada deve ser descrita com base no [comparador de modelos](../eval/model_comparison.py), e não inferida apenas da documentação do serviço (OLLAMA, s.d.).

A página oficial do Streamlit o apresenta como framework Python para aplicações de dados interativas. Ela contextualiza a escolha da tecnologia do painel, enquanto os componentes e fluxos entregues devem ser descritos pelo [código da aplicação](../src/app.py) (STREAMLIT, s.d.).

A documentação `sqlite3` do Python descreve conexões, execução de SQL, leitura e gravação. Ela serve como referência para a persistência planejada, não como evidência de recurso implementado: na base desta branch, a persistência de resultados continua em CSV e SQLite permanece pendente (PYTHON SOFTWARE FOUNDATION, s.d.).

O pytest documenta execução de testes, asserções, fixtures e demais recursos do framework. A página dá contexto à ferramenta; a quantidade aprovada do projeto vem dos registros de execução em [`PROMPTS.md`](../PROMPTS.md), e a cobertura percentual ainda não foi medida. Esta rodada documental não executou testes (PYTEST, s.d.).

**Para a versão completa, a equipe deve:** ler integralmente os quatro artigos; revisar a adequação das citações e das diferenças entre os cenários publicados e os chamados sintéticos em português; confirmar o padrão autor-data e a formatação bibliográfica exigidos pela instituição; completar a discussão sem transferir resultados externos para a amostra local.

## 3 Metodologia

### Desenho e conjunto de dados

O trabalho é descrito aqui como um estudo comparativo, quantitativo e exploratório, executado localmente. A bateria [`eval/datasets/test_cases.csv`](../eval/datasets/test_cases.csv) contém 100 mensagens distintas, distribuídas entre seis categorias: Hardware (17), Software (17), Rede (17), Acesso (17), Instalação (16) e Configuração (16). O histórico de geração registra a intenção de criar exemplos sintéticos e preservar dez exemplos anteriores; a proveniência detalhada de cada linha não está registrada.

### Classificadores avaliados e métrica principal

Os três classificadores são `qwen2.5:1.5b`, `llama3.2:3b` e `gemma3:1b`, chamados pelo fluxo de `eval/model_comparison.py`. Cada modelo recebeu os 100 chamados, resultando em 300 linhas no [`results_100_metrics.csv`](../eval/results/results_100_metrics.csv). O campo `correct` é calculado no executor por comparação textual normalizada da resposta com a categoria esperada. A taxa reportada como acurácia é o número de `correct=true` dividido por 100 para cada modelo.

Não confundir essa medida com o parecer do juiz: `judge_correct` e `judge_reason` são campos distintos e não substituem `correct`. O campo principal é uma correspondência textual, não uma avaliação semântica feita por humanos.

### Juiz híbrido

O `LLMJudge` normaliza a categoria esperada e a resposta. Se houver correspondência exata após normalização, o Python marca o parecer como correto sem chamada ao juiz de linguagem. Caso contrário, pode enviar a mensagem original, a categoria esperada e a resposta ao modelo `qwen2.5:3b`, que retorna uma avaliação estruturada. Esse fluxo auxilia a anotação do juiz e é analisado separadamente do resultado principal dos três classificadores.

### Regressão de prompts

O arquivo arquivado [`regression_results_prompt_comparison.csv`](../eval/results/results_old/regression_results_prompt_comparison.csv) contém 20 pares e aplica as duas versões de prompt aos mesmos chamados. O script atual documenta amostragem com semente `42` e uso de `qwen2.5:1.5b`, mas grava em outro caminho (`eval/results/regression_results_prompt_comparison.csv`). O CSV em `results_old` é tratado como uma amostra de execução arquivada, não como a seleção final da bateria.

### Revisão humana e calibração

Os CSVs [`human_review_30.csv`](../eval/results/human_review_30.csv) e [`human_review_30_calibrated.csv`](../eval/results/human_review_30_calibrated.csv) têm 30 linhas: 10 registros por modelo para os mesmos 10 chamados distintos. O script `eval.calibration` lê um CSV calibrado local escolhido interativamente e calcula concordância/Kappa sem chamar Ollama; os scripts de reavaliação do juiz são etapas distintas e podem chamar o modelo.

### Reprodutibilidade e informações faltantes

As fontes do procedimento são [`eval/model_comparison.py`](../eval/model_comparison.py), [`eval/regression_test.py`](../eval/regression_test.py), [`src/llm_judge.py`](../src/llm_judge.py), [`eval/calibration.py`](../eval/calibration.py) e os CSVs acima. Os arquivos não identificam versões/digests dos modelos executados, hardware, versão do Ollama, parâmetros completos de geração, nem uma versão de prompt associada a cada registro. Também não há logs completos da execução disponíveis nesta revisão.

**Para a versão completa, a equipe deve:** confirmar se a descrição do desenho é adequada; registrar ambiente, versões de modelos e parâmetros; esclarecer quem produziu e revisou os rótulos esperados; definir o procedimento humano e o juiz como instrumentos distintos; decidir qual execução arquivada é a referência e fornecer logs reprodutíveis.

## 4 Resultados e discussão

### Comparação dos três classificadores

A contagem recalculada diretamente no CSV principal é:

| Classificador | Registros | Acertos (`correct=true`) | Acurácia por correspondência textual |
|---|---:|---:|---:|
| `qwen2.5:1.5b` | 100 | 46 | 46% |
| `llama3.2:3b` | 100 | 24 | 24% |
| `gemma3:1b` | 100 | 32 | 32% |
| **Total** | **300** | **102** | **34%** |

Nesta execução registrada, o Qwen 2.5 1.5B teve mais correspondências textuais, seguido pelo Gemma 3 1B e pelo Llama 3.2 3B. Esta ordenação descreve apenas o CSV analisado; não foram calculados intervalos de confiança nem testes de significância. A análise de erros atribui 198 erros ao campo `correct` e discute confusões como Rede/Acesso, Hardware/Instalação e Rede/Configuração ([análise detalhada](analise_erros_classificacao.md)).

### Divergências entre versões de resultados

Os documentos e arquivos históricos não representam todos a mesma fotografia. A conferência desta revisão encontrou:

| Artefato | Acertos Qwen / Llama / Gemma | Observação |
|---|---|---|
| [`eval/results/results_100_metrics.csv`](../eval/results/results_100_metrics.csv) e análise de erros atual | 46 / 24 / 32 | Base principal deste rascunho; 300 linhas. |
| [`eval/results/results_old/results_100_metrics.csv`](../eval/results/results_old/results_100_metrics.csv) e [Métricas de consumo](Metricas_consumo.md) | 49 / 22 / 37 | Outro CSV arquivado; os números do relatório correspondem a esse arquivo antigo. |
| [`eval/results/results_old/results_100.csv`](../eval/results/results_old/results_100.csv) | 51 / 25 / 38 | Terceiro snapshot arquivado, com contagens diferentes. |

As diferenças devem ser tratadas como snapshots de execuções distintas até que a equipe confirme a proveniência. Não se deve combinar os valores nem atribuir causa às diferenças sem logs e metadados de execução.

### Regressão arquivada

O CSV de regressão consultado pelo painel tem 20 pares, 10 acertos com o prompt original (50%) e 3 com o degradado (15%). A diferença **degradado − original** é **−35 pontos percentuais**. Essa é uma amostra arquivada; não demonstra que o time já selecionou a bateria para o relatório final.

Há divergência entre artefatos de regressão: [Teste de Regressão de Prompt](Teste_regressao.md) relata 9 e 3 acertos (45% e 15%, queda de 30 p.p.); o arquivo [`regression_results.csv`](../eval/results/results_old/regression_results.csv) contém 11 e 2; o CSV arquivado usado no painel contém 10 e 3. Não há metadados suficientes para vincular o texto do relatório a um desses arquivos. A equipe precisa identificar a execução de cada relato antes de consolidar a versão final.

### Revisão humana e juiz

O CSV calibrado apresenta 30 concordâncias em 30 registros (100%, Kappa calculado em 1,00), mas esses registros são apenas 10 chamados repetidos entre três modelos. Essa concordância não comprova desempenho geral nem representa 30 situações independentes.

Também há divergência na distribuição: os CSVs de revisão mostram 10 avaliações humanas positivas e 20 negativas, enquanto [`LLM_judge_calibracao.md`](LLM_judge_calibracao.md) relata 7 positivas e 23 negativas. O [relatório de calibração](relatorio_calibracao_judge.md) informa 30 concordâncias, mas não especifica essa divisão. A concordância foi recalculada a partir do CSV; a contagem 7/23 precisa ser reconciliada antes de reutilização.

### Síntese e limitações interpretativas

Os resultados demonstram que os artefatos disponíveis permitem descrever diferenças de classificação e erros de categoria, mas ainda não sustentam uma conclusão sobre superioridade geral. A bateria é sintética, contém 100 mensagens, e a medida principal penaliza respostas semanticamente corretas com redação diferente. O juiz híbrido e a revisão humana têm papéis e amostras próprios; seus resultados não devem ser misturados aos acertos dos classificadores.

**Para a versão completa, a equipe deve:** escolher e documentar uma versão de cada resultado; reconciliar as divergências indicadas; validar se 34% agregado é pertinente além das acurácias individuais; redigir a discussão em diálogo com as oito fontes após leitura; avaliar limitações, validade externa e possíveis análises estatísticas sem extrapolar a amostra.

## 5 Considerações finais

Este rascunho organiza uma comparação de três classificadores em 100 chamados sintéticos, registra 46, 24 e 32 acertos no CSV principal e separa esses resultados dos pareceres do juiz híbrido `qwen2.5:3b`. Também distingue a regressão arquivada (20 pares, 50% versus 15%, queda de 35 p.p.) de outras versões históricas e esclarece que 30 avaliações humanas cobrem apenas 10 chamados. As divergências entre documentos e snapshots impedem apresentar todos os números como uma única execução consolidada.

Como conclusão provisória, o `qwen2.5:1.5b` obteve mais acertos textuais que os outros modelos na base atual. Essa observação é restrita ao conjunto e ao critério empregados; não estabelece que o modelo seja melhor em outros domínios ou chamados reais.

**Para a versão completa, a equipe deve:** redigir contribuições, implicações e recomendações após resolver as divergências; decidir se os dados e procedimentos permitem responder à pergunta de pesquisa; registrar trabalhos futuros e restrições; revisar resumo e abstract por último.

## Referências

As referências abaixo correspondem às fontes citadas no texto. Para os artigos, os dados de versão e publicação foram conferidos nas páginas do arXiv; a leitura integral permanece pendente para a equipe. As páginas de documentação têm endereços versionados ou dinâmicos conforme indicado.

CHIANG, Wei-Lin et al. *Chatbot Arena: An Open Platform for Evaluating LLMs by Human Preference*. arXiv:2403.04132, versão 1, submetida em 7 mar. 2024. DOI: [10.48550/arXiv.2403.04132](https://doi.org/10.48550/arXiv.2403.04132). Disponível em: [https://arxiv.org/abs/2403.04132v1](https://arxiv.org/abs/2403.04132v1). Acesso em: 19 nov. 2026.

LIANG, Percy et al. *Holistic Evaluation of Language Models*. arXiv:2211.09110, versão 2, revisada em 1 out. 2023; submetida originalmente em 16 nov. 2022. Publicado em *Transactions on Machine Learning Research* (TMLR), 2023. DOI: [10.48550/arXiv.2211.09110](https://doi.org/10.48550/arXiv.2211.09110). Disponível em: [https://arxiv.org/abs/2211.09110v2](https://arxiv.org/abs/2211.09110v2). Acesso em: 19 nov. 2026.

LIU, Yang et al. *G-Eval: NLG Evaluation using GPT-4 with Better Human Alignment*. arXiv:2303.16634, versão 3, revisada em 23 maio 2023. DOI: [10.48550/arXiv.2303.16634](https://doi.org/10.48550/arXiv.2303.16634). Disponível em: [https://arxiv.org/abs/2303.16634v3](https://arxiv.org/abs/2303.16634v3). Acesso em: 19 nov. 2026.

OLLAMA. *Generate a response*. Documentação do endpoint `/api/generate`; a página não identifica uma versão editorial fixa (a especificação exibida informa OpenAPI 3.1.0). Disponível em: [https://docs.ollama.com/api/generate](https://docs.ollama.com/api/generate). Acesso em: 19 nov. 2026.

PYTHON SOFTWARE FOUNDATION. *sqlite3 — DB-API 2.0 interface for SQLite databases*. Documentação Python 3; o endereço `/3/` não fixa uma versão menor (a página consultada aponta o código-fonte CPython 3.15). Disponível em: [https://docs.python.org/3/library/sqlite3.html](https://docs.python.org/3/library/sqlite3.html). Acesso em: 19 nov. 2026.

PYTEST. *pytest documentation*. Documentação no endereço dinâmico `stable`; a página consultada não identifica uma versão numérica fixa. Disponível em: [https://docs.pytest.org/en/stable/](https://docs.pytest.org/en/stable/). Acesso em: 19 nov. 2026.

STREAMLIT. *Streamlit documentation*. Página inicial da documentação; não identifica versão editorial fixa. Disponível em: [https://docs.streamlit.io/](https://docs.streamlit.io/). Acesso em: 19 nov. 2026.

ZHENG, Lianmin et al. *Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena*. arXiv:2306.05685, versão 4, revisada em 24 dez. 2023. NeurIPS 2023, Datasets and Benchmarks Track. DOI: [10.48550/arXiv.2306.05685](https://doi.org/10.48550/arXiv.2306.05685). Disponível em: [https://arxiv.org/abs/2306.05685v4](https://arxiv.org/abs/2306.05685v4). Acesso em: 19 nov. 2026.

### Registros internos usados para este rascunho

Estas fontes internas sustentam descrições do projeto e contagens, mas não substituem o referencial acadêmico nem estão formatadas para a versão ABNT final:

- [Documentação técnica da T17](documentacao-tecnica.md).
- [Índice de evidências da T17](../evidencias/README.md).
- [Relatório de métricas e consumo](Metricas_consumo.md).
- [Análise de erros de classificação](analise_erros_classificacao.md).
- [Análise de casos de falha](Analise_erros.md).
- [Relatório de teste de regressão](Teste_regressao.md).
- [Relatório de calibração do Judge](relatorio_calibracao_judge.md).
- [Relatório de qualidade dos dados](relatorio_qualidade_dados.md).
- [Calibração do LLM Judge](LLM_judge_calibracao.md).
- [Reavaliação das avaliações humanas](Reavaliacao_human_review.md).
- [`eval/datasets/test_cases.csv`](../eval/datasets/test_cases.csv).
- [`eval/results/results_100_metrics.csv`](../eval/results/results_100_metrics.csv).
- [`eval/results/results_old/regression_results_prompt_comparison.csv`](../eval/results/results_old/regression_results_prompt_comparison.csv).
- [`eval/results/human_review_30_calibrated.csv`](../eval/results/human_review_30_calibrated.csv).

**Para a versão completa:** ler integralmente os quatro artigos e validar a síntese com os integrantes; confirmar o padrão bibliográfico exigido, revisar as citações e referências e gerar/revisar `docs/pesquisa-abnt.pdf` depois da aprovação da equipe.
