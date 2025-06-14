from abc import ABC, abstractmethod
from datetime import date, datetime
from typing import List, Dict, Optional

class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self) -> float:
        pass
    
    @abstractmethod
    def registrar(self, conta: 'Conta') -> None:
        pass

class Historico:
    def __init__(self):
        self._transacoes: List[Transacao] = []
    
    def adicionar_transacao(self, transacao: Transacao) -> None:
        self._transacoes.append(transacao)
    
    @property
    def transacoes(self) -> List[Transacao]:
        return self._transacoes

class Deposito(Transacao):
    def __init__(self, valor: float):
        self._valor = valor
    
    @property
    def valor(self) -> float:
        return self._valor
    
    def registrar(self, conta: 'Conta') -> None:
        sucesso = conta.depositar(self.valor)
        if sucesso:
            conta.historico.adicionar_transacao(self)

class Saque(Transacao):
    def __init__(self, valor: float):
        self._valor = valor
    
    @property
    def valor(self) -> float:
        return self._valor
    
    def registrar(self, conta: 'Conta') -> None:
        sucesso = conta.sacar(self.valor)
        if sucesso:
            conta.historico.adicionar_transacao(self)

class Cliente:
    def __init__(self, endereco: str):
        self._endereco = endereco
        self._contas: List[Conta] = []
    
    def realizar_transacao(self, conta: 'Conta', transacao: Transacao) -> None:
        transacao.registrar(conta)
    
    def adicionar_conta(self, conta: 'Conta') -> None:
        self._contas.append(conta)
    
    @property
    def contas(self) -> List['Conta']:
        return self._contas
    
    @property
    def endereco(self) -> str:
        return self._endereco

class PessoaFisica(Cliente):
    def __init__(self, cpf: str, nome: str, data_nascimento: date, endereco: str):
        super().__init__(endereco)
        self._cpf = cpf
        self._nome = nome
        self._data_nascimento = data_nascimento
    
    @property
    def cpf(self) -> str:
        return self._cpf
    
    @property
    def nome(self) -> str:
        return self._nome
    
    @property
    def data_nascimento(self) -> date:
        return self._data_nascimento
    
    def __str__(self) -> str:
        return f"Nome: {self.nome}, CPF: {self.cpf}"

class Conta:
    def __init__(self, cliente: Cliente, numero: int):
        self._saldo = 0.0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()
    
    @classmethod
    def nova_conta(cls, cliente: Cliente, numero: int) -> 'Conta':
        return cls(cliente, numero)
    
    @property
    def saldo(self) -> float:
        return self._saldo
    
    @property
    def numero(self) -> int:
        return self._numero
    
    @property
    def agencia(self) -> str:
        return self._agencia
    
    @property
    def cliente(self) -> Cliente:
        return self._cliente
    
    @property
    def historico(self) -> Historico:
        return self._historico
    
    def sacar(self, valor: float) -> bool:
        if valor <= 0:
            print("Operação falhou! O valor informado é inválido.")
            return False
        
        if self.saldo < valor:
            print("Operação falhou! Você não tem saldo suficiente.")
            return False
        
        self._saldo -= valor
        print(f"Saque de R$ {valor:.2f} realizado com sucesso!")
        return True
    
    def depositar(self, valor: float) -> bool:
        if valor <= 0:
            print("Operação falhou! O valor informado é inválido.")
            return False
        
        self._saldo += valor
        print(f"Depósito de R$ {valor:.2f} realizado com sucesso!")
        return True

class ContaCorrente(Conta):
    def __init__(self, cliente: Cliente, numero: int, limite: float = 500.0, limite_saques: int = 3):
        super().__init__(cliente, numero)
        self._limite = limite
        self._limite_saques = limite_saques
    
    def sacar(self, valor: float) -> bool:
        if valor <= 0:
            print("Operação falhou! O valor informado é inválido.")
            return False
        
        if valor > self._limite:
            print(f"Operação falhou! O valor do saque excede o limite de R$ {self._limite:.2f}.")
            return False
        
        saques_diarios = len(
            [transacao for transacao in self.historico.transacoes 
             if isinstance(transacao, Saque) and 
                transacao.data.date() == datetime.now().date()]
        )
        
        if saques_diarios >= self._limite_saques:
            print(f"Operação falhou! Número máximo de {self._limite_saques} saques diários excedido.")
            return False
        
        return super().sacar(valor)
    
    def __str__(self) -> str:
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """

# Funções para interação com o menu
def menu() -> None:
    print("\n".join([
        "\n======== MENU ========",
        "[1]\tDepositar",
        "[2]\tSacar",
        "[3]\tExtrato",
        "[4]\tNova conta",
        "[5]\tListar contas",
        "[6]\tNovo usuário",
        "[0]\tSair",
        "======================="
    ]))

def filtrar_cliente(cpf: str, clientes: List[PessoaFisica]) -> Optional[PessoaFisica]:
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None

def criar_cliente(clientes: List[PessoaFisica]) -> None:
    cpf = input("Informe o CPF (somente números): ")
    cliente = filtrar_cliente(cpf, clientes)
    
    if cliente:
        print("\nJá existe cliente com esse CPF!")
        return
    
    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")
    
    dia, mes, ano = map(int, data_nascimento.split('-'))
    data_nascimento = date(ano, mes, dia)
    
    cliente = PessoaFisica(cpf=cpf, nome=nome, data_nascimento=data_nascimento, endereco=endereco)
    clientes.append(cliente)
    
    print("\n=== Cliente criado com sucesso! ===")

def criar_conta(numero_conta: int, clientes: List[PessoaFisica], contas: List[ContaCorrente]) -> None:
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)
    
    if not cliente:
        print("\nCliente não encontrado, fluxo de criação de conta encerrado!")
        return
    
    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.adicionar_conta(conta)
    
    print("\n=== Conta criada com sucesso! ===")

def listar_contas(contas: List[ContaCorrente]) -> None:
    if not contas:
        print("\nNenhuma conta cadastrada!")
        return
    
    print("\n======== CONTAS ========")
    for conta in contas:
        print(str(conta))
        print("=" * 23)

def depositar(clientes: List[PessoaFisica]) -> None:
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)
    
    if not cliente:
        print("\nCliente não encontrado!")
        return
    
    if not cliente.contas:
        print("\nCliente não possui contas!")
        return
    
    # Simplificação: usando a primeira conta do cliente
    conta = cliente.contas[0]
    valor = float(input("Informe o valor do depósito: "))
    
    transacao = Deposito(valor)
    cliente.realizar_transacao(conta, transacao)

def sacar(clientes: List[PessoaFisica]) -> None:
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)
    
    if not cliente:
        print("\nCliente não encontrado!")
        return
    
    if not cliente.contas:
        print("\nCliente não possui contas!")
        return
    
    # Simplificação: usando a primeira conta do cliente
    conta = cliente.contas[0]
    valor = float(input("Informe o valor do saque: "))
    
    transacao = Saque(valor)
    cliente.realizar_transacao(conta, transacao)

def exibir_extrato(clientes: List[PessoaFisica]) -> None:
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)
    
    if not cliente:
        print("\nCliente não encontrado!")
        return
    
    if not cliente.contas:
        print("\nCliente não possui contas!")
        return
    
    # Simplificação: usando a primeira conta do cliente
    conta = cliente.contas[0]
    
    print("\n======== EXTRATO ========")
    transacoes = conta.historico.transacoes
    
    if not transacoes:
        print("Não foram realizadas movimentações.")
    else:
        for transacao in transacoes:
            tipo = "Depósito" if isinstance(transacao, Deposito) else "Saque"
            print(f"{tipo}:\tR$ {transacao.valor:.2f}")
    
    print(f"\nSaldo:\t\tR$ {conta.saldo:.2f}")
    print("========================")

def main() -> None:
    clientes: List[PessoaFisica] = []
    contas: List[ContaCorrente] = []
    
    while True:
        menu()
        opcao = input("=> ")
        
        if opcao == "1":
            depositar(clientes)
        elif opcao == "2":
            sacar(clientes)
        elif opcao == "3":
            exibir_extrato(clientes)
        elif opcao == "4":
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)
        elif opcao == "5":
            listar_contas(contas)
        elif opcao == "6":
            criar_cliente(clientes)
        elif opcao == "0":
            break
        else:
            print("\nOperação inválida, por favor selecione novamente a operação desejada.")

if __name__ == "__main__":
    main()
