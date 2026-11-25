# Registro de interações com IA

**Guilherme Henrique de Castro — Produto e Interface**

## 1. Criação do contrato e do exemplo sintético

- **Data:** 31/10/2026
- **Responsável:** Guilherme Henrique de Castro
- **Ferramenta:** GitHub Copilot Free, seleção Auto; modelo específico não informado.
- **Prompt completo:**

> Estamos na T06 do Projeto Integrador — Tema 3: uma plataforma para avaliar modelos de linguagem na classificação de chamados de suporte em português.
>
> Leia README.md e guia_repositorio_tema3.md para entender o projeto.
>
> Crie somente estes dois arquivos:
>
> 1. docs/contrato-avaliacao.md
> Um rascunho curto, claro e didático, em português, contendo:
> - Fluxo da interface: selecionar bateria de casos, modelo e prompt → executar → acompanhar o estado → comparar resultados.
> - Uma tabela dos dados necessários, com nome, tipo e significado.
> - Dados da execução: identificador, data, estado, versões da bateria, modelo e prompt, parâmetros e identificação do juiz.
> - Dados por caso: identificador, chamado, categoria esperada, resposta original, categoria prevista, justificativa, acerto, nota do juiz, tempo em milissegundos, tokens de entrada e saída e eventual erro.
> - Regras para valores indisponíveis: usar null, sem confundir ausência de medição com zero.
> - Falhas, respostas inválidas e timeouts devem permanecer registrados e entrar no total de casos da acurácia.
> - Pendências que precisam de validação da equipe.
>
> 2. docs/exemplo-avaliacao.json
> Um exemplo válido e coerente com o documento, contendo dois casos fictícios: um sucesso e uma falha. Identifique explicitamente o arquivo com "sintetico": true. Medições não realizadas devem ficar null.
>
> As categorias, as métricas e a rubrica do juiz ainda dependem da validação de Hugo na T05. Identifique sugestões como propostas, sem apresentá-las como decisões aprovadas.
>
> Use a estrutura mais simples que atenda ao pedido. Preserve os arquivos existentes. Nesta tarefa, produza apenas os dois documentos, sem implementar a aplicação nem instalar dependências. Não faça commit ou push.
>
> Ao terminar, explique brevemente o que criou e quais decisões ficaram pendentes. Não afirme ter executado modelos ou testes que não executou.
- **Resumo da resposta real:** Foram criados o contrato e um exemplo sintético com um caso de sucesso e um timeout. A resposta informou que o JSON foi validado. Na revisão, foram encontrados números de desempenho fictícios apesar de nenhum modelo ter sido executado, a possibilidade de usar juiz havia sido deixada como pendente e o formato JSON da resposta não estava documentado.
- **Decisão:** **Correções solicitadas** — Corrigir esses três problemas: retirar medições inventadas e usar `null`, registrar o juiz de IA como requisito e propor o formato JSON com categoria e justificativa, ainda sujeito à validação na T05.

## 2. Correção das medições, do requisito do juiz e do formato da resposta

- **Data:** 31/10/2026
- **Responsável:** Guilherme Henrique de Castro
- **Ferramenta:** GitHub Copilot Free, seleção Auto; modelo específico não informado.
- **Prompt completo:**

> Revise somente docs/contrato-avaliacao.md e docs/exemplo-avaliacao.json:
>
> 1. Medições:
> Nenhum modelo foi executado. Portanto, tempo_ms, tokens_entrada e tokens_saida devem ser null nos dois casos. Remova os números fictícios de desempenho e ajuste a observacao para informar que não houve medições. Preserve os parâmetros de configuração, como temperature: 0.
>
> 2. Juiz de IA:
> No contrato, remova a pendência “definir se haverá juiz”. O juiz de IA calibrado contra avaliações humanas é requisito do Tema 3. Permanecem pendentes a escolha do juiz, sua versão e a definição da rubrica com Hugo.
>
> 3. Formato da resposta:
> Documente como formato proposto um JSON com categoria e justificativa, sujeito à validação na T05. No caso de sucesso do exemplo, represente esse JSON dentro de resposta_original, mantendo esse campo como string. Garanta coerência com categoria_prevista e justificativa.
>
> Preserve o restante e mantenha explícito que o exemplo é inteiramente sintético. Valide a sintaxe do JSON e informe a verificação realizada. Não execute modelos, não implemente a aplicação e não faça commit ou push.
- **Resumo da resposta real:** Os dois documentos foram revisados; as medições foram definidas como `null`, `temperature: 0` foi preservada, o juiz de IA foi registrado como requisito e o formato proposto foi documentado. A sintaxe JSON e a coerência entre a resposta original e os campos interpretados foram verificadas.
- **Decisão:** **Aceito como rascunho para revisão da equipe** — As correções foram conferidas, mas categorias, métricas e rubrica ainda dependem da T05. Isso não representa aprovação da equipe nem do PR.

## 3. Implementação e revisão do painel de resultados (T11)

Guilherme Henrique de Castro conduziu a implementação com GitHub Copilot e revisou o resultado com ChatGPT. A validação local ocorreu em 07/11/2026.

### Prompt completo preparado nesta conversa para o Copilot

> Vamos implementar a primeira versão da T11: painel de resultados em Streamlit.
>
> Leia o README e a estrutura existente. Reaproveite as configurações do projeto.
>
> Crie src/app.py e somente os arquivos auxiliares necessários.
>
> Para os dados de demonstração, consulte o exemplo existente na branch docs/t06-fluxo-contrato:
> git show docs/t06-fluxo-contrato:docs/exemplo-avaliacao.json
>
> Copie esse exemplo, sem alterar seu conteúdo, para eval/exemplos/exemplo-avaliacao.json.
>
> A interface deve:
> - Abrir com o exemplo carregado e mostrar “Demonstração — dados sintéticos”.
> - Permitir carregar outro arquivo JSON no mesmo formato.
> - Exibir modelo, versão do prompt, quantidade de casos, acertos e falhas.
> - Mostrar uma tabela dos casos e permitir consultar chamado, resposta, justificativa e erro.
> - Apresentar tempo e tokens null como “Não medido”.
> - Tratar arquivo inválido ou lista de casos vazia com mensagem clara.
>
> Mantenha a interface simples e em português. As categorias e a rubrica continuam sujeitas à validação da equipe.
>
> Inclua testes com pytest para leitura inválida, inclusão das falhas no denominador da acurácia e preservação de medições ausentes. Execute as verificações usando a .venv e informe os comandos e resultados reais.
>
> Declare somente as dependências utilizadas, reaproveitando os arquivos existentes. Nesta etapa, trabalhe na consulta dos resultados, sem executar modelos ou configurar infraestrutura. Não faça commit ou push.

### Resumo da resposta real

O Copilot implementou o painel em `src/app.py`, com demonstração sintética, upload e validação de JSON, indicadores, tabela e detalhes por caso. Copiou o exemplo para `eval/exemplos/exemplo-avaliacao.json`, atualizou o `README.md`, declarou as dependências em `requirements.txt` e acrescentou os testes em `tests/test_app.py`. Relatou quatro testes aprovados na primeira versão, além das verificações com Streamlit AppTest, `py_compile` e conferência do JSON.

### Decisão e justificativa

**Aceito após revisão para o commit inicial da T11.** A versão revisada separou classificações incorretas de falhas de execução, passou a rejeitar falhas marcadas como acerto, preservou o aviso de exemplo sintético após o upload e apresentou uma mensagem para erros de leitura. Foi acrescentado um teste de regressão para o timeout marcado como acerto.

### Validação local

O comando `.\.venv\Scripts\python.exe -m pytest tests\test_app.py` retornou **5 testes aprovados**. O upload do exemplo manteve o aviso de demonstração e exibiu dois casos, um acerto, uma falha de execução e 50% de acurácia. A consulta de `caso-demo-002` mostrou `TIMEOUT`, com resposta e justificativa indisponíveis.

---

## 4. Consulta dos resultados gravados no painel (T11)

- **Data:** 18/11/2026
- **Ferramenta:** Codex no ChatGPT.
- **Pedido de Guilherme:**

> Pronto, foi feito o merge do meu último commit e, em seguida, de mais uma colaboração de outro colega. Agora vamo:
>
> 1. Pegar o último commit;
> 2. Checar o andamento do projeto (prazos, onde estamos, o que falta);
> 3. Continuar

**Resposta e implementação proposta:** conferiu a `main` no commit `7979bd4`, os relatórios e o quadro do projeto. Preparou o painel para ler `eval/results/results_100_metrics.csv`, comparar os modelos e consultar respostas e pareceres. Manteve a demonstração e o upload JSON e acrescentou o upload de CSV.

**Decisões e verificação:** a acurácia usa o campo `correct` de todos os registros de cada modelo. O parecer do juiz aparece separado e uma versão ausente do prompt fica identificada como tal. A leitura dos dados publicados recuperou 46, 24 e 32 acertos em 100 casos por modelo. Os cinco testes novos do leitor passaram na cópia de trabalho. A execução da interface com Streamlit e a revisão pela equipe ficam para a validação do PR.

Na primeira execução de Guilherme no Windows, passaram 10 testes e 12 subtestes. O teste do painel atingiu o limite padrão de 3 segundos ao abrir o CSV, antes de conferir a tabela. Após receber essa saída, o Codex ajustou o limite do AppTest para 30 segundos por execução. A abertura do CSV e a troca para a demonstração JSON ainda precisam ser confirmadas no Windows. (atualização: Em 18/11/2026, Guilherme confirmou que a validação local do painel funcionou no Windows após o ajuste do teste.)

---

## 5. Regressão de prompts no painel (T11)

### Preparação em 18/11/2026

Guilherme pediu ao Codex no ChatGPT

> Feito. Forcei o merge com bypass porque temos urgência em terminar. Sigamos, lembrando que desenvolvimento e escrita de código devem ser escrita pra IA que estamos usando e os prompts devidamente registrados no arquivo

O Codex conferiu o merge do PR #8 na `main` (`cc03b4a`), registrou no Notion o bypass informado por Guilherme e verificou o CSV pareado. Em 20 chamados, o arquivo arquivado contém 10 acertos do prompt original e 3 do degradado. O relatório da T16 cita 9 e 3. O próximo pedido concentra a mudança na interface e preserva a identificação do arquivo de origem. A equipe de avaliação decidirá qual execução usar na entrega.

### Solicitação preparada para o GitHub Copilot Free no VS Code

Mensagem para iniciar a tarefa no modo Agente

> Execute a especificação da seção “Regressão de prompts no painel (T11)” de PROMPTS.md e complete o registro com o que você fizer.

**Especificação referenciada na mensagem**

1. Na branch `feat/t11-regressao-painel`, adicione a opção “Regressão de prompts” ao painel Streamlit em `src/app.py`. Leia localmente `eval/results/results_old/regression_results_prompt_comparison.csv`. Mostre o nome do arquivo e identifique a amostra como experimento arquivado. Mantenha os fluxos atuais de CSV, upload e demonstração JSON.
2. Compare `original_correct` e `degraded_correct` sobre as mesmas linhas. Exiba o total de pares, os acertos e a acurácia de cada prompt. Calcule a variação em pontos percentuais como 100 × (acurácia degradada − acurácia original). Mostre se houve queda, estabilidade ou melhora. Permita selecionar um chamado e consultar a categoria esperada e as duas respostas. Arquivo vazio, colunas ausentes ou veredito inválido devem produzir uma mensagem clara. Reaproveite a leitura e a validação existentes onde forem compatíveis.
3. Comece pelos testes do cálculo e da validação com amostras pequenas. Cubra queda, empate, melhora e entrada inválida. Exercite a nova opção com Streamlit AppTest. Rode na `.venv` os testes do painel e de CSV, incluindo os novos. Use os resultados publicados para conferir a tela. Nesse arquivo específico os valores esperados são 50%, 15% e −35 pontos percentuais. Calcule os números a partir dos dados. A execução desta tarefa usa os arquivos locais e as dependências atuais.
4. Acrescente ao README uma instrução curta para abrir a comparação. Concentre as mudanças no painel, em sua leitura de dados, nos testes, no README e neste registro. Os CSVs e a escolha da bateria para o relatório pertencem à T16. Deixe o diff na branch para revisão de Guilherme antes de commit e push.
5. Ao terminar, atualize esta mesma entrada com a data da execução, a ferramenta e o modelo se identificado, o resumo da sua resposta, os arquivos alterados, os comandos de teste realmente executados e os resultados observados, inclusive falhas. Se houver um novo pedido de correção, registre também o seu texto e a resposta. A decisão de aceitar, corrigir ou descartar e o motivo serão preenchidos após a revisão humana.

**Execução do Copilot** — Executada em 18/11/2026 pelo GitHub Copilot usando o Copilot SDK no VS Code; o modelo específico não foi informado pela ferramenta.

O Copilot adicionou a opção **Regressão de prompts** ao painel, com leitura local de
`eval/results/results_old/regression_results_prompt_comparison.csv`, identificação do
arquivo e do experimento arquivado, métricas dos dois prompts, variação em pontos
percentuais, classificação da variação e consulta individual das respostas. Os fluxos
atuais de resultados publicados, demonstração JSON e upload foram preservados.

**Arquivos alterados:**

- `src/app.py` — nova opção de fonte e renderização da comparação.
- `src/results_csv.py` — leitura, validação e resumo dos pares de regressão.
- `tests/test_app.py` — testes AppTest da nova opção e dos valores publicados.
- `tests/test_results_csv.py` — testes de queda, empate, melhora, entrada inválida e
  resultados publicados.
- `README.md` — instrução curta para abrir a comparação no painel.
- `PROMPTS.md` — registro desta execução.

**Comandos realmente executados:**

```powershell
.\.venv\Scripts\python.exe -m pytest -q tests/test_app.py tests/test_results_csv.py
```

**Resultados observados:**

- A primeira execução passou 13 testes e 16 subtestes, mas apresentou duas falhas:
  uma em um teste AppTest porque um caminho temporário não pertencia à raiz do projeto
  e outra em uma expectativa incorreta de −50 para uma amostra cuja variação calculada
  era −100 pontos percentuais.
- A falha de caminho foi corrigida exibindo o caminho relativo quando possível e o
  absoluto em arquivos temporários ou externos.
- A expectativa incorreta foi corrigida para −100 pontos percentuais.
- A execução repetida passou **15 testes e 16 subtestes**.
- Os dados publicados têm **20 pares**, 10 acertos do prompt original e 3 do degradado,
  portanto 50%, 15% e **−35 pontos percentuais**.

### Pedido de correção registrado em 19/11/2026

> Na T11, use `st.warning` para queda, `st.info` para estabilidade e `st.success` para melhora. Ajuste a métrica e a mensagem para que uma variação fracionária como −0,4 p.p. fique visível. Preserve o resultado de −35 p.p. do CSV arquivado.
>
> Atualize os testes para verificar o aviso de queda e a exibição da variação fracionária. Rode `.\.venv\Scripts\python.exe -m pytest -q tests/test_app.py tests/test_results_csv.py`.
>
> Na seção 5 de `PROMPTS.md`, registre este pedido, resuma as correções e copie a última linha real do pytest. Preserve o histórico das rodadas anteriores e deixe uma única decisão de aceite pendente da revisão de Guilherme. Deixe as alterações na branch para revisão antes do commit.

**Correções desta rodada** — A variação agora é apresentada com uma casa decimal tanto
na métrica quanto na mensagem, preservando o sinal e a unidade; o banner usa `st.warning`
para queda, `st.info` para estabilidade e `st.success` para melhora. Os testes verificam
o aviso de queda, a visibilidade de −0,4 p.p. e a manutenção do valor arquivado de
−35 p.p.

**Validação desta rodada** — Executado
`.\.venv\Scripts\python.exe -m pytest -q tests/test_app.py tests/test_results_csv.py`.
Última linha real: `17 passed, 16 subtests passed in 2.32s`

Aceito para revisão da equipe. Conferi no painel os resultados dos 20 pares e o aviso de queda de 50% para 15%. O teste automatizado cobre a variação de −0,4 p.p.

## 6. Documentação técnica e evidências (T17)

- **Data:** 19/11/2026
- **Responsável:** Guilherme Henrique de Castro
- **Ferramenta:** GitHub Copilot usando o Copilot SDK no VS Code; modelo específico não informado.
- **Pedido completo:**

> Prepare a primeira versão da documentação técnica da T17 a partir desta branch, que inclui o PR #9. Escreva em português para alguém que acabou de clonar o repositório.
>
> 1. Crie docs/documentacao-tecnica.md com os nove tópicos do enunciado: visão geral e arquitetura com diagrama e fluxo dos dados, instalação e execução, decisões de arquitetura, referência da interface, dados e modelos, reprodução das avaliações, testes e CI, segurança/privacidade/limitações e manual do usuário. Reaproveite os guias e relatórios por links relativos. Detalhe os passos para abrir o painel no Windows e consultar modelos e regressão. Nas 3 a 5 decisões previstas, inclua contexto e alternativas apenas com as evidências disponíveis. Identifique o que precisa de confirmação ou captura real.
>
> 2. Crie evidencias/README.md ligando cada afirmação comprovada ao arquivo e à forma de conferência. Verifique os 300 resultados de 100 chamados em 3 modelos, a regressão do CSV arquivado de 20 pares e os testes locais registrados no PROMPTS.md. Distinga a amostra arquivada da bateria que a equipe ainda vai selecionar e as 30 linhas de revisão humana dos 10 chamados distintos que elas representam. Identifique as evidências pendentes, incluindo o vídeo, os logs da execução completa e a CI verde da versão final.
>
> 3. Confira os caminhos relativos e a precisão das instruções. Mantenha esta rodada nos dois documentos e em PROMPTS.md. Na seção de Guilherme, registre esta mensagem integral, a ferramenta, um resumo do resultado, os arquivos e as verificações realmente feitas. Deixe a decisão de aceite para Guilherme e apresente o diff antes de commit e push.

**Resumo do resultado:** criada uma primeira versão com os nove tópicos solicitados e um índice de evidências que associa afirmações às fontes e aos métodos de conferência. Foram registradas as contagens dos CSVs e explicitadas as divergências entre alguns relatórios e seus arquivos de dados. A documentação distingue a regressão arquivada da bateria pendente de seleção e esclarece que 30 revisões humanas representam 10 chamados repetidos entre três modelos.

**Arquivos alterados nesta rodada:**

- `docs/documentacao-tecnica.md` — documentação técnica T17.
- `evidencias/README.md` — índice de evidências, verificações e pendências.
- `PROMPTS.md` — registro deste pedido e desta execução.

**Verificações realmente feitas:** conferido no histórico Git o merge do PR #9 (`3b9e07c`); contadas as linhas, mensagens distintas, modelos e acertos dos CSVs; executado `.\.venv\Scripts\python.exe -m pytest -q tests/test_app.py tests/test_results_csv.py`, com resultado `17 passed, 16 subtests passed in 4.65s`; verificados 38 links relativos nos dois documentos novos, sem links quebrados. Não foram executados os modelos, a CI, uma execução completa, nem foram gravados vídeo ou logs de modelo.

### Pedido de revisão registrado em 19/11/2026

> Revise `docs/documentacao-tecnica.md` e `evidencias/README.md` conforme os pontos abaixo.
>
> 1. Corrija o diagrama para mostrar que o juiz usa `qwen2.5:3b` e devolve sua avaliação ao executor. O desenho atual encaminha o juiz ao grupo dos três modelos avaliados.
> 2. Alinhe as evidências ao enunciado. O vídeo deve ter **3–5 minutos**, mostrar a **tela inteira**, iniciar o projeto com `docker compose up` e percorrer o fluxo principal. A CI final precisa de link e captura da execução na tag `v1.0`. Inclua também os vínculos para pelo menos três falhas analisadas e para as contribuições e revisões do grupo. Registre a integração do Compose como pendente, pois a configuração atual executa testes.
> 3. Complete a seção de dados e modelos com origem, tratamento e licenças verificadas ou identificadas como pendentes. Informe que a cobertura de testes ainda não foi medida. Explicite as pendências de SQLite, execução de avaliações pelo painel e identificação das versões dos prompts.
> 4. Esclareça que `eval.calibration` calcula concordância lendo um CSV local. A escolha do arquivo é interativa e esse cálculo funciona sem Ollama. Diferencie-o das reavaliações que chamam modelos. Para conferir a base da branch, use `git merge-base --is-ancestor 3b9e07c HEAD`.
>
> Registre este pedido integral e as correções na seção 6 de `PROMPTS.md`. Verifique novamente os links relativos e o diff. Mantenha o aceite de Guilherme pendente e apresente o resultado antes do commit.

**Correções desta rodada:** o diagrama separa os três modelos avaliados do `qwen2.5:3b` usado pelo juiz e representa o retorno da avaliação ao executor. A documentação agora registra as condições do vídeo e da evidência de CI na tag `v1.0`, bem como a integração do Compose como pendente. Foram detalhadas origem e tratamento dos dados, escopo conhecido da licença MIT e licenças externas ainda não verificadas; incluídas as pendências de cobertura, SQLite, execução via painel e identificação dos prompts. Também foi esclarecida a calibração local sem Ollama, diferenciada das reavaliações que podem chamar modelos, e acrescentados links para falhas, contribuições e uma revisão aprovada do grupo.

**Arquivos alterados nesta rodada:** `docs/documentacao-tecnica.md`, `evidencias/README.md` e este registro.

**Verificações desta rodada:** `git merge-base --is-ancestor 3b9e07c HEAD` terminou com código 0. A consulta GitHub não encontrou workflows/execuções de Actions nem um commit associado à tag `v1.0`; não foi apresentada uma CI verde inexistente. Foram verificados 61 links relativos nos dois documentos, sem destinos quebrados; `git diff --check HEAD` não apontou problemas. Não foram alterados código ou testes.

Aceito para revisão da equipe. As correções solicitadas foram incorporadas. As pendências da entrega estão identificadas nos documentos.

## 7. Rascunho de pesquisa acadêmica (T17)

- **Data:** 19/11/2026
- **Responsável:** Guilherme Henrique de Castro
- **Ferramenta:** GitHub Copilot usando o Copilot SDK no VS Code; modelo específico não informado.
- **Pedido completo:**

> Na branch docs/t17-rascunho-pesquisa, organize e revise os textos já produzidos pela equipe para preparar docs/pesquisa-rascunho.md. Leia docs/documentacao-tecnica.md, evidencias/README.md, os relatórios em docs/ e os CSVs citados. Use a redação dos integrantes e os resultados comprovados como base.
>
> Organize o rascunho em resumo, abstract, palavras-chave, 1 Introdução, 2 Referencial teórico, 3 Metodologia, 4 Resultados e discussão, 5 Considerações finais e Referências. Identifique por seção o que precisa de redação ou validação da equipe para a versão completa de 12–20 páginas textuais. O PDF final previsto é docs/pesquisa-abnt.pdf.
>
> Na metodologia e nos resultados, diferencie o classificador dos três modelos e o juiz híbrido qwen2.5:3b. Apresente os 300 registros de 100 chamados, com 46, 24 e 32 acertos por modelo. Identifique a regressão como amostra arquivada de 20 pares, com 50% e 15% e queda de 35 pontos percentuais. Contextualize as divergências dos relatórios. A revisão humana contém 30 registros de 10 chamados distintos. Registre limitações e pendências com base nas evidências.
>
> Para o referencial, comece pelas oito fontes listadas no cartão T17. Confira os trechos originais e os metadados antes de inserir citações e referências. Relacione cada fonte ao que ela sustenta e cite apenas as que utilizar. Se o conteúdo estiver inacessível, sinalize a leitura pendente. Os artigos tratam de cenários diferentes do nosso estudo. Informações bibliográficas incompletas e afirmações que precisem de redação dos autores devem ficar identificadas para revisão humana.
>
> Atualize a seção de Guilherme em PROMPTS.md com este pedido integral, ferramenta, resumo do que organizou e revisou, fontes consultadas e verificações efetivamente feitas. Confira os links. Apresente o diff e deixe a decisão de aceite para Guilherme antes do commit.

**Resumo do resultado:** organizado um rascunho acadêmico nas seções solicitadas, com notas de redação/validação por seção e caminho previsto para o PDF. A metodologia separa os três classificadores do juiz híbrido; os resultados usam as contagens do CSV principal e distinguem snapshots divergentes de regressão e calibração. O cartão/lista das oito fontes acadêmicas não foi localizado no repositório, nos issues disponíveis ou no histórico de sessão consultado. Não foram inventadas citações: a leitura, a síntese comparativa e as referências dessas fontes estão marcadas como pendentes.

**Fontes internas consultadas:** `docs/documentacao-tecnica.md`, `evidencias/README.md`, os relatórios `docs/Metricas_consumo.md`, `docs/analise_erros_classificacao.md`, `docs/Analise_erros.md`, `docs/Teste_regressao.md`, `docs/relatorio_calibracao_judge.md`, `docs/relatorio_qualidade_dados.md`, `docs/LLM_judge_calibracao.md`, `docs/Reavaliacao_human_review.md` e `docs/contrato-avaliacao.md`; trechos relevantes de `PROMPTS.md`; código de comparação, juiz, calibração e regressão. Foram lidos os CSVs atuais e arquivados usados nos resultados, incluindo bateria, métricas, pares de regressão e revisão humana.

**Verificações efetivamente feitas:** as contagens foram recalculadas com `csv.DictReader`. O CSV principal tem 300 linhas (100 por modelo) e 46/24/32 acertos; o CSV de regressão do painel tem 20 pares e 10/3 acertos; a revisão humana tem 30 linhas, 10 chamados distintos e concordância 30/30. Foram identificados snapshots antigos (49/22/37 e 51/25/38), versões de regressão divergentes (11/2 e 10/3 versus os 9/3 do relatório) e diferença entre o CSV de calibração (10/20) e o texto de `LLM_judge_calibracao.md` (7/23). Foram verificados 32 links relativos em `docs/pesquisa-rascunho.md`, sem destinos quebrados; as nove seções solicitadas estão presentes. `git diff --check` terminou sem apontamentos. Não foram executados modelos ou testes.

**Arquivos alterados nesta rodada:** `docs/pesquisa-rascunho.md` e `PROMPTS.md`.

### Revisão do referencial teórico e das referências da T17

- **Data:** 19/11/2026
- **Responsável:** Guilherme Henrique de Castro
- **Ferramenta:** GitHub Copilot usando o Copilot SDK no VS Code; modelo específico não informado. As páginas de origem foram consultadas diretamente com `web_fetch`.
- **Pedido registrado:**

> Use o material fornecido para revisar o referencial teórico e as referências de `docs/pesquisa-rascunho.md`. Relacione cada fonte às afirmações que ela sustenta. Diferencie as notas fornecidas das fontes que você conseguir consultar diretamente e registre as leituras pendentes.
>
> Na seção 7 de `PROMPTS.md`, registre este pedido, o uso do arquivo de apoio, as correções e as verificações realizadas. Mantenha o aceite de Guilherme pendente e apresente o diff antes do commit.

**Material de apoio:** o texto “Fontes de apoio para o rascunho da T17”, com quatro artigos e quatro documentações, foi fornecido diretamente na mensagem do usuário. Não havia arquivo de apoio separado no workspace. As notas fornecidas serviram de roteiro; não foram tratadas como prova de leitura integral dos artigos.

**Resumo do resultado:** substituída a tabela de fontes não identificadas por uma síntese que relaciona as oito fontes às afirmações que podem sustentar, citações autor-data no texto e referências com links e versões identificadas quando disponíveis. O texto diferencia os cenários dos artigos dos experimentos locais e liga as documentações ao código ou às pendências do projeto. Os artigos foram consultados diretamente apenas pela página arXiv de metadados e resumo; a leitura integral pelos integrantes continua pendente.

**Fontes consultadas diretamente:** páginas arXiv de HELM (`2211.09110v2`), LLM-as-a-Judge (`2306.05685v4`), G-Eval (`2303.16634v3`) e Chatbot Arena (`2403.04132v1`); documentação do endpoint Generate do Ollama, página inicial da documentação Streamlit, referência Python `sqlite3` e documentação pytest no endereço `stable`. As páginas Ollama, Streamlit e pytest não fixam uma versão numérica; a URL do Python é `/3/` e a página consultada aponta para código CPython 3.15. A data de acesso registrada é 19/11/2026.

**Verificações efetivamente feitas:** conferidos os metadados e resumos nas quatro páginas arXiv, as versões fixadas e os DOIs, além das quatro páginas oficiais de documentação. Os 37 links relativos do rascunho não têm destinos quebrados; os 12 links externos incluídos foram consultados. `git diff --check` passou e uma checagem adicional de whitespace nos dois arquivos não encontrou ocorrências inesperadas. Não foram executados testes nem lidos integralmente os artigos.

**Arquivos alterados nesta rodada:** `docs/pesquisa-rascunho.md` e `PROMPTS.md`.

**Correção adicional:** removidos os espaços ao final das linhas 3, 4 e 5 de `docs/pesquisa-rascunho.md`, mantendo as linhas em branco que separam o cabeçalho. As alterações ficam na branch para revisão; nenhum commit foi feito.

Aceito como rascunho para revisão da equipe. A leitura integral das fontes, a ampliação do texto e a preparação do PDF ABNT permanecem pendentes.

---

## 8. Resolução do conflito do PR #13

- Data de execução — 21/11/2026.
- Ferramenta — Codex no ChatGPT.
- Pedido de Guilherme

> Antes de seguirmos para isso: ao tentar aceitar o PR de um colega da equipe, tive problemas de conflito com o merge. Resolva: https://github.com/GuihCastro/plataforma-avaliacao-llm/pull/13/conflicts

O Codex reproduziu o merge da `main` `1d89360` na branch `IamMorpheu-patch-1`, do PR #13, originalmente em `c072a6f`. O conflito era do tipo add/add em `src/avaliador.py`, que havia sido adicionado em ambas as branches.

A resolução mantém os logs com data e hora do PR #13, a gravação do CSV e a mensagem final no terminal. Os arquivos da infraestrutura e o cliente `gerar_classificacao` da main entram pelo merge.

A validação executou o teste existente de `tests/test_backend.py` diretamente com a geração simulada, em diretório temporário. Foram conferidos os três registros do CSV e os oito registros de log. Os CSVs e logs versionados foram preservados durante essa validação. Os oito testes de `tests/test_results_csv.py` passaram com `python -m unittest discover -s tests -p test_results_csv.py -v`. A compilação de `src/avaliador.py`, `src/ollama_client.py` e `tests/test_backend.py` com `py_compile` passou.

A instalação das dependências da suite não foi concluída no ambiente de revisão. Pytest e Streamlit ficaram indisponíveis para a execução completa. A inspeção também identificou uma incompatibilidade anterior ao PR #13, na main do PR #12. `src/ollama_client.py` fornece `gerar_classificacao`, mas retirou a classe `OllamaClient` ainda importada pelo juiz, pelos scripts de avaliação e pelos testes antigos. Essa ocorrência precisa de correção própria e não é causada pelo conflito em `avaliador.py`.

A resolução da branch do PR #13 foi preparada para conferência de Guilherme. O merge final do PR na main depende da revisão da equipe.

---

## 9. Restauração da compatibilidade do cliente Ollama

- **Data:** 21/11/2026
- **Responsável:** Guilherme Henrique de Castro
- **Ferramenta:** GitHub Copilot SDK no VS Code.
- **Prompt completo:**

> Corrija a compatibilidade de `src/ollama_client.py`.
>
> Recupere a classe anterior consultando `git show d8cbb2a:src/ollama_client.py`. Restaure `OllamaClient`, `generate` e `generate_with_metrics`, preservando seus retornos, métricas e tratamento de erros. Mantenha disponível a função atual `gerar_classificacao`, usada pelo novo backend.
>
> Para configurar o endereço da classe, respeite esta prioridade: argumento `base_url`, variável `OLLAMA_BASE_URL`, variável `OLLAMA_HOST` e endereço local padrão. Confira o uso de `OLLAMA_HOST` no Compose.
>
> Atualize `tests/test_ollama_client.py` com respostas HTTP simuladas para verificar os dois contratos, as métricas, o endereço configurado e os erros. Os testes devem funcionar localmente sem depender do Ollama.
>
> Execute na `.venv`:
>
> `.\.venv\Scripts\python.exe -m pytest -q tests/test_ollama_client.py tests/test_app.py tests/test_results_csv.py`
>
> Registre este pedido integral, as alterações, os resultados reais e as decisões na seção de Guilherme em `PROMPTS.md`. Apresente o diff e deixe o aceite pendente para revisão antes do commit.

### Alterações realizadas

- Restabelecida em `src/ollama_client.py` a classe `OllamaClient` e os métodos `generate` e `generate_with_metrics`, recuperando o contrato anterior: `generate` retorna somente texto ou `None`, enquanto `generate_with_metrics` retorna o texto e todas as métricas de entrada, saída, duração total e durações por etapa.
- Preservados os quatro modelos suportados pela versão anterior, a validação de modelo com `ValueError`, `response.raise_for_status()`, timeout de 120 segundos e o retorno `None` com mensagem de erro para `RequestException`.
- Mantida `gerar_classificacao`; a função continua retornando `response`, `latency_seconds` e `tokens` para o backend atual e passa a respeitar a configuração dinâmica de endereço.
- Implementada a prioridade de endereço `base_url` explícito, `OLLAMA_BASE_URL`, `OLLAMA_HOST` e `http://localhost:11434`. Endereços sem esquema recebem `http://`, barras finais são removidas e `0.0.0.0` é convertido para `localhost`.
- Conferido `compose.yaml`: o serviço `app` define `OLLAMA_HOST=http://ollama:11434`, endereço interno do Compose compatível com a nova resolução.
- Reescrito `tests/test_ollama_client.py` sem chamadas reais ao Ollama, usando respostas HTTP simuladas para os contratos de texto e métricas, a função `gerar_classificacao`, a prioridade de configuração, o endereço padrão, modelos inválidos, erros de conexão e erros HTTP.

### Resultado real da validação

O comando solicitado foi executado na `.venv`:

```text
..........................                                     [100%]
26 passed, 16 subtests passed in 10.37s
```

### Decisão

- Alteração preparada, validada e deixada no diff da branch para revisão.
- Não foi realizado commit nem push.
- Aceite pendente de Guilherme Henrique de Castro.

---

### Correção adicional da normalização do endereço — 21/11/2026

- **Pedido completo de Guilherme:**

> Corrija apenas a normalização do endereço em src/ollama_client.py:
>
> 1. Substitua 0.0.0.0 por localhost somente quando o hostname completo for exatamente 0.0.0.0. Preserve esquema, porta e os demais componentes.
> 2. Preserve endereços como:
>    - http://10.0.0.0:11434
>    - http://node-0.0.0.0.example:11434
> 3. Acrescente testes para esses casos e mantenha a conversão de 0.0.0.0:8080 para http://localhost:8080.
> 4. Preserve os dois contratos, a precedência das configurações e os testes existentes.
> 5. Registre este pedido integral, a correção e o resultado real da validação na seção 9 de PROMPTS.md. Mantenha o aceite humano pendente.
>
> Execute:
> .\.venv\Scripts\python.exe -m pytest -q tests/test_ollama_client.py tests/test_app.py tests/test_results_csv.py
>
> Não execute modelos reais. Não faça commit nem push.

- **Ferramenta:** GitHub Copilot SDK no VS Code.
- **Correção:** a normalização deixou de substituir texto em qualquer parte da URL e passou a comparar o hostname completo do componente `netloc`, preservando esquema, porta, caminho, consulta e fragmento. A substituição ocorre apenas para `0.0.0.0` e `0.0.0.0:<porta>`; `10.0.0.0` e `node-0.0.0.0.example` permanecem intactos.
- **Testes:** acrescentada cobertura para `http://10.0.0.0:11434` e `http://node-0.0.0.0.example:11434`, além da manutenção do caso `0.0.0.0:8080`.
- **Validação real:** o comando solicitado foi executado sem chamadas a modelos reais:

```text
...........................                                     [100%]
27 passed, 16 subtests passed in 5.29s
```

- **Decisão:** correção validada e mantida no diff para revisão. Não houve commit nem push. O aceite humano permanece pendente.

---

### Documentação das capturas manuais do painel — 21/11/2026

- **Pedido completo de Guilherme:**

> Prepare a documentação das três capturas feitas manualmente:
>
> - evidencias/imagens/painel-modelos.png
> - evidencias/imagens/painel-regressao.png
> - evidencias/imagens/painel-falha.png
>
> Confira se os arquivos existem e atualize evidencias/README.md com links relativos e descrições das imagens.
>
> Identifique a regressão como experimento arquivado e a falha TIMEOUT como demonstração com dados sintéticos. Não afirme que os modelos foram executados nesta etapa.
>
> Confira e preserve layout="wide" na chamada existente de st.set_page_config em src/app.py.
>
> Registre este pedido integralmente e as alterações realizadas na seção de Guilherme em PROMPTS.md. Informe que as capturas foram feitas manualmente por Guilherme e conferidas visualmente no ChatGPT.
>
> Não marque outras evidências pendentes como concluídas. Não execute modelos nem faça commit ou push. Apresente o diff para revisão.

- **Ferramenta:** GitHub Copilot SDK no VS Code.
- **Arquivos conferidos:** existiam os três PNGs solicitados em `evidencias/imagens/`: `painel-modelos.png`, `painel-regressao.png` e `painel-falha.png`.
- **Alterações:** adicionada em `evidencias/README.md` uma seção de capturas manuais com links relativos e descrições das três imagens. O painel de modelos não afirma nova execução. A imagem de regressão foi identificada como experimento arquivado. A imagem da falha foi identificada como demonstração sintética com `TIMEOUT`. A linha de pendências foi ajustada somente para registrar a adição das capturas e manter pendente a confirmação das escolhas arquiteturais.
- **Conferência do painel:** Guilherme adicionou manualmente `layout="wide"` em `src/app.py`, seguindo orientação do ChatGPT, para mostrar integralmente os indicadores da regressão. A etapa posterior de documentação apenas preservou esse ajuste.
- **Conferência visual:** as capturas foram feitas manualmente por Guilherme Henrique de Castro e conferidas visualmente no ChatGPT nesta etapa.
- **Validação:** não foram executados modelos reais, testes automatizados desta documentação ou avaliações. Não houve consulta ao Ollama.
- **Decisão:** documentação preparada no diff para revisão humana. Não houve commit nem push. O aceite permanece pendente de Guilherme Henrique de Castro.

---

### Integração contínua com GitHub Actions — 21/11/2026

- **Pedido completo de Guilherme:**

> Configure a integração contínua deste repositório com GitHub Actions.
>
> Crie .github/workflows/tests.yml para:
> - Executar em pull requests destinados à main, pushes na main,
>   tags v* e acionamento manual.
> - Usar Ubuntu e Python 3.11, compatível com o Dockerfile.
> - Instalar requirements.txt.
> - Executar python -m pytest -q tests/.
> - Usar permissão contents: read.
> - Definir um limite de tempo para o job.
>
> Os testes devem funcionar sem Ollama, Docker ou download de modelos.
> Preserve as chamadas HTTP simuladas existentes.
>
> O teste de backend escreve em arquivos versionados de resultados e
> logs. Ajuste seu isolamento, usando um diretório temporário, para
> que os testes não sobrescrevam evidências ou resultados reais.
> Não enfraqueça as verificações para obter aprovação.
>
> Atualize evidencias/README.md:
> - Corrija a informação desatualizada sobre Dockerfile e compose.yaml:
>   a configuração atual já inicia o painel Streamlit.
> - Diferencie configuração existente de execução validada:
>   não afirme que o Docker foi executado nesta etapa.
> - Mantenha a evidência de CI verde na tag v1.0 como pendente.
>
> Execute localmente na .venv:
> .\.venv\Scripts\python.exe -m pytest -q tests/
>
> Confira git diff --check e git status --short.
> Registre este pedido integralmente, as alterações e os resultados
> reais na seção de Guilherme em PROMPTS.md.
>
> Não execute modelos, não crie tags e não faça commit ou push.
> Apresente o diff e a saída dos testes para revisão.

- **Ferramenta:** GitHub Copilot SDK no VS Code.
- **Alterações:** criado `.github/workflows/tests.yml` com eventos para PR direcionado a `main`, push em `main`, tags `v*` e disparo manual; job em `ubuntu-latest` com Python 3.11, permissão `contents: read`, limite de 15 minutos, instalação de `requirements.txt` e comando `python -m pytest -q tests/`.
- **Isolamento do teste de backend:** `tests/test_backend.py` executa o backend em subprocesso com diretório de trabalho `tmp_path`. A chamada de geração continua simulada e é verificada três vezes; CSV e log são conferidos dentro do diretório temporário, incluindo três registros e a configuração de modelo/versão de prompt. A importação e a configuração de logging também ocorrem nesse diretório, sem sobrescrever arquivos versionados.
- **Documentação:** `evidencias/README.md` agora informa que o `Dockerfile` e `compose.yaml` configuram o serviço Streamlit, mas que a execução do Docker Compose não foi validada nesta etapa. A linha da CI verde na tag `v1.0` permanece como pendência.
- **Resultado real:** execução local do comando solicitado:

```text
............................                             [100%]
28 passed, 16 subtests passed in 2.35s
```

`git diff --check` foi executado e não indicou problemas de whitespace. `git status --short` foi conferido; apresentou `M PROMPTS.md`, `M evidencias/README.md`, `M tests/test_backend.py` e `?? .github/`.

- **Escopo de validação:** nenhum modelo foi executado; não foi executado Docker Compose ou CI remoto; nenhuma tag foi criada; não houve commit nem push.
- **Decisão:** workflow e ajustes de teste/documentação preparados para revisão. A comprovação de CI verde na tag `v1.0` permanece pendente.

---

### Validação manual do painel pelo Docker Compose — 23/11/2026

- **Pedido completo de Guilherme:**

> Documente a validação manual do painel via Docker Compose,
> realizada por Guilherme em 23/11/2026.
>
> Leia:
> - evidencias/docker-compose.log
> - evidencias/docker-compose-status.txt
>
> Atualize evidencias/README.md com links para esses arquivos e
> registre o alcance da validação:
> - docker compose up --build concluiu a construção e inicialização;
> - os serviços app e ollama ficaram em execução;
> - Guilherme abriu e conferiu as telas de resultados dos modelos,
>   regressão arquivada e demonstração JSON no localhost:8501;
> - o ChatGPT conferiu as saídas e capturas enviadas.
>
> Registre como realizada a validação manual da inicialização do
> painel pelo Compose. Mantenha pendentes o vídeo, a execução real
> dos modelos, seus logs e a CI na tag v1.0.
>
> Não afirme que houve inferência ou que a comunicação entre o
> backend e o Ollama foi testada.
>
> Registre este pedido integralmente e as alterações na seção de
> Guilherme em PROMPTS.md.
>
> Não altere código, não execute modelos e não faça commit ou push.
> Execute git diff --check e apresente o diff e git status --short.

- **Ferramenta:** GitHub Copilot SDK no VS Code.
- **Arquivos conferidos:** `evidencias/docker-compose.log` e `evidencias/docker-compose-status.txt`.
- **Alterações:** `evidencias/README.md` agora registra como realizada a validação manual da inicialização pelo Compose em 23/11/2026, links para os dois registros e a conferência das telas de resultados dos modelos, regressão arquivada e demonstração JSON em `localhost:8501`. Também registra que o ChatGPT conferiu as saídas e capturas enviadas. A descrição explicita que não houve inferência nem teste da comunicação entre backend e Ollama.
- **Pendências preservadas:** vídeo, execução real dos modelos, logs dessa execução e CI verde na tag `v1.0` permanecem pendentes.
- **Verificação:** `git diff --check` não apontou problemas de whitespace. `git status --short` apresentou `M PROMPTS.md`, `M evidencias/README.md` e `?? evidencias/docker-compose-status.txt`.
- **Escopo:** nenhuma alteração de código; modelos não foram executados; não houve commit nem push.

---

### Correção da fonte dos logs de inicialização do Compose — 23/11/2026

- **Pedido completo de Guilherme:**

> Ajuste a documentação da validação do Docker Compose:
>
> 1. Use evidencias/docker-compose-inicializacao.txt como arquivo
>    versionável dos logs de inicialização. Atualize os links no
>    evidencias/README.md.
>
> 2. Esclareça que esse arquivo contém a saída dos serviços obtida
>    com docker compose logs --no-color --timestamps.
>    Ele não contém as etapas da construção da imagem.
>
> 3. Registre separadamente que a conclusão do build foi conferida
>    na saída de docker compose up --build enviada por Guilherme
>    ao ChatGPT.
>
> 4. Registre essa correção em PROMPTS.md, preservando integralmente
>    os pedidos anteriores e mantendo as demais pendências.
>
> Não altere código nem execute novamente o build ou modelos.
> Não faça commit ou push.
> Execute git diff --check e apresente o diff e git status --short.

- **Ferramenta:** GitHub Copilot SDK no VS Code.
- **Alterações:** os links em `evidencias/README.md` agora apontam para `evidencias/docker-compose-inicializacao.txt` e `evidencias/docker-compose-status.txt`. A documentação distingue a saída de `docker compose logs --no-color --timestamps`, que não contém etapas de build, da confirmação separada da conclusão do build na saída de `docker compose up --build` enviada por Guilherme ao ChatGPT. O registro anterior do pedido e da validação foi preservado.
- **Pendências preservadas:** vídeo, execução real dos modelos, logs da execução dos modelos e CI verde na tag `v1.0`.
- **Verificação:** `git diff --check` não apontou problemas de whitespace. `git status --short` apresentou `M PROMPTS.md`, `M evidencias/README.md`, `?? evidencias/docker-compose-inicializacao.txt` e `?? evidencias/docker-compose-status.txt`.
- **Escopo:** nenhuma alteração de código; build e modelos não foram executados novamente; não houve commit nem push.

---

### Registro do vídeo de demonstração — 23/11/2026

- **Pedido completo de Guilherme:**

> Confira evidencias/video-demonstracao.mp4 e adicione um link
> relativo para ele em evidencias/README.md.
>
> Registre que é uma gravação real da demonstração, compactada
> pelo ChatGPT, com aproximadamente 1min43s e sem narração audível.
> Guilherme decidiu manter essa versão. Informe a duração real,
> sem afirmar que atende ao intervalo solicitado de 3–5 minutos.
>
> Registre este pedido e as alterações na seção de Guilherme
> em PROMPTS.md. Preserve as demais pendências.
>
> Não altere código nem execute modelos. Não faça commit ou push.
> Execute git diff --check e apresente o diff e git status --short.

- **Ferramenta:** GitHub Copilot SDK no VS Code.
- **Arquivo conferido:** o vídeo foi encontrado em `evidencias/videos/video-demonstracao.mp4` (dentro de `videos/`, não diretamente na raiz de `evidencias/`). A duração lida dos metadados MP4 é 102,891 segundos, isto é, 1 min 42,891 s (aproximadamente 1 min 43 s).
- **Alterações:** `evidencias/README.md` contém um link relativo para o vídeo e registra que é uma gravação real, compactada pelo ChatGPT, sem narração audível. Também registra que Guilherme decidiu manter esta versão e que sua duração não atende ao intervalo solicitado de 3–5 minutos.
- **Pendências preservadas:** execução real dos modelos e regressão, logs dessa execução e CI verde na tag `v1.0`. O requisito de duração de 3–5 minutos não é atendido pela versão mantida.
- **Escopo:** nenhuma alteração de código; modelos não foram executados; não houve commit nem push.

---

### Documentação da regressão real 20261123-213619 — 23/11/2026

- **Pedido completo de Guilherme:**

> Documente a execução real de regressão 20261123-213619.
>
> Leia:
> - eval/results/execucoes/20261123-213619/regressao.csv
> - evidencias/regressao-20261123-213619.txt
>   (arquivo UTF-16; contém acentos corrompidos na saída capturada).
>
> Preserve os arquivos originais e confira os resultados:
> 20 chamados distintos, 10 acertos originais, zero degradados,
> nenhuma resposta vazia e queda de 50 pontos percentuais.
>
> Crie docs/regressao-20261123-213619.md explicando:
> - modelo qwen2.5:1.5b, ID registrado 65ec06548149;
> - execução em 23/11/2026 no horário de Brasília;
> - semente 42 usada somente para selecionar a amostra;
> - geração com parâmetros padrão do Ollama;
> - avaliação por comparação exata normalizada, sem LLM juiz;
> - respostas extensas do prompt degradado também falham no formato;
> - resultados específicos desta rodada, sem generalização estatística.
>
> Atualize evidencias/README.md com links para o relatório, CSV e log.
> Diferencie esta rodada da regressão arquivada exibida pelo painel.
> Registre a regressão real e seu log como obtidos, preservando a
> pendência da comparação completa dos três modelos e da CI na v1.0.
>
> Registre este pedido integralmente e as verificações reais em
> PROMPTS.md. Não altere código ou resultados anteriores.
> Não execute modelos, faça commit ou push.
> Execute git diff --check e apresente o diff e git status --short.

- **Ferramenta:** GitHub Copilot SDK no VS Code.
- **Arquivos conferidos:** `eval/results/execucoes/20261123-213619/regressao.csv` e `evidencias/regressao-20261123-213619.txt`; também foi consultado `eval/regression_test.py` para confirmar a seleção amostral e a normalização exata.
- **Verificações reais:** o CSV contém 20 linhas e 20 entradas distintas, 10 `original_correct=true`, zero `degraded_correct=true` e nenhuma resposta vazia em nenhuma das duas colunas de resposta. As acurácias recalculadas são 50% e 0%, diferença de -50 pontos percentuais. O log UTF-16 foi decodificado sem alterar o original; os horários UTC foram convertidos para 23/11/2026, 21:36:37.233930–21:37:37.588633 no horário de Brasília. A saída tem acentos corrompidos, como indicado no pedido.
- **Alterações:** criado `docs/regressao-20261123-213619.md` com modelo e ID, horário, uso da semente apenas para a amostra, parâmetros padrão do Ollama, critério de avaliação sem LLM juiz, resultados e limites de generalização. `evidencias/README.md` agora liga relatório, CSV e log e distingue esta execução da regressão arquivada mostrada pelo painel.
- **Pendências preservadas:** comparação completa dos três modelos e CI verde na tag `v1.0`.
- **Escopo:** nenhum código ou resultado anterior foi alterado; modelos não foram executados; não houve commit nem push.

---


# Registro de uso de IA na programação — Plataforma de Avaliação de LLMs

**Hugo — IA e Avaliação**

Durante o desenvolvimento do projeto, utilizei uma ferramenta de IA como apoio na programação e na resolução de problemas que foram surgindo. A IA foi utilizada principalmente para ajudar na criação dos arquivos Python, corrigir erros, implementar as funcionalidades e analisar partes do código.

Neste documento, registrei alguns dos principais prompts que utilizei durante o desenvolvimento, junto com um resumo das respostas recebidas. Também incluí observações sobre o que foi aproveitado e o que precisou ser corrigido, já que nem todas as sugestões da IA funcionaram como esperado.

Foram selecionadas 14 interações relevantes, incluindo implementações, correções e análises. O objetivo é documentar também erros e limitações da IA, e não somente os resultados aproveitados.

IAs utilizadas: Qwen3:14b (Em conjunto com Ollama e Cline) e ChatGPT Gratuito (Apoio nos prompts e análise das respostas)

## 1. Correção de erro de sintaxe nos testes

**Objetivo:** corrigir um erro de sintaxe no teste de integração com o Ollama.

### Prompt original

> Ao executar pytest tests/test_ollama_client.py -v, ocorreu este erro:
>
> SyntaxError: unterminated string literal
> Arquivo: tests/test_ollama_client.py
> Linha 7:
> `result = client.generate("qwen2.5:1.5b", "Classifique este chamado: "")`
>
> Corrija o erro de sintaxe. Revise também o restante do arquivo para identificar outros erros semelhantes.
> Não altere o módulo src/ollama_client.py nem outros arquivos. Ao terminar, mostre exatamente o que foi corrigido.

### Resumo da resposta do Qwen

O Qwen apontou uma aspa dupla excedente no final do segundo argumento de `client.generate()` e apresentou a linha corrigida:

```python
result = client.generate("qwen2.5:1.5b", "Classifique este chamado: ")
```

Também orientou executar novamente o `pytest` para verificar se o erro havia sido resolvido.

### Resultado e avaliação

A correção indicada era específica e coerente com o erro apresentado. Nas conversas posteriores, a execução do conjunto de testes foi apresentada com **3 testes aprovados**. A resposta do Qwen, contudo, não demonstrava por si só que todos os testes haviam sido executados com sucesso; essa confirmação veio da execução posterior.

---

## 2. Correção da importação do pacote `src`

**Objetivo:** permitir que os testes importassem `OllamaClient` usando `from src.ollama_client import OllamaClient`.

### Prompt original

> O teste está falhando com:
>
> ModuleNotFoundError: No module named 'src'
>
> Confirme a estrutura do projeto e corrija a importação dos testes. A pasta src contém ollama_client.py, mas não possui init.py.
> Crie o necessário para que from src.ollama_client import OllamaClient funcione corretamente.
> Não altere a lógica do cliente Ollama nem os testes além do necessário para corrigir a importação. Explique as alterações.

### Resumo da resposta do Qwen

A resposta correspondente no arquivo explica a criação de `src/__init__.py`, vazio, para que a pasta `src` seja reconhecida como pacote Python. Ela também mostra a estrutura de diretórios esperada e recomenda executar novamente os testes.

**Observação de organização da fonte:** no arquivo de registro, essa resposta aparece depois do prompt seguinte, que trata de `stream: False`. O conteúdo da resposta, porém, é sobre a criação de `src/__init__.py`; por isso, foi associado aqui ao pedido de correção da importação, de acordo com o assunto tratado na própria resposta.

### Resultado e avaliação

A solução proposta é compatível com a correção de importação solicitada. A alteração não muda a lógica do cliente Ollama. A associação foi feita pelo conteúdo da resposta, e não apenas pela posição em que o bloco aparece no arquivo.

---

## 3. Primeira comparação automatizada entre modelos

**Objetivo:** criar uma primeira avaliação comparativa dos três modelos locais usando dez exemplos de chamados.

### Prompt original

> Vamos implementar a primeira comparação automatizada dos modelos de avaliação.
>
> Já existe:
> - src/ollama_client.py com a classe OllamaClient.
> - tests/test_ollama_client.py com três testes aprovados.
> - Os modelos instalados no Ollama:
>   qwen2.5:1.5b
>   llama3.2:3b
>   gemma3:1b
>
> Crie um script em Python que:
> 1. Utilize a classe OllamaClient existente.
> 2. Envie a mesma instrução de classificação aos três modelos.
> 3. Utilize as categorias Hardware, Software, Rede, Acesso, Instalação e Configuração.
> 4. Utilize estes 10 exemplos iniciais:
>    - Estou sem rede. -> Rede
>    - Programa travou. -> Software
>    - Internet lenta. -> Rede
>    - Sem acesso a pasta. -> Acesso
>    - Não consigo entrar no computador. -> Acesso
>    - Preciso de um programa. -> Instalação
>    - Sem máquina nessa mesa. -> Instalação
>    - Monitor parou. -> Hardware
>    - Preciso que fique dessa forma. -> Configuração
>    - Preciso do meu computador no modo noturno. -> Configuração
> 5. Compare a resposta de cada modelo com a categoria esperada.
> 6. Registre o tempo de resposta.
> 7. Exiba uma tabela no terminal com modelo, acertos, erros e tempo médio.
> 8. Salve os resultados em CSV.
>
> Não implemente dashboard, banco de dados ou LLM judge ainda.
>
> Antes de alterar arquivos, explique o que pretende criar. Reutilize o código existente e não modifique o cliente Ollama sem necessidade.

### Resumo da resposta do Qwen

O Qwen propôs um script chamado `compare_models.py`, reutilizando `OllamaClient`. Apresentou os dez exemplos, os três modelos, contagem de acertos e erros, medição de tempo médio, tabela no terminal e gravação de um CSV resumido por modelo.

### Resultado e avaliação

A resposta forneceu uma primeira estrutura funcional para comparação, mas o código apresentado enviava diretamente a mensagem do chamado ao modelo (`client.generate(model, prompt)`). Isso não atendia completamente à exigência de enviar uma instrução explícita de classificação junto com cada mensagem. Esse ponto foi identificado e corrigido em uma interação posterior.

---

## 4. Criação de `src/model_comparison.py`

**Objetivo:** organizar a comparação dos três modelos em um arquivo dentro de `src`.

### Prompt original

> Crie um único arquivo chamado `src/model_comparison.py`.
>
> Ele deve:
> 1. Importar e utilizar a classe OllamaClient de `src.ollama_client`.
> 2. Definir os três modelos: qwen2.5:1.5b, llama3.2:3b e gemma3:1b.
> 3. Definir os 10 exemplos de chamados e suas categorias esperadas que já foram estabelecidos nesta conversa.
> 4. Enviar cada exemplo aos três modelos, utilizando o mesmo prompt de classificação.
> 5. Medir o tempo de resposta de cada chamada.
> 6. Comparar a resposta com a categoria esperada.
> 7. Exibir no terminal os acertos, erros e tempo médio por modelo.
>
> Não crie outros arquivos. Não modifique nenhum arquivo existente.
>
> Ao terminar:
> - Confirme o caminho exato do arquivo criado.
> - Mostre o conteúdo do arquivo.
> - Não diga que concluiu se o arquivo não tiver sido realmente criado.

### Resumo da resposta do Qwen

O Qwen apresentou o conteúdo de `src/model_comparison.py`, com a lista dos três modelos e os dez exemplos, além de um loop para executar as chamadas, contabilizar acertos e erros e exibir uma tabela no terminal.

### Resultado e avaliação

O código serviu como ponto de partida, mas repetiu a limitação da primeira versão: não incluía a instrução textual de classificação antes da mensagem do chamado. O próprio usuário identificou essa falha e solicitou uma revisão. A afirmação do Qwen de que o arquivo havia sido criado foi tratada como uma declaração da ferramenta, não como validação independente da execução.

---

## 5. Correção do prompt de classificação e normalização das respostas

**Objetivo:** garantir que os modelos recebessem instruções explícitas e que a comparação tolerasse diferenças simples de formatação.

### Prompt original

> Revise src/model_comparison.py.
>
> Identifiquei um problema: o script está enviando apenas a mensagem original aos modelos, sem instruções de classificação.
>
> Corrija para que cada chamada envie o mesmo prompt de instrução, contendo:
>
> "Classifique a mensagem de suporte de TI em exatamente uma destas categorias: Hardware, Software, Rede, Acesso, Instalação ou Configuração. Responda somente com o nome da categoria, sem explicações."
>
> Em seguida, inclua a mensagem do chamado.
>
> Também:
> 1. Normalize a resposta antes de compará-la com a categoria esperada, ignorando diferenças de maiúsculas, minúsculas e pontuação final.
> 2. Garanta que o tempo médio seja calculado corretamente, inclusive quando houver falhas.
> 3. Não altere os 10 exemplos nem os três modelos.
> 4. Não modifique outros arquivos.
>
> Mostre o que foi alterado.

### Resumo da resposta do Qwen

O Qwen apresentou uma alteração para concatenar a instrução de classificação com o texto do chamado. Também propôs converter resposta e categoria esperada para minúsculas e registrar o tempo de execução mesmo quando ocorressem falhas.

### Resultado e avaliação

A inclusão da instrução explícita foi aproveitada como correção necessária. Entretanto, a resposta não demonstrou integralmente todos os requisitos: no trecho de código apresentado, a normalização visível usava `strip().lower()`, mas não removia efetivamente a pontuação final, apesar de a explicação afirmar que isso seria tratado. Portanto, a explicação do Qwen foi mais abrangente do que o código exibido.

---

## 6. Correções de sintaxe e gravação dos resultados em CSV

**Objetivo:** corrigir o cabeçalho da tabela e registrar os resultados individuais em `results.csv`.

### Prompt original — erro de sintaxe

> Corrija o SyntaxError em src/model_comparison.py, na linha 64.
>
> A linha atual é:
>
> `print(f"{\"Modelo\":<20} | {\"Acertos\":<7} | {\"Erros\":<5} | {\"Tempo Médio (s)\":<12}")`
>
> Substitua por uma forma válida de imprimir o cabeçalho da tabela, sem barras invertidas desnecessárias nas f-strings.
>
> Revise o restante do arquivo para garantir que não existam outros erros de sintaxe. Não altere a lógica da comparação nem os exemplos.

### Resumo da resposta do Qwen

O Qwen substituiu o cabeçalho por uma f-string válida, usando aspas simples dentro da expressão:

```python
print(f"{'Modelo':<20} | {'Acertos':<7} | {'Erros':<5} | {'Tempo Médio (s)':<12}")
```

### Prompt original — gravação do CSV

> Altere somente src/model_comparison.py para salvar os resultados individuais de cada teste em um arquivo CSV chamado results.csv na raiz do projeto.
>
> O CSV deve conter:
> - model
> - input
> - expected
> - response
> - correct
> - latency_seconds
>
> Cada modelo deve gerar 10 registros, totalizando 30 linhas.
>
> Mantenha a comparação atual no terminal, os três modelos e os dez exemplos.
> Não altere outros arquivos.

### Resumo da resposta do Qwen

O Qwen acrescentou a lista `individual_results`, a importação de `csv`, o registro de cada chamada e um `csv.DictWriter` com as seis colunas solicitadas.

Em uma solicitação posterior, o usuário informou que `results.csv` não havia sido encontrado e pediu que o caminho fosse definido com `pathlib.Path`, a partir da localização do arquivo Python. A resposta seguinte usou `Path(__file__).parent / "results.csv"`.

### Resultado e avaliação

A estrutura de gravação das linhas individuais foi aproveitada. Porém, `Path(__file__).parent` aponta para a pasta `src`, não para a raiz do projeto. Assim, a explicação do Qwen dizendo que o arquivo ficaria na raiz não correspondia ao caminho indicado no código. Em uma correção posterior do projeto, o caminho foi ajustado para usar o diretório pai de `src`, por exemplo `Path(__file__).resolve().parent.parent / "results.csv"`.

---

## 7. Criação da classe `LLMJudge`

**Objetivo:** implementar um segundo modelo para avaliar as respostas produzidas pelos modelos de classificação.

### Prompt original

> Crie o arquivo `src/llm_judge.py` para implementar um LLM Judge usando o modelo `qwen2.5:3b` via Ollama.
>
> Contexto do projeto:
> - Classificamos chamados de suporte de TI em seis categorias: Hardware, Software, Rede, Acesso, Instalação e Configuração.
> - Já existe `src/ollama_client.py`, com a classe `OllamaClient`.
> - O modelo `qwen2.5:3b` está instalado.
>
> Requisitos:
> 1. Criar uma classe chamada `LLMJudge`.
> 2. Utilizar o `OllamaClient` existente, sem duplicar a comunicação HTTP.
> 3. Criar um método `evaluate(input_text, expected, response)`.
> 4. Enviar ao juiz a mensagem original, a categoria esperada e a resposta do modelo avaliado.
> 5. O juiz deve retornar um JSON com `correct` (booleano) e `reason` (justificativa breve).
> 6. Validar a resposta JSON e tratar erros de conexão, respostas vazias e JSON inválido.
> 7. Não modificar `ollama_client.py`, `model_comparison.py` ou qualquer outro arquivo.
> 8. Não criar dashboard ainda.
>
> Ao terminar, mostre o código criado e explique brevemente como testar a classe.

### Resumo da resposta do Qwen

O Qwen apresentou uma classe `LLMJudge` que reutilizava `OllamaClient`, montava um prompt com a mensagem, categoria esperada e resposta recebida, chamava `qwen2.5:3b` e tentava interpretar o retorno como JSON.

### Resultado e avaliação

A estrutura geral da classe e a reutilização do cliente foram aproveitadas como base. Contudo, havia um problema na verificação de resposta vazia: o bloco que verificava `judge_response.strip()` aparecia depois dos blocos que já retornavam em caso de JSON inválido ou erro. Dessa forma, a verificação de resposta vazia não era executada no fluxo pretendido. Foi necessário solicitar uma correção.

---

## 8. Validação e correção da implementação do `LLMJudge`

**Objetivo:** permitir o modelo do juiz e validar corretamente a estrutura do JSON retornado.

### Prompt original

> Corrija a implementação do LLMJudge com os seguintes ajustes:
>
> 1. Em `src/ollama_client.py`, permita também o modelo `qwen2.5:3b` na lista de modelos suportados. Não remova os três modelos de avaliação existentes.
> 2. Em `src/llm_judge.py`, verifique se a resposta do juiz está vazia antes de tentar interpretar o JSON.
> 3. Valide se `correct` é realmente um booleano e se `reason` é uma string.
> 4. Mantenha o juiz utilizando `qwen2.5:3b`.
> 5. Não altere nenhum outro arquivo.
> 6. Ao terminar, mostre exatamente o que foi alterado e explique brevemente cada mudança.

### Resumo da resposta do Qwen

O Qwen informou que adicionou `qwen2.5:3b` à lista de modelos permitidos e apresentou verificações para resposta vazia, presença dos campos `correct` e `reason`, e seus tipos (`bool` e `str`).

Em seguida, diante de outro erro, recebeu este prompt:

> Corrija o erro de sintaxe em `src/llm_judge.py`.
>
> O erro está na construção de `judge_prompt`: uma f-string contém uma quebra de linha literal e não foi fechada corretamente.
>
> Use `\n` dentro da string ou divida o texto em strings válidas.
>
> Não altere nenhum outro arquivo. Preserve a lógica atual da classe `LLMJudge`, incluindo o uso do modelo `qwen2.5:3b`, a validação do JSON e o tratamento de erros.
>
> Ao terminar, mostre o arquivo completo corrigido.

O Qwen então apresentou uma versão com quebras `\n`, verificação de resposta vazia antes do `json.loads()` e validação dos tipos dos campos.

### Resultado e avaliação

As validações solicitadas foram incorporadas à versão apresentada. A correção de sintaxe também foi aplicada no código exibido. Ainda assim, a resposta do modelo não substitui a execução de testes específicos para JSON inválido, resposta vazia e tipos incorretos; esses cenários precisam ser verificados por testes próprios para que a robustez seja comprovada.

---

## 9. Geração do conjunto de 100 chamados sintéticos

**Objetivo:** ampliar a base de avaliação para 100 exemplos distribuídos entre as seis categorias.

### Prompt original

> Vamos retomar a tarefa de geração dos 100 casos de teste do nosso projeto.
>
> Você perdeu o contexto anterior. Releia as instruções abaixo e conclua a tarefa.
>
> **Objetivo:** criar `test_cases.csv` na raiz do projeto, contendo exatamente 100 chamados sintéticos de suporte de TI.
>
> **Colunas:** `input` e `expected`.
>
> **Categorias permitidas:** Hardware, Software, Rede, Acesso, Instalação e Configuração.
>
> **Distribuição:** 16 ou 17 casos por categoria, totalizando exatamente 100.
>
> **Preserve estes 10 exemplos originais:**
> 1. Estou sem rede. → Rede
> 2. Programa travou. → Software
> 3. Internet lenta. → Rede
> 4. Sem acesso a pasta. → Acesso
> 5. Não consigo entrar no computador. → Acesso
> 6. Preciso de um programa. → Instalação
> 7. Sem máquina nessa mesa. → Instalação
> 8. Monitor parou. → Hardware
> 9. Preciso que fique dessa forma. → Configuração
> 10. Preciso do meu computador no modo noturno. → Configuração
>
> Crie mais 90 mensagens realistas, distintas e sem ambiguidades.
>
> **Instruções de execução:**
> 1. Verifique se `generate_test_cases.py` já existe. Se não existir, crie-o.
> 2. Gere o CSV com Python.
> 3. Execute usando exatamente ` .\.venv\Scripts\python.exe generate_test_cases`

### Resumo da resposta do Qwen

O Qwen afirmou que `generate_test_cases.py` havia sido criado e mostrou o comando para executá-lo. Também descreveu como resultado esperado um CSV com 100 registros e distribuição de 16 ou 17 casos por categoria.

### Resultado e avaliação

A resposta registrada não apresentou a saída real da execução nem exibiu os 100 registros do CSV; apresentou o comando e os resultados esperados. Nas conversas posteriores, o usuário executou a geração e verificou o arquivo, informando 100 registros e as colunas `input` e `expected`. Portanto, a validação do conjunto deve ser atribuída à execução e conferência posteriores, não somente à declaração do Qwen.

---

## 10. Implementação do teste de regressão de prompts

**Objetivo:** comparar a acurácia do mesmo modelo usando um prompt original e outro propositalmente degradado.

### Prompt original

> Crie um novo arquivo chamado `src/regression_test.py` para implementar uma demonstração de teste de regressão no nosso projeto de avaliação de LLMs.
>
> Contexto:
> - O projeto avalia modelos de classificação de chamados de suporte de TI.
> - As categorias são: Hardware, Software, Rede, Acesso, Instalação e Configuração.
> - Os 100 casos de teste estão em `test_cases.csv`, na raiz do projeto.
> - A integração com Ollama está em `src/ollama_client.py`.
> - O modelo escolhido para o teste será `qwen2.5:1.5b`.
>
> Requisitos:
> 1. Ler 20 casos do arquivo `test_cases.csv`.
> 2. Executar o modelo com o prompt original, que exige uma categoria e proíbe explicações.
> 3. Executar os mesmos 20 casos novamente com um prompt propositalmente degradado, menos específico e menos restritivo.
> 4. Comparar as respostas com as categorias esperadas, ignorando maiúsculas/minúsculas e pontuação final.
> 5. Calcular a acurácia de cada versão.
> 6. Exibir a diferença de desempenho.
> 7. Salvar os resultados individuais em `regression_results.csv`.
>
> O CSV deve registrar: `input`, `expected`, `original_response`, `original_correct`, `degraded_response`, `degraded_correct`.
>
> **IMPORTANTE:**
> - Crie somente `src/regression_test.py`.
> - Não altere `model_comparison.py`, `ollama_client.py`, `llm_judge.py`, `test_cases.csv` ou qualquer outro arquivo.
> - Não execute o teste automaticamente.
> - Reutilize a classe `OllamaClient` existente.
> - Mantenha o código simples e compatível com Python 3.14.

### Resumo da resposta do Qwen

O Qwen apresentou um script que usava pandas para ler os casos, selecionar 20 exemplos, executar duas versões do prompt, calcular acurácia e salvar um CSV.

### Resultado e avaliação

O código apresentado não estava pronto para execução e precisou de ajustes posteriores. Em uma execução anterior do experimento, foram registrados 55% de acurácia com o prompt original (11/20) e 10% com o prompt degradado (2/20), uma diferença de 45 pontos percentuais. Em uma execução posterior, os resultados foram diferentes, e os valores dessa execução estão registrados em docs/Teste_regressao.md

---

## 11. Análise do cliente Ollama — resposta com apontamentos incorretos

**Objetivo:** solicitar uma revisão de comunicação HTTP, tratamento de erros, validação de modelos e confiabilidade.

### Prompt original

> Analise o arquivo `src/ollama_client.py` do projeto.
>
> Verifique:
> 1. Se a comunicação com a API do Ollama está implementada corretamente.
> 2. Se o tratamento de erros é adequado.
> 3. Se a validação dos modelos suportados funciona corretamente.
> 4. Se existem problemas de segurança ou confiabilidade.
>
> Não altere nenhum arquivo. Apenas analise o código e apresente:
> - Problemas encontrados.
> - Pontos que estão corretos.
> - Melhorias recomendadas, se houver.
>
> Explique de maneira simples, considerando que o projeto é acadêmico.

### Resumo da resposta do Qwen

O Qwen reconheceu o uso do endpoint `/api/generate`, o parâmetro `stream: False` e o tratamento de exceções de requisição. Entretanto, apontou como ausentes a verificação de status HTTP, o timeout e a validação de modelos suportados. Também recomendou adicionar `response.raise_for_status()`, configurar timeout e manter uma lista de modelos permitidos.

### Resultado e avaliação

Essa análise continha erros factuais em relação à versão do `src/ollama_client.py` que estávamos utilizando: o código já possuía `response.raise_for_status()`, `timeout=10` e uma lista de modelos suportados. Portanto, essas três recomendações foram apresentadas como se fossem correções necessárias, embora já estivessem implementadas. A resposta não foi aceita como diagnóstico confiável sem conferência do código-fonte.

O registro é importante porque demonstra que a IA pode produzir uma análise plausível, mas incorreta, mesmo quando o pedido é apenas revisar um código existente.

---

## 12. Análise dos testes — resposta insuficientemente fundamentada

**Objetivo:** avaliar o que os testes verificavam, a cobertura de falhas e a dependência do servidor Ollama.

### Prompt original

> Analise o arquivo `tests/test_ollama_client.py`.
>
> Verifique:
> 1. O que cada teste está verificando.
> 2. Se os testes cobrem os principais cenários de sucesso e falha.
> 3. Se existem situações importantes que não estão sendo testadas.
> 4. Se os testes dependem de um servidor Ollama em execução.
>
> Não modifique nenhum arquivo. Apresente os pontos positivos, limitações e melhorias recomendadas em linguagem simples, considerando o contexto acadêmico do projeto.

### Resumo da resposta do Qwen

O Qwen afirmou que o arquivo possuía um único teste principal e descreveu de forma hipotética o que esse teste provavelmente verificava. Em seguida, apontou lacunas como ausência de testes de conexão, timeout, modelo inexistente, resposta JSON inválida e uso de mocks.

### Resultado e avaliação

A resposta não apresentou uma análise concreta de cada teste: ela própria utilizou termos como “provavelmente” e “pode capturar”, indicando que estava inferindo parte do conteúdo. Nas conversas do projeto, a execução do `pytest` foi apresentada com **3 testes aprovados**, e o conjunto de testes incluía cenários de sucesso, modelo não suportado e erro de conexão. Assim, a afirmação de que havia apenas um teste não correspondia ao estado que estávamos validando.

As recomendações sobre ampliar cenários e usar mocks podem ser consideradas sugestões gerais, mas não devem ser confundidas com constatações comprovadas sobre o arquivo. A dependência de um servidor Ollama também precisaria ser verificada diretamente na implementação dos testes antes de ser afirmada.

---

## 13. Implementação do LLM Judge híbrido

**Arquivo alterado:** `src/llm_judge.py`

**Ferramenta utilizada:** ChatGPT Gratuito.

**Objetivo:** melhorar a avaliação das respostas dos modelos, combinando comparação direta em Python com avaliação por um modelo de linguagem.

### Solicitação realizada (síntese)

A solicitação consistiu em revisar e adaptar a implementação do LLM Judge para utilizar uma abordagem híbrida, seguindo os requisitos:

1. Normalizar a resposta produzida pelo modelo e a categoria esperada.
2. Comparar os dois valores diretamente em Python.
3. Quando houver correspondência exata após a normalização, considerar a resposta correta sem consultar outro modelo.
4. Quando não houver correspondência exata, encaminhar a avaliação ao modelo `qwen2.5:3b`.
5. Considerar a mensagem original, a categoria esperada e a resposta recebida durante a avaliação.
6. Retornar um resultado estruturado com os campos `correct` e `reason`.
7. Preservar o tratamento de erros e a validação do resultado retornado pelo juiz.

### Resumo da resposta da IA

Foi proposta uma implementação híbrida para a classe `LLMJudge`.

A comparação direta em Python ficou responsável por reconhecer respostas equivalentes após a normalização textual. Quando essa comparação não identifica uma correspondência, o código utiliza o modelo `qwen2.5:3b` para analisar a resposta.

Essa abordagem evita chamadas desnecessárias ao modelo juiz quando a resposta já corresponde à categoria esperada.

### Resultado e avaliação

A implementação foi aproveitada e incorporada ao projeto.

Foram realizados quatro testes manuais:

- Categoria correta com correspondência exata.
- Categoria correta com diferença entre letras maiúsculas e minúsculas.
- Categoria incorreta, exigindo avaliação do modelo juiz.
- Resposta que apenas repete a mensagem original, sem apresentar a categoria esperada.

Os quatro cenários apresentaram os resultados esperados durante a verificação manual.

**Decisão:** implementação aceita e utilizada no processo de avaliação. A abordagem híbrida foi mantida no projeto.

---

## 14. Ajuste do cálculo de calibração

**Arquivo alterado:** `eval/calibration.py`

**Ferramenta utilizada:** ChatGPT Gratuito.

**Objetivo:** adaptar o cálculo de calibração para comparar as avaliações humanas com os resultados do LLM Judge híbrido.

### Solicitação realizada (síntese)

A solicitação consistiu em revisar o script de calibração para utilizar os resultados atualizados do avaliador e calcular as métricas de concordância.

Foram definidos os seguintes requisitos:

1. Utilizar o arquivo `eval/results/human_review_*_calibrated.csv` permitindo selecionar o arquivo desejado durante a execução.
2. Comparar a avaliação humana com o resultado produzido pelo avaliador.
3. Calcular o percentual de concordância.
4. Calcular o Kappa de Cohen.
5. Identificar e apresentar os casos de discordância.
6. Evitar apresentar um valor de Kappa como válido quando não houver variabilidade suficiente nas avaliações para seu cálculo.

### Resumo da resposta da IA

Foi apresentada uma versão atualizada de `calibration.py`, com leitura do arquivo de avaliações humanas, comparação dos resultados e cálculo das métricas.

O script também foi organizado para apresentar o total de avaliações, concordâncias, discordâncias, percentual de concordância e Kappa de Cohen, além de listar eventuais divergências.

### Resultado e avaliação

A alteração foi incorporada e executada utilizando 30 registros de avaliação humana.

O resultado apresentado no terminal foi:

- Total de avaliações: 30.
- Concordâncias: 30.
- Discordâncias: 0.
- Concordância percentual: 100%.
- Kappa de Cohen: 1,0000.

Não foram encontradas discordâncias nessa execução.

**Decisão:** alteração aceita e executada com sucesso.

O resultado indica concordância perfeita dentro da amostra utilizada. Entretanto, existem limitações: os 30 registros representam apenas 10 situações distintas, repetidas entre os três modelos, e as correspondências exatas são resolvidas diretamente pelo Python, sem consulta ao LLM Judge.

Por isso, o resultado não deve ser interpretado como garantia de desempenho geral do avaliador.

### Interação X — Estruturação de Infraestrutura Docker e Backend Ollama
- **Prompt resumido:** Solicitei a estruturação do `Dockerfile`, `compose.yaml` e dos módulos Python (`ollama_client.py` e `avaliador.py`) para integrar o Ollama local ao painel Streamlit e exportar métricas em CSV.
- **Resumo da resposta:** A IA gerou a configuração multi-container com rede interna (`OLLAMA_HOST`), volumes persistentes e um cliente HTTP para coletar latência e tokens.
- **O que foi aceito/corrigido:** Aceita a arquitetura desacoplada e o contrato CSV. Corrigido o tratamento da variável `OLLAMA_HOST` para adicionar `http://` automaticamente quando executado fora do Docker no Windows.

## Pedido — Preparar uma nova comparação real de modelos sem sobrescrever resultados

### Solicitação integral

> Prepare eval/model_comparison.py para uma nova execução real,
> preservando os resultados anteriores.
>
> Requisitos:
> - Coloque a execução em main(), protegida por
>   if __name__ == "__main__". Importar o módulo não pode gerar
>   respostas, escrever arquivos ou iniciar a avaliação.
> - Adicione --output obrigatório para indicar um CSV novo.
>   Recuse um arquivo existente antes de qualquer inferência.
> - Preserve os três modelos, os 100 chamados, os prompts,
>   o critério de acerto e o uso atual do LLMJudge.
> - Antes da avaliação, confira a disponibilidade dos três
>   modelos e do juiz qwen2.5:3b. Se faltar algum, interrompa
>   com mensagem clara, sem iniciar a bateria.
> - Preserve as colunas consumidas pelo painel.
> - Grave os resultados progressivamente, sem perder os casos
>   concluídos se houver interrupção.
> - Registre falhas explicitamente; não apresente medições
>   ausentes como zero.
> - Mostre progresso por modelo e caso, com saída imediata.
> - Registre início/fim em UTC, endereço do Ollama,
>   identificação dos modelos, hash SHA256 do dataset, prompts
>   e parâmetros efetivamente enviados. Não invente parâmetros
>   ou medições. Salve os metadados ao lado do novo CSV.
> - Diferencie métricas da geração classificadora das chamadas
>   adicionais ao juiz.
>
> Adicione testes com respostas simuladas para importação sem
> efeitos, proteção contra sobrescrita, modelo ausente, gravação
> incremental e tratamento de falhas.
>
> Execute na .venv:
> .\.venv\Scripts\python.exe -m pytest -q tests/
>
> Confira git diff --check. Registre este pedido integralmente,
> decisões e resultados reais em PROMPTS.md.
>
> Não execute modelos nem altere resultados anteriores.
> Não faça commit ou push. Apresente o diff, a saída dos testes
> e git status --short.

### Decisões de implementação

- A execução ficou em `main()` e só é iniciada pelo ponto de entrada `if __name__ == "__main__"`. `--output` é obrigatório; o caminho CSV e o sidecar `<csv>.metadata.json` existentes são recusados antes de qualquer inferência.
- A conferência de disponibilidade usa `GET /api/tags` e exige os nomes exatos `qwen2.5:1.5b`, `llama3.2:3b`, `gemma3:1b` e `qwen2.5:3b`. Não baixa nem executa modelos na pré-verificação.
- Foram mantidos os três classificadores, 100 casos por classificador, o prompt de classificação, a comparação normalizada já existente e o `LLMJudge`. Permanecem todas as colunas antigas do CSV; as novas colunas identificam erros e métricas exclusivas do juiz.
- O CSV é criado em modo exclusivo e descarregado após cada caso. O sidecar registra o estado da execução e cada prompt/requisição, incluindo chamadas em andamento. Medições indisponíveis são gravadas em branco; a latência observada de uma tentativa com falha permanece registrada, enquanto tokens e duração Ollama ausentes não são convertidos em zero.
- Os metadados guardam horários UTC, URL do Ollama, identificação retornada para os modelos, SHA256 dos bytes do dataset, prompts efetivamente tentados e payload efetivamente usado. As chamadas classificadoras e adicionais do juiz são separadas; o payload não envia opções de amostragem.
- Não foram executadas inferências reais. A validação usa somente respostas e disponibilidades simuladas, sem alterar os CSVs históricos.

### Resultados reais da validação

- Comando executado: `.\.venv\Scripts\python.exe -m pytest -q tests/`
- Saída final: `35 passed, 16 subtests passed in 11.41s` (código de saída 0).
- `git diff --check`: código de saída 0, sem mensagens.
- Sintaxe Pylance: sem erros nos dois arquivos de implementação e nos dois arquivos de teste alterados. Diagnósticos Pylance de `eval/model_comparison.py`: nenhum.
- Nenhuma inferência real foi iniciada; os testes de execução usaram clientes/modelos simulados. Os CSVs históricos não foram editados.
- `git status --short`:
  ```text
   M PROMPTS.md
   M docs/documentacao-tecnica.md
   M eval/model_comparison.py
   M src/ollama_client.py
   M tests/test_ollama_client.py
  ?? tests/test_model_comparison.py
  ```

## Revisão — Corrigir falhas no sidecar e nos vereditos

### Solicitação integral

> Corrija os três problemas encontrados na revisão:
>
> 1. Em eval/model_comparison.py, só atualize/finalize o arquivo
>    de metadados depois que esta execução o criar com sucesso.
>    Se a criação exclusiva falhar porque o arquivo passou a existir,
>    preserve integralmente seu conteúdo e interrompa sem inferência.
>
> 2. Registre como falha de avaliação respostas do juiz vazias,
>    JSON inválido ou campos com tipos inválidos. Preencha judge_error
>    e diferencie ausência de veredito de um julgamento negativo válido.
>    Preserve a separação das métricas do classificador e do juiz.
>
> 3. Resposta vazia ou somente espaços do classificador deve preencher
>    model_error, marcar a chamada como falha e impedir consulta ao juiz.
>    Preserve as métricas efetivamente recebidas.
>
> Acrescente testes simulados para esses cenários. Para os erros de
> interpretação do juiz, exercite o LLMJudge real com transporte
> simulado, em vez de substituir toda a avaliação por FakeJudge.
>
> Preserve os demais requisitos e arquivos históricos.
> Atualize a documentação necessária e registre este pedido integral,
> as correções e os resultados reais em PROMPTS.md.
>
> Execute:
> .\.venv\Scripts\python.exe -m pytest -q tests/
> git diff --check
>
> Não execute modelos nem faça commit ou push.
> Apresente o diff das correções e a saída dos testes.

### Correções e decisões

- O executor só atualiza o sidecar após obter sucesso em `open("x")`. Se outra execução criar o sidecar durante a pré-verificação, preserva seus bytes e interrompe antes da inferência; o CSV vazio criado por esta tentativa é removido.
- `LLMJudge` continua retornando o mesmo formato existente, mas expõe `evaluation_error` para diferenciar resposta vazia, JSON inválido e esquema/tipos inválidos de uma avaliação negativa válida. O CSV deixa `judge_correct` em branco sem veredito; `false` é reservado a um julgamento negativo válido, e `judge_error` contém a falha. As métricas do juiz continuam separadas.
- Resposta do classificador vazia, só com espaços ou não textual agora registra `model_error`, marca a chamada como falha e impede a execução do juiz. Métricas que chegaram na resposta continuam registradas.
- Os testes de interpretação instanciam `LLMJudge` real e simulam `GET /api/tags` e `POST /api/generate`; não fazem inferência nem conexão real com Ollama.

### Resultados reais

- Comando executado: `.\.venv\Scripts\python.exe -m pytest -q tests/`
- Saída: `43 passed, 16 subtests passed in 8.33s` (código de saída 0).
- `git diff --check`: código de saída 0, sem mensagens.
- Pylance: sem erros de sintaxe em `src/llm_judge.py`; diagnósticos de `eval/model_comparison.py`: nenhum.
- Nenhum modelo foi executado; as chamadas HTTP dos testes foram simuladas. Os resultados históricos não foram alterados.
