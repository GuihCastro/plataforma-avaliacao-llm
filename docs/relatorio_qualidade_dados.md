# Relatório de Análise de Qualidade dos Dados

**Projeto:** Plataforma de Avaliação de LLMs e Agentes  
**Área:** Dados e Qualidade  
**Responsável pela análise:** Johnny Henrique Viudes  
**Data:** 17/11/2026

## 1. Objetivo

Realizar uma análise inicial do conjunto de dados utilizado na classificação de chamados de suporte em português, verificando sua organização, integridade e consistência das categorias.

## 2. Arquivo analisado

`eval/datasets/test_cases.csv`

O arquivo contém duas colunas:

- `input`: descrição do chamado de suporte.
- `expected`: categoria esperada para o chamado.

## 3. Verificações realizadas

Foram realizadas verificações utilizando comandos do terminal e scripts Python, sem modificar o arquivo original.

| Verificação | Resultado |
|---|---:|
| Total de casos de teste | 100 |
| Campos vazios | 0 |
| Chamados duplicados | 0 |
| Categorias inesperadas | 0 |
| Categorias identificadas | 6 |

## 4. Distribuição das categorias

| Categoria | Quantidade |
|---|---:|
| Hardware | 17 |
| Software | 17 |
| Rede | 17 |
| Acesso | 17 |
| Instalação | 16 |
| Configuração | 16 |
| **Total** | **100** |

A distribuição está equilibrada, com uma diferença máxima de apenas um registro entre as categorias.

## 5. Pontos identificados para revisão humana

Durante a inspeção dos exemplos, foram identificados alguns chamados que podem gerar dúvidas na classificação:

| Linha | Chamado | Categoria atual | Observação |
|---|---|---|---|
| 70 | Preciso de um programa. | Instalação | Texto genérico, sem indicar claramente o que precisa ser feito. |
| 71 | Sem máquina nessa mesa. | Instalação | Pode representar uma solicitação de disponibilização de equipamento. |
| 86 | Preciso que fique dessa forma. | Configuração | Falta contexto para identificar a necessidade. |
| 98 | Preciso configurar a conexão Wi-Fi com a rede corporativa. | Configuração | Pode gerar confusão com a categoria Rede. |

Esses registros não foram alterados. Recomenda-se uma revisão humana para confirmar se as categorias estão adequadas.

## 6. Recomendações

- Revisar os chamados genéricos ou com pouco contexto.
- Avaliar possíveis ambiguidades entre as categorias Rede e Configuração.
- Considerar a inclusão de exemplos mais complexos e variados.
- Garantir que os casos de teste representem situações reais de suporte técnico.
- Validar a classificação esperada com a equipe antes de realizar alterações na base.

## 7. Conclusão

A análise inicial identificou que o conjunto de dados possui 100 casos de teste, distribuídos de forma equilibrada entre seis categorias.

Não foram encontrados campos vazios, chamados duplicados ou categorias fora do padrão definido.

Apesar dos bons resultados estruturais, alguns exemplos precisam de revisão humana para garantir que as classificações representem corretamente os problemas descritos.

Esta análise contribui para melhorar a confiabilidade dos dados utilizados na avaliação e comparação dos modelos de linguagem (LLMs).

**Observação:** esta etapa avaliou a integridade e a consistência estrutural dos dados, não a precisão de todas as classificações esperadas.
