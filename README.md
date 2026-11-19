# Tema 3: Plataforma de Avaluação de LLMs
**Curso:** EAD_PROINT_100.DD-ADS-PI-10-74.2026.74

**Disciplina:** Projeto Integrador

## Integrantes

| Nome | RA |
| --- | --- |
| Guilherme Henrique de Castro | 2409953 |
| Johnny Henrique Viudes | 2413104 |
| Hugo | 2411493 |
| Mateus | 2409692 |

Plataforma para avaliar modelos de linguagem e prompts na classificação de chamados de suporte em português. Projeto Integrador — Tema 3.

## Painel de resultados (T11)

O painel abre os [resultados salvos dos modelos](eval/results/results_100_metrics.csv). Compare acurácia, latência de geração e tokens, selecione um modelo e consulte o chamado, a resposta original e o parecer do juiz. A consulta funciona localmente, sem iniciar o Ollama.

Em **Fonte dos resultados**, você também pode abrir a demonstração sintética ou carregar um arquivo. O JSON segue o [contrato de avaliação](docs/contrato-avaliacao.md). O CSV usa UTF-8 e vírgulas, com as colunas obrigatórias `model`, `input`, `expected`, `response` e `correct` (true/false). A coluna opcional `prompt_version` separa os resultados por versão. No CSV histórico, essa informação aparece como ausente.

Instale as dependências e inicie o painel:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run src\app.py
```

Para verificar as leituras de CSV e JSON e os cálculos do painel:

```powershell
.\.venv\Scripts\python.exe -m pytest -q tests/test_app.py tests/test_results_csv.py
```
