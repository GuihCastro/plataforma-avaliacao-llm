# Registro de uso de IA na programação — Plataforma de Avaliação de LLMs

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