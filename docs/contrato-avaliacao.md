# Contrato de avaliação (rascunho)

Este documento descreve os dados mínimos para registrar uma avaliação de modelos na classificação de chamados. É um rascunho para validação da equipe, não uma especificação aprovada.

## Fluxo da interface

1. Selecionar uma bateria de casos, um modelo e um prompt.
2. Executar a avaliação.
3. Acompanhar o estado da execução até sua conclusão, inclusive quando houver falhas.
4. Comparar os resultados das execuções.

## Dados registrados

Os campos abaixo são necessários. Valores que não puderem ser obtidos devem ser `null`, e não zero ou uma string vazia.

| Escopo | Nome | Tipo | Significado |
|---|---|---|---|
| Execução | `id` | string | Identificador único da execução. |
| Execução | `data` | string (data/hora ISO 8601) | Momento em que a execução foi iniciada. |
| Execução | `estado` | string | Estado geral, incluindo conclusão com falhas quando aplicável. |
| Execução | `bateria` | objeto `{id, versao}` | Bateria de casos utilizada e sua versão. |
| Execução | `modelo` | objeto `{id, versao}` | Modelo avaliado e sua versão. |
| Execução | `prompt` | objeto `{id, versao}` | Prompt utilizado e sua versão. |
| Execução | `parametros` | objeto | Parâmetros enviados ao modelo, como temperatura e limite de tokens. |
| Execução | `juiz` | objeto `{id, versao}` | Identificação e versão do juiz de IA calibrado contra avaliações humanas, requisito do Tema 3. |
| Caso | `id` | string | Identificador do caso na bateria. |
| Caso | `chamado` | string | Texto do chamado submetido à classificação. |
| Caso | `categoria_esperada` | string | Categoria de referência do caso. |
| Caso | `resposta_original` | string ou `null` | Resposta bruta do modelo, antes de interpretação ou normalização. O formato proposto é um JSON com `categoria` e `justificativa`, ainda sujeito à validação na T05. |
| Caso | `categoria_prevista` | string ou `null` | Categoria extraída da resposta do modelo. |
| Caso | `justificativa` | string ou `null` | Justificativa produzida para a classificação, se disponível. |
| Caso | `acerto` | boolean | Indica se a categoria prevista corresponde à esperada; falhas e respostas inválidas contam como `false`. |
| Caso | `nota_juiz` | número ou `null` | Nota atribuída pelo juiz conforme a rubrica validada. |
| Caso | `tempo_ms` | inteiro ou `null` | Tempo medido para processar o caso, em milissegundos. |
| Caso | `tokens_entrada` | inteiro ou `null` | Tokens de entrada contabilizados. |
| Caso | `tokens_saida` | inteiro ou `null` | Tokens de saída contabilizados. |
| Caso | `erro` | objeto `{codigo, mensagem}` ou `null` | Falha ocorrida no caso; `null` quando não houve erro. |

Cada caso pertence a uma execução e deve permanecer registrado mesmo se houver falha, resposta inválida ou timeout. Esses casos também entram no total usado para calcular a acurácia; portanto, uma falha sem categoria prevista conta como caso incorreto, não como caso ausente.

Como proposta para validação na T05, a resposta do modelo deve ser um JSON com esta estrutura:

```json
{
  "categoria": "categoria_proposta",
  "justificativa": "Justificativa da classificação."
}
```

`null` significa que o valor não está disponível ou não foi medido. Não significa zero: por exemplo, tokens não contabilizados devem ser `null`, e não `0`. O zero só deve ser usado quando uma medição válida resultar efetivamente em zero.

## Pendências para validação da equipe

- **Categorias:** nomes, conjunto permitido e se a classificação admite uma ou mais categorias — validar com Hugo na T05. Qualquer categoria usada neste rascunho é apenas ilustrativa.
- **Métricas:** confirmar a definição da acurácia e quais outras métricas devem ser calculadas e comparadas — validar com Hugo na T05. A regra de inclusão das falhas no total acima é parte deste rascunho.
- **Juiz:** escolher o juiz de IA, definir sua versão, escala de notas e rubrica de avaliação com Hugo — validar na T05. O uso de um juiz de IA calibrado contra avaliações humanas é requisito do Tema 3.
- **Formato da resposta:** validar na T05 a proposta de JSON com `categoria` e `justificativa`.
- **Estados e formato dos erros:** confirmar os valores padronizados para estado da execução e códigos de erro.
