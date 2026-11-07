# Registro de interações com IA

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
