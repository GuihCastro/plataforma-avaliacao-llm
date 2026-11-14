import csv
from pathlib import Path
from collections import Counter

cases = {
    "Hardware": [
        "Monitor parou.",
        "Meu teclado não funciona.",
        "O mouse não está respondendo aos movimentos.",
        "A tela do notebook está piscando constantemente.",
        "O computador não liga quando aperto o botão.",
        "A impressora está puxando várias folhas de uma vez.",
        "O headset não reproduz som em nenhum aplicativo.",
        "Uma das portas USB não reconhece o pendrive.",
        "O carregador do notebook está com o cabo danificado.",
        "A webcam não liga quando conecto ao computador.",
        "A tela do monitor está com uma faixa preta.",
        "O notebook está superaquecendo e desligando sozinho.",
        "A bateria do notebook não segura carga.",
        "Algumas teclas do teclado estão fisicamente quebradas.",
        "O computador está emitindo um ruído forte na ventoinha.",
        "O conector do cabo de vídeo está quebrado.",
        "O scanner não liga quando pressiono o botão."
    ],
    "Software": [
        "Programa travou.",
        "O sistema fecha sozinho ao abrir.",
        "O navegador apresenta erro ao iniciar.",
        "O aplicativo de folha de pagamento parou de responder.",
        "O Word fecha quando tento salvar o documento.",
        "O programa exibe uma mensagem de erro ao executar.",
        "O sistema apresenta falha ao carregar os relatórios.",
        "O aplicativo não abre depois da atualização.",
        "O programa apresenta falha ao exportar um arquivo PDF.",
        "O sistema duplicou os registros ao salvar.",
        "O navegador não carrega as extensões instaladas.",
        "O antivírus exibe um erro durante a verificação.",
        "O aplicativo apresenta uma tela branca ao iniciar.",
        "O programa não reconhece o arquivo que tento importar.",
        "O sistema apaga os filtros depois que fecho a tela.",
        "O leitor de PDF fecha ao abrir determinados arquivos.",
        "A planilha apresenta erro ao executar uma fórmula."
    ],
    "Rede": [
        "Estou sem rede.",
        "Internet lenta.",
        "Não consigo acessar nenhum site mesmo conectado ao Wi-Fi.",
        "A conexão Wi-Fi cai várias vezes durante o expediente.",
        "O computador não recebe um endereço IP da rede.",
        "O cabo de rede não está conectando à internet.",
        "A rede da empresa está indisponível em todos os computadores.",
        "Não consigo alcançar o servidor pelo endereço IP.",
        "A videoconferência trava por causa da instabilidade da conexão.",
        "A conexão cabeada está desconectando sozinha.",
        "O Wi-Fi corporativo não aparece na lista de redes disponíveis.",
        "A impressora de rede está indisponível para todos os computadores.",
        "A intranet está fora do ar para todos os funcionários.",
        "A conexão com o servidor apresenta perda de pacotes.",
        "O computador está conectado ao Wi-Fi, mas sem acesso à internet.",
        "A VPN desconecta continuamente durante o uso.",
        "A transferência de arquivos pela rede está muito lenta."
    ],
    "Acesso": [
        "Sem acesso a pasta.",
        "Não consigo entrar no computador.",
        "Não consigo fazer login no sistema com minha conta.",
        "Minha senha corporativa foi bloqueada após várias tentativas.",
        "Preciso recuperar o acesso ao meu e-mail institucional.",
        "Minha conta não consegue entrar no portal interno.",
        "Aparece usuário sem permissão ao abrir o sistema.",
        "Meu crachá não libera meu acesso ao sistema de ponto.",
        "Não consigo acessar a pasta compartilhada do meu departamento.",
        "Preciso liberar acesso ao módulo financeiro para meu usuário.",
        "Minha conta foi desativada e não consigo autenticar.",
        "O sistema não aceita a senha da minha conta.",
        "Não consigo entrar no painel administrativo com meu usuário.",
        "Preciso redefinir minha senha de rede.",
        "O acesso ao sistema foi negado para minha matrícula.",
        "Meu usuário não tem permissão para visualizar os relatórios.",
        "O login no e-mail retorna uma mensagem de credenciais inválidas."
    ],
    "Instalação": [
        "Preciso de um programa.",
        "Sem máquina nessa mesa.",
        "Preciso instalar o Microsoft Teams neste computador.",
        "Solicito a instalação do pacote de escritório.",
        "Preciso adicionar uma impressora nova ao meu computador.",
        "Instalem o leitor de PDF na minha estação.",
        "Preciso instalar o certificado digital neste computador.",
        "Quero instalar o aplicativo de videoconferência.",
        "Solicito a instalação do cliente VPN.",
        "A nova estação precisa receber o sistema operacional.",
        "Preciso instalar os drivers da impressora.",
        "Solicito a instalação do navegador Firefox.",
        "Preciso instalar o aplicativo de acesso remoto.",
        "Instalem o software de desenho nesta máquina.",
        "Preciso adicionar o agente de antivírus no notebook.",
        "Solicito a instalação do driver do scanner."
    ],
    "Configuração": [
        "Preciso que fique dessa forma.",
        "Preciso do meu computador no modo noturno.",
        "Quero alterar a resolução do monitor para 1920x1080.",
        "Preciso configurar a assinatura automática do e-mail.",
        "Quero mudar o idioma do sistema para português.",
        "Configure o navegador para abrir a página da intranet ao iniciar.",
        "Preciso ajustar o fuso horário do computador.",
        "Quero alterar o tempo para a tela bloquear automaticamente.",
        "Configure a impressora para imprimir frente e verso por padrão.",
        "Preciso mapear a unidade de rede Z: no meu computador.",
        "Quero definir o aplicativo de PDF como programa padrão.",
        "Ajuste o brilho da tela para um nível menor.",
        "Preciso configurar a conexão Wi-Fi com a rede corporativa.",
        "Quero mudar o formato de data do sistema para dd/mm/aaaa.",
        "Configure meu e-mail para atualizar a cada cinco minutos.",
        "Preciso deixar a escala da tela em 125%."
    ]
}

rows = [
    {"input": message, "expected": category}
    for category, messages in cases.items()
    for message in messages
]

output = Path(__file__).resolve().parent / "datasets" / "test_cases.csv"

with open(output, "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=["input", "expected"])
    writer.writeheader()
    writer.writerows(rows)

# Validar o arquivo criado
with open(output, newline="", encoding="utf-8") as file:
    saved_rows = list(csv.DictReader(file))

counts = Counter(row["expected"] for row in saved_rows)

assert len(saved_rows) == 100, f"Esperados 100 registros, encontrados {len(saved_rows)}"
assert len(set(row["input"] for row in saved_rows)) == 100, "Existem mensagens duplicadas"
assert all(row["expected"] in cases for row in saved_rows), "Categoria inválida"
assert all(16 <= counts[category] <= 17 for category in cases), "Distribuição incorreta"

print("\n--- VALIDAÇÃO DOS CASOS DE TESTE ---")
print("Total de registros:", len(saved_rows))
print("Mensagens duplicadas: 0")
print("\nQuantidade por categoria:")

for category, quantity in counts.items():
    print(f"{category}: {quantity}")

print("\nCSV criado e validado em:", output)
