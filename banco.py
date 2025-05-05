import datetime

# Variáveis do sistema
saldo = 0.0
extrato = []
limite_saque = 500.0
saques_diarios = 3
saques_realizados = 0
data_ultimo_saque = None

def depositar(valor):
    global saldo, extrato
    if valor > 0:
        saldo += valor
        extrato.append(f"Depósito: R$ {valor:.2f}")
        print("Depósito realizado com sucesso!")
    else:
        print("Valor de depósito inválido. Informe um valor positivo.")

def sacar(valor):
    global saldo, extrato, saques_realizados, data_ultimo_saque

    hoje = datetime.date.today()
    if data_ultimo_saque != hoje:
        saques_realizados = 0
        data_ultimo_saque = hoje

    if saques_realizados >= saques_diarios:
        print("Limite diário de saques atingido.")
    elif valor > limite_saque:
        print(f"Limite por saque é de R$ {limite_saque:.2f}.")
    elif valor > saldo:
        print("Saldo insuficiente para saque.")
    elif valor <= 0:
        print("Valor de saque inválido. Informe um valor positivo.")
    else:
        saldo -= valor
        extrato.append(f"Saque: R$ {valor:.2f}")
        saques_realizados += 1
        print("Saque realizado com sucesso!")

def mostrar_extrato():
    print("\n========== EXTRATO ==========")
    if not extrato:
        print("Não foram realizadas movimentações.")
    else:
        for operacao in extrato:
            print(operacao)
    print(f"\nSaldo atual: R$ {saldo:.2f}")
    print("=============================\n")

# Menu principal
def menu():
    while True:
        print("Escolha uma operação:")
        print("[1] Depositar")
        print("[2] Sacar")
        print("[3] Ver Extrato")
        print("[0] Sair")
        opcao = input("Opção: ")

        if opcao == "1":
            try:
                valor = float(input("Informe o valor do depósito: R$ "))
                depositar(valor)
            except ValueError:
                print("Valor inválido.")
        elif opcao == "2":
            try:
                valor = float(input("Informe o valor do saque: R$ "))
                sacar(valor)
            except ValueError:
                print("Valor inválido.")
        elif opcao == "3":
            mostrar_extrato()
        elif opcao == "0":
            print("Encerrando o sistema. Obrigado!")
            break
        else:
            print("Opção inválida, tente novamente.")

# Inicia o sistema
menu()
