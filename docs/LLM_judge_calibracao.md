# Calibração do LLM Judge

## 1. Objetivo

A calibração do LLM Judge tem como objetivo verificar se o avaliador automático consegue julgar corretamente as classificações produzidas pelos modelos, comparando suas avaliações com aquelas realizadas por humanos.

Essa etapa permite analisar o nível de concordância entre a avaliação automática e a avaliação humana.

## 2. Implementação

O projeto utiliza uma abordagem híbrida para avaliar as respostas:

- Quando a resposta normalizada corresponde exatamente à categoria esperada, a validação é realizada diretamente pelo Python.
- Quando não existe correspondência exata, a avaliação é encaminhada ao modelo Qwen2.5:3b, utilizado como LLM Judge.
- O avaliador considera a mensagem original, a categoria esperada e a resposta produzida.

A normalização textual remove diferenças de maiúsculas e minúsculas, espaços excedentes e pontuação final.

## 3. Avaliação humana

Foi utilizado um conjunto de 30 avaliações humanas, armazenadas no arquivo:

`eval/results/human_review_30_calibrated.csv`

As avaliações humanas foram comparadas com os resultados produzidos pelo avaliador híbrido.

Distribuição das avaliações humanas:

- Avaliações positivas: 7
- Avaliações negativas: 23
- Total: 30

## 4. Resultados da calibração

A execução do script de calibração apresentou os seguintes resultados:

- Total de avaliações: 30
- Concordâncias entre o avaliador e a revisão humana: 30
- Discordâncias: 0
- Concordância percentual: 100%
- Kappa de Cohen: 1,0000

Não foram identificadas discordâncias entre as avaliações analisadas.

## 5. Interpretação

O percentual de concordância foi calculado pela proporção de avaliações em que o resultado automático coincidiu com a avaliação humana.

O Kappa de Cohen também foi utilizado para medir a concordância, considerando a concordância esperada ao acaso.

O valor de 1,0000 indica concordância perfeita entre as duas avaliações no conjunto analisado.

Esse resultado demonstra que, nas avaliações realizadas, o avaliador híbrido apresentou os mesmos resultados da revisão humana.

## 6. Limitações

Apesar do resultado de concordância total, existem limitações importantes:

- O conjunto contém 30 registros, mas representa apenas 10 situações distintas, repetidas entre os três modelos.
- Parte das avaliações é resolvida diretamente pelo Python por correspondência exata, sem consulta ao LLM Judge.
- O resultado não garante que o avaliador terá o mesmo desempenho em outros conjuntos de dados.
- A qualidade da calibração depende da consistência das avaliações humanas e da definição das categorias.

Portanto, o resultado deve ser interpretado como uma concordância perfeita no conjunto avaliado, e não como garantia de precisão geral do avaliador.

## 7. Reprodutibilidade

A calibração pode ser executada utilizando:

`python -m eval.calibration`

O arquivo utilizado como referência nesta avaliação é:

`eval/results/human_review_30_calibrated.csv`

A implementação do avaliador está em:

`src/llm_judge.py`

O cálculo das métricas está em:

`eval/calibration.py`

## 8. Conclusão

A calibração permitiu comparar o avaliador automático com avaliações humanas e medir a concordância entre eles.

O resultado de 100% de concordância e Kappa de Cohen igual a 1,0000 foi obtido no conjunto de 30 avaliações utilizado.

As limitações identificadas devem ser consideradas em futuras avaliações, principalmente a quantidade reduzida de situações distintas e o uso de correspondência exata pelo Python.