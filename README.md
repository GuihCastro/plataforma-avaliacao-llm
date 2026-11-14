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

O painel consulta avaliações no formato definido em [`docs/contrato-avaliacao.md`](docs/contrato-avaliacao.md) e abre com um exemplo sintético. Ele não executa modelos nem configura infraestrutura; categorias, métricas e rubrica permanecem sujeitas à validação da equipe.

Instale as dependências e inicie o painel:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run src\app.py
```

Para validar a leitura dos arquivos, a acurácia com falhas e as medições ausentes:

```powershell
.\.venv\Scripts\python.exe -m pytest
```
