# Guia rápido do repositório

Projeto Integrador Tema 3

**Repositório:** [GuihCastro/plataforma-avaliacao-llm](https://github.com/GuihCastro/plataforma-avaliacao-llm)

**Regra do grupo:** a `main` é a versão principal. Trabalhe em uma branch por tarefa e envie as alterações para revisão.

**Antes de usar:** convite aceito, Git configurado e branch `main` criada. Os comandos abaixo usam uma atualização do README como exemplo; adapte os nomes à sua tarefa.

## 1 Baixe o projeto uma vez

No terminal, dentro da pasta onde deseja guardar o projeto:

```bash
git clone https://github.com/GuihCastro/plataforma-avaliacao-llm.git
cd plataforma-avaliacao-llm
```

## 2 Comece cada tarefa em uma branch

Marque a tarefa como **Em andamento** no Notion. Atualize a `main` e crie sua branch, um espaço separado para trabalhar:

```bash
git switch main
git pull --ff-only
git switch -c docs/readme-guilherme
```

## 3 Desenvolva com IA e teste

Revise o código gerado e execute os testes do projeto. Você deve conseguir explicar o que entregou. Registre as interações relevantes em `PROMPTS.md`: prompt, resumo da resposta, decisão e motivo.

## 4 Salve e envie as alterações

Execute uma linha por vez e confira os arquivos antes de salvar. O commit registra as alterações no computador; o push envia sua branch ao GitHub.

```bash
git status
git diff
git add README.md
git commit -m "docs: atualiza README"
git push -u origin HEAD
```

## 5 Peça revisão e conclua

No GitHub, abra **Pull requests > New pull request**. Selecione **base: main** e **compare: sua branch**. O PR é o pedido de revisão: informe a tarefa, o que mudou e como testou.

Outro integrante revisa. Faça **merge** (juntar à `main`) somente com pelo menos **uma aprovação** e **CI verde** (testes automáticos no GitHub). Depois, marque a tarefa como **Concluído** no Notion.

**Sempre:** nenhuma alteração direta na `main`; ninguém aprova o próprio PR. Mantenha `.env` no `.gitignore`. Não envie senhas, chaves ou dados pessoais reais.

Referência: [GitHub Flow](https://docs.github.com/pt/get-started/using-github/github-flow).
