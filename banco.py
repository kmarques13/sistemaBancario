import datetime
import re

# Variáveis do sistema
usuarios = []
contas = []

AGENCIA = "0001"

def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    """Função de saque - keyword-only arguments"""
    if valor > saldo:
        print("Saldo insuficiente para saque.")
    elif valor > limite:
        print(f"Limite por saque é de R$ {limite:.2f}.")
    elif numero_saques >= limite_saques:
        print("Limite diário de saques atingido.")
    elif valor <= 0:
        print("Valor de saque inválido.")
    else:
        saldo -= valor
        extrato.append(f"Saque: R$ {valor:.2f}")
        numero_saques += 1
        print("Saque realizado com sucesso!")
    return saldo, extrato, numero_saques

def depositar(saldo, valor, extrato, /):
    """Função de depósito - positional-only arguments"""
    if valor > 0:
        saldo += valor
        extrato.append(f"Depósito: R$ {valor:.2f}")
        print("Depósito realizado com sucesso!")
    else:
        print("Valor de depósito inválido.")
    return saldo, extrato

def exibir_extrato(saldo, /, *, extrato):
    """Função de extrato - positional and keyword-only arguments"""
    print("\n========== EXTRATO ==========")
    if not extrato:
        print("Não foram realizadas movimentações.")
    else:
        for operacao in extrato:
            print(operacao)
    print(f"\nSaldo atual: R$ {saldo:.2f}")
    print("=============================\n")

def criar_usuario(usuarios):
    cpf = input("Informe o CPF (somente números): ")
    cpf = re.sub(r'\D', '', cpf)  # Remove qualquer não-dígito

    usuario = [u for u in usuarios if u["cpf"] == cpf]
    if usuario:
        print("Usuário já cadastrado.")
        return

    nome = input("Informe o nome completo: ")
    nascimento = input("Informe a data de nascimento (dd/mm/aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    usuarios.append({
        "nome": nome,
        "data_nascimento": nascimento,
        "cpf": cpf,
        "endereco": endereco
    })
    print("Usuário criado com sucesso!")

def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Informe o CPF do usuário: ")
    cpf = re.sub(r'\D', '', cpf)

    usuario = next((u for u in usuarios if u["cpf"] == cpf), None)
    if not usuario:
        print("Usuário não encontrado. Crie um usuário primeiro.")
        return None

    conta = {
        "agencia": agencia,
        "numero_conta": numero_conta,
        "usuario": usuario
    }
    print(f"Conta criada com sucesso! Agência: {agencia}, Conta: {numero_conta}")
    return conta

# Menu principal
def menu():
    saldo = 0.0
    extrato = []
    limite = 500.0
    numero_saques = 0
    limite_saques = 3
    global usuarios, contas

    while True:
        print("""
[1] Depositar
[2] Sacar
[3] Ver Extrato
[4] Criar Usuário
[5] Criar Conta
[6] Listar Contas
[0] Sair
""")
        opcao = input("Escolha uma operação: ")

        if opcao == "1":
            try:
                valor = float(input("Informe o valor do depósito: R$ "))
                saldo, extrato = depositar(saldo, valor, extrato)
            except ValueError:
                print("Valor inválido.")
        
        elif opcao == "2":
            try:
                valor = float(input("Informe o valor do saque: R$ "))
                saldo, extrato, numero_saques = sacar(
                    saldo=saldo,
                    valor=valor,
                    extrato=extrato,
                    limite=limite,
                    numero_saques=numero_saques,
                    limite_saques=limite_saques
                )
            except ValueError:
                print("Valor inválido.")

        elif opcao == "3":
            exibir_extrato(saldo, extrato=extrato)

        elif opcao == "4":
            criar_usuario(usuarios)

        elif opcao == "5":
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)
            if conta:
                contas.append(conta)

        elif opcao == "6":
            print("\n=== Contas cadastradas ===")
            for conta in contas:
                usuario = conta["usuario"]
                print(f"Agência: {conta['agencia']} | Conta: {conta['numero_conta']} | Titular: {usuario['nome']}")
            print("==========================\n")

        elif opcao == "0":
            print("Encerrando o sistema. Obrigado!")
            break

        else:
            print("Opção inválida, tente novamente.")

# Inicia o sistema
menu()
