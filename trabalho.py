import pandas as pd
import re
import matplotlib.pyplot as plt


def parse_line(line):
    pattern = r'(\[\d{1,2}/\d{1,2}/\d{2,4}, \d{1,2}:\d{2}(?::\d{2})?\]) (.*?): (.*)'
    match = re.match(pattern, line)

    if match:
        data_hora = match.group(1)
        remetente = match.group(2)
        mensagem = match.group(3)
        data_hora = data_hora[1:-1]  # Remove os colchetes []
        data, hora = data_hora.split(', ')
        return data, hora, remetente, mensagem
    return None


def ler_arquivo(filename):
    messages = []
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            parsed = parse_line(line)
            if parsed:
                messages.append(parsed)

    df = pd.DataFrame(messages, columns=['data', 'hora', 'remetente', 'mensagem'])
    return df


def resumo_conversas(df):
    resumo = df['remetente'].value_counts().reset_index()
    resumo.columns = ['Remetente', 'Mensagens']
    return resumo


def historico_remetente(df, remetente):
    return df[df['remetente'] == remetente]


def grafico_historico_remetente(df, remetente):
    df_remetente = df[df['remetente'] == remetente].copy()

    df_remetente['data'] = pd.to_datetime(df_remetente['data'], errors='coerce')

    # Remover valores nulos gerados durante a conversão
    df_remetente = df_remetente.dropna(subset=['data'])

    # Agrupar as mensagens por dia
    df_historico = df_remetente.groupby(df_remetente['data'].dt.date).size()

    # Gerar o gráfico
    df_historico.plot(kind='bar')
    plt.title(f'Histórico de mensagens de {remetente}')
    plt.xlabel('Data')
    plt.ylabel('Quantidade de Mensagens')
    plt.show()


def grafico_pizza(df):
    resumo = df['remetente'].value_counts()
    resumo.plot.pie(autopct='%1.1f%%', startangle=90)
    plt.title('Distribuição de mensagens por remetente')
    plt.ylabel('')
    plt.show()


def grafico_linhas(df):

    df['data'] = pd.to_datetime(df['data'], errors='coerce')

    df = df.dropna(subset=['data'])

    # Agrupar as mensagens por data e remetente
    df_contagem = df.groupby([df['data'].dt.date, 'remetente']).size().unstack(fill_value=0)

    # Gerar o gráfico
    df_contagem.plot(kind='line', marker='o')
    plt.title('Quantidade de mensagens ao longo do tempo por remetente')
    plt.xlabel('Data')
    plt.ylabel('Quantidade de Mensagens')
    plt.legend(title='Remetente')
    plt.show()


# Main
if __name__ == "__main__":
    arquivo = 'chat.txt'
    df_conversa = ler_arquivo(arquivo)

    print("Tabela de conversa:")
    print(df_conversa)

    while True:
        print("\nEscolha uma opção:")
        print("1. Resumo das conversas")
        print("2. Histórico do remetente")
        print("3. Gráfico do histórico do remetente")
        print("4. Gráfico de pizza")
        print("5. Gráfico de linhas")
        print("6. Sair")

        opcao = input("Digite o número da opção: ")

        if opcao == '1':
            print(resumo_conversas(df_conversa))

        elif opcao == '2':
            remetente = input("Digite o nome do remetente: ")
            print(historico_remetente(df_conversa, remetente))

        elif opcao == '3':
            remetente = input("Digite o nome do remetente: ")
            grafico_historico_remetente(df_conversa, remetente)

        elif opcao == '4':
            grafico_pizza(df_conversa)

        elif opcao == '5':
            grafico_linhas(df_conversa)

        elif opcao == '6':
            break

        else:
            print("Opção inválida, tente novamente.")
