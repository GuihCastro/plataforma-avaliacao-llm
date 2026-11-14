# Teste de Regressão de Prompt

## 1. Objetivo

O objetivo deste experimento foi verificar se uma alteração propositalmente negativa no prompt de classificação causaria uma redução no desempenho do modelo.

Para isso, foram comparados dois cenários: a utilização do prompt original e a utilização de um prompt degradado, que instrui o modelo a responder sempre com a categoria Hardware, independentemente da mensagem recebida.

## 2. Configuração do experimento

- **Modelo:** qwen2.5:1.5b
- **Quantidade de casos:** 20
- **Seleção da amostra:** aleatória com semente fixa (`42`), garantindo a reprodução da mesma seleção.
- **Categorias avaliadas:** Hardware, Software, Rede, Acesso, Instalação e Configuração.
- **Critério de acerto:** a resposta deve corresponder exatamente à categoria esperada, após normalização de texto.

Cada mensagem foi avaliada duas vezes, uma com cada versão do prompt, totalizando 40 solicitações ao modelo.

## 3. Prompts utilizados

### Prompt original

Classifique a mensagem de suporte de TI em exatamente uma destas categorias: Hardware, Software, Rede, Acesso, Instalação ou Configuração. Responda somente com o nome da categoria, sem explicações.

### Prompt degradado

Classifique a mensagem de suporte de TI. Independentemente do conteúdo da mensagem, responda sempre Hardware.

## 4. Resultados

| Métrica | Prompt original | Prompt degradado |
|---|---:|---:|
| Casos avaliados | 20 | 20 |
| Acertos | 9 | 3 |
| Erros | 11 | 17 |
| Acurácia | 45% | 15% |

A utilização do prompt degradado provocou uma queda de **30 pontos percentuais** na acurácia, em comparação com o prompt original.

## 5. Análise dos resultados

O prompt original apresentou desempenho superior ao prompt degradado, demonstrando que a qualidade das instruções influencia diretamente o resultado da classificação.

Entretanto, o desempenho de 45% do prompt original também evidencia limitações do modelo na identificação das categorias. Foram observados erros em mensagens relacionadas a instalação, acesso, hardware e software.

No cenário degradado, o modelo passou a responder frequentemente com Hardware, inclusive em situações nas quais outras categorias eram esperadas. Isso provocou uma redução significativa na quantidade de acertos.

## 6. Limitações

O experimento utilizou uma amostra de apenas 20 mensagens e um único modelo. Portanto, os resultados não permitem generalizar o desempenho para todos os modelos ou para todos os tipos de solicitações de suporte de TI.

Além disso, a avaliação considera apenas correspondências exatas entre a resposta e a categoria esperada, após normalização. Respostas explicativas, mesmo quando mencionam a categoria correta, são contabilizadas como incorretas.

## 7. Arquivo de resultados

Os resultados individuais das 20 mensagens estão armazenados em CSV, contendo:

- Mensagem original;
- Categoria esperada;
- Resposta com o prompt original;
- Resultado da avaliação original;
- Resposta com o prompt degradado;
- Resultado da avaliação degradada.

Esse arquivo permite consultar os casos individualmente e reproduzir a análise dos resultados.