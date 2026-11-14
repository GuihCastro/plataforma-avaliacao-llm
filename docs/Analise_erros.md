# Análise de Erros dos Modelos

## 1. Objetivo

Esta análise apresenta exemplos de classificações incorretas identificadas durante a avaliação dos modelos de linguagem utilizados na plataforma.

Foram selecionados quatro casos de falha, envolvendo dois modelos diferentes.

## 2. Casos analisados

### Caso 1 — Qwen 2.5 1.5B

- Mensagem: "A webcam não liga quando conecto ao computador."
- Categoria esperada: Hardware
- Resposta obtida: Instalação
- Resultado: Incorreto.

**Análise:** O modelo classificou um problema de funcionamento de um periférico como instalação. A mensagem descreve uma falha em um equipamento físico, portanto a categoria adequada é Hardware.

### Caso 2 — Qwen 2.5 1.5B

- Mensagem: "A tela do monitor está com uma faixa preta."
- Categoria esperada: Hardware
- Resposta obtida: Instalação
- Resultado: Incorreto.

**Análise:** O modelo não reconheceu adequadamente um possível defeito físico no monitor. A resposta indica confusão entre problemas de hardware e instalação.

### Caso 3 — Llama 3.2 3B

- Mensagem: "A conexão cabeada está desconectando sozinha."
- Categoria esperada: Rede
- Resposta obtida: Acesso
- Resultado: Incorreto.

**Análise:** O modelo confundiu uma instabilidade de conexão de rede com um problema de acesso. A mensagem descreve uma falha na conectividade, não uma dificuldade de autenticação ou permissão.

### Caso 4 — Llama 3.2 3B

- Mensagem: "O Wi-Fi corporativo não aparece na lista de redes disponíveis."
- Categoria esperada: Rede
- Resposta obtida: Configuração.
- Resultado: Incorreto.

**Análise:** O modelo classificou a indisponibilidade de uma rede sem fio como configuração. Embora configurações possam influenciar a conexão, a categoria definida para esse chamado no conjunto de testes é Rede.

## 3. Padrões identificados

Nos exemplos analisados, foram observadas dificuldades de distinção entre categorias próximas:

- **Hardware e Instalação:** o Qwen confundiu falhas de funcionamento de equipamentos com problemas de instalação.
- **Rede e Acesso:** o Llama interpretou problemas de conectividade como dificuldades de acesso.
- **Rede e Configuração:** o Llama confundiu a indisponibilidade de uma rede sem fio com uma questão de configuração.

Esses resultados demonstram que os modelos podem apresentar dificuldades mesmo em chamados relativamente objetivos, especialmente quando diferentes categorias possuem conceitos relacionados.

## 4. Limitações da análise

Os quatro casos apresentados são exemplos selecionados de falhas e não representam, isoladamente, o comportamento completo dos modelos.

A análise considera as categorias esperadas definidas no conjunto de testes e as respostas efetivamente registradas durante a execução.

## 5. Conclusão

A análise evidencia a importância de avaliar modelos de linguagem com conjuntos variados de chamados e categorias bem definidas.

Os erros observados podem orientar melhorias futuras nos prompts, nas instruções de classificação e nos próprios conjuntos de testes.