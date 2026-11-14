# Guia de instalação e execução do projeto

Este documento apresenta os requisitos, as instruções de instalação e os procedimentos necessários para preparar o ambiente e executar os testes da plataforma de avaliação de LLMs.

## 1. Requisitos do sistema

Antes de começar, verifique se o computador possui:

- Windows 10 ou Windows 11
- Conexão com a internet
- Espaço em disco suficiente para instalar os modelos de IA
- Memória RAM compatível com a execução dos modelos escolhidos (8GB é o mínimo)

As ferramentas necessárias são:

| Ferramenta | Finalidade |
|---|---|
| Python 3.12 ou superior | Execução do projeto sem Docker |
| Ollama | Execução local dos modelos de linguagem |
| Docker Desktop | Criação do ambiente isolado |
| Git (opcional) | Obtenção e atualização do repositório |
| VS Code (opcional) | Edição e visualização dos arquivos |

## 2. Instalação das ferramentas

### 2.1. Python

Acesse o site oficial:

https://www.python.org/downloads/

Baixe e instale o Python 3.12 ou superior.

Durante a instalação no Windows, marque a opção **Add Python to PATH**, quando disponível.

Após a instalação, abra o PowerShell e verifique:

```powershell
python --version
```

O terminal deverá apresentar a versão instalada.

Também é possível verificar o gerenciador de pacotes:

```powershell
python -m pip --version
```

### 2.2. Ollama

Acesse:

https://ollama.com/download

Baixe e instale a versão correspondente ao sistema operacional.

Após a instalação, abra o PowerShell e execute:

```powershell
ollama --version
```

O Ollama é responsável por executar localmente os modelos de linguagem utilizados pelo projeto.

### 2.3. Docker Desktop

Acesse:

https://www.docker.com/products/docker-desktop/

Baixe e instale o Docker Desktop para Windows.

Durante a configuração, utilize o mecanismo baseado em WSL 2, quando disponível. Caso necessário, siga as instruções oficiais de instalação do WSL.

Após a instalação, abra o Docker Desktop e aguarde o Docker Engine iniciar.

Verifique no PowerShell:

```powershell
docker --version
docker compose version
```

Para verificar se o Docker está funcionando, execute:

```powershell
docker run --rm hello-world
```

A mensagem "Hello from Docker!" indica que o teste básico do Docker foi concluído.

### 2.4. Git (opcional)

O Git pode ser instalado pelo site:

https://git-scm.com/downloads

Ele permite clonar o repositório e obter atualizações do projeto.

## 3. Obtenção do projeto

Obtenha os arquivos do repositório disponibilizado pelo grupo, por meio de clonagem ou download.

Caso utilize Git, abra o PowerShell na pasta em que deseja armazenar o projeto e execute:

```powershell
git clone URL_DO_REPOSITORIO
```

Substitua `URL_DO_REPOSITORIO` pelo endereço real do repositório.

Entre na pasta do projeto:

```powershell
cd plataforma-avaliacao-llm
```

Os comandos seguintes devem ser executados a partir da raiz do projeto.

## 4. Preparação dos modelos de IA

O projeto utiliza os seguintes modelos:

| Modelo | Utilização |
|---|---|
| qwen2.5:1.5b | Comparação de modelos |
| llama3.2:3b | Comparação de modelos |
| gemma3:1b | Comparação de modelos |
| qwen2.5:3b | Avaliação pelo LLM Judge |

Para baixar os modelos, execute individualmente:

```powershell
ollama pull qwen2.5:1.5b
ollama pull llama3.2:3b
ollama pull gemma3:1b
ollama pull qwen2.5:3b
```

Os downloads podem levar algum tempo, dependendo da conexão com a internet.

Confira se todos os modelos foram instalados:

```powershell
ollama list
```

### 4.1. Verificação do serviço

O Ollama precisa estar em execução durante os testes que realizam chamadas aos modelos.

Para verificar se a API está respondendo, execute:

```powershell
Invoke-RestMethod http://localhost:11434/api/tags
```

Se o serviço não estiver iniciado, abra o aplicativo Ollama. Caso necessário, inicie-o pelo terminal:

```powershell
ollama serve
```

Não é necessário executar esse comando se o serviço já estiver ativo.

## 5. Execução utilizando Docker (recomendado)

O Docker permite executar os testes em um ambiente isolado, sem precisar instalar as dependências Python diretamente no ambiente principal do computador.

O projeto utiliza uma imagem Python própria, definida no arquivo `Dockerfile`, e instala as dependências declaradas em `requirements.txt`.

### 5.1. Construir a imagem

Com o Docker Desktop e o Ollama em execução, abra o terminal na raiz do projeto e execute:

```powershell
docker compose build
```

Na primeira execução, o Docker precisará baixar a imagem base do Python e instalar as dependências.

### 5.2. Executar os testes automatizados

Execute:

```powershell
docker compose run --rm testes
```

O comando cria um contêiner temporário, executa os testes automatizados e remove o contêiner ao finalizar.

O resultado esperado é a aprovação dos três testes de `tests/test_ollama_client.py`.

### 5.3. Comunicação com o Ollama

O contêiner utiliza o endereço `http://host.docker.internal:11434` para acessar o Ollama instalado no computador hospedeiro.

Essa configuração está definida no arquivo `compose.yaml`.

Portanto, mesmo utilizando Docker, é necessário manter o Ollama e os modelos instalados no computador hospedeiro.

## 6. Execução diretamente pelo Python (sem Docker)

Também é possível executar os testes sem utilizar Docker.

Nesse caso, é necessário ter o Python e o Ollama instalados no computador.

### 6.1. Criar um ambiente virtual

Na raiz do projeto, execute:

```powershell
python -m venv .venv
```

O ambiente virtual mantém as dependências do projeto separadas das demais instalações Python do computador.

### 6.2. Ativar o ambiente virtual

No PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Caso o PowerShell bloqueie a ativação por política de execução, consulte as orientações oficiais do Python ou do PowerShell para habilitar a execução de scripts no ambiente do usuário.

### 6.3. Instalar as dependências

Com o ambiente virtual ativado, execute:

```powershell
python -m pip install -r requirements.txt
```

Esse comando instala as bibliotecas declaradas no arquivo `requirements.txt`, incluindo `requests` e `pytest`.

### 6.4. Executar os testes

Execute:

```powershell
python -m pytest -v
```

O resultado esperado é a aprovação dos três testes automatizados.

## 7. Solução de problemas

### Docker não consegue iniciar

Verifique se o Docker Desktop está aberto e se o Docker Engine terminou de inicializar.

### Ollama não responde

Verifique se o aplicativo está em execução e se a API está disponível na porta 11434.

### Modelo não encontrado

Execute:

```powershell
ollama list
```

Se o modelo necessário não aparecer, faça o download utilizando `ollama pull` e o nome correspondente.

### Docker informa que não encontrou o pytest

Reconstrua a imagem para incorporar as dependências atualizadas:

```powershell
docker compose build --no-cache
```

Depois execute novamente:

```powershell
docker compose run --rm testes
```

### Falha na conexão com o Ollama dentro do Docker

Confira se o Ollama está em execução no computador hospedeiro e se o endereço configurado em `compose.yaml` está correto.

## 8. Observações importantes

- O Docker automatiza a preparação do ambiente Python, mas não instala automaticamente o Ollama nem os modelos de IA.
- Os modelos precisam ser baixados separadamente e ocupam espaço em disco.
- A primeira construção da imagem Docker exige conexão com a internet.
- Os testes automatizados verificam funcionalidades do cliente Ollama; sua aprovação não representa, por si só, a aprovação de todos os experimentos e avaliações do projeto.
- O desempenho e o tempo de execução dos modelos dependem das características do computador utilizado.
- O ambiente Docker deste projeto utiliza Python 3.12, enquanto a execução local pode utilizar outra versão compatível.