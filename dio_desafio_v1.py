from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime


class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf


class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")

        elif valor > 0:
            self._saldo -= valor
            print("\n=== Saque realizado com sucesso! ===")
            return True

        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

        return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("\n=== Depósito realizado com sucesso! ===")
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
            return False

        return True


class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__]
        )

        excedeu_limite = valor > self.limite
        excedeu_saques = numero_saques >= self.limite_saques

        if excedeu_limite:
            print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")

        elif excedeu_saques:
            print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")

        else:
            return super().sacar(valor)

        return False

    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """


class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%s"),
            }
        )


class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass

    @abstractclassmethod
    def registrar(self, conta):
        pass


class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

##IPLEMENTAÇÃO DO SISTEMA BANCARIO - DESAIO_V1 e DESAFIO_V2: CONCLUIDO COM SUCESSO!

#funçao que cria um MENU com as opções de serviços do sistema.
def menu():
    print("\n|*******************************|")
    print("\n|**  JRSS - SISTEMAS BANCARIO **|")
    print("  |*******************************|")
    print("|---1 -> Depositar\n")
    print("|---2 -> Sacar\n")
    print("|---3 -> Extrato\n")
    print("|---4 -> Sair\n")
    print("\n|*******************************|")
    
    return input("\n   DIGITE UMA OPÇÃO DO MENU: \n")
    
#Exibe uma mensagem para o usuario informar a opção de serviços que deseja realisar


# Criando cliente e conta inicial
cliente = PessoaFisica("Joel Ricardo", "20-06-1989", "02345678911", "Rua Moteiro Lobato, 1539")
conta = ContaCorrente.nova_conta(cliente, numero = 1)
cliente.adicionar_conta(conta)

#Opções do menu escolha do menu principal
#cria um laço  de repetição que executa uma rotina com 4 opções no menu
# enquanto a condição de teste for avaliada como verdadeira. 

while True:
    opcao = menu()

    if opcao == "1": #Faz a verificação se o usuário escolheu a opção de depósito.
        valor = float(input("DIGITE O VALOR DO DEPÓSITO: "))#Converte o valor de entrada para um numero do tipo float.
#Exibe uma Mensagem ao usuário pedindo o valor de entrada 
        deposito = Deposito(valor)# Gera a o deposito com o mesmo valor informadoo pelo usuario
        cliente.realizar_transacao(conta, deposito)#Executa a Operação de deposito na conta do Cliente.


    elif opcao == "2":
        valor = float(input("DIGITE O VALOR DO SAQUE: "))
        saque = Saque(valor)# Gera a Operação de saque.
        cliente.realizar_transacao(conta, saque)#Realiza a Operação de saque.

    elif opcao == "3":
        print("\n>>>>> EXTRADO DA CONTA: <<<<<")
        print(f"Saldo atual ---->R$ {conta.saldo}")#{conta.saldo}->Exibe o saldo atual da conta do cliente.
        for transacao in conta.historico.transacoes:
#O Laço for -> gera um Loop percorrendo a lista de transações do historico da conta do cliente.
            print(transacao)#Imprime o historico na tela 

    elif opcao == "4":
        print("FINALIZANDO O SISTEMA...")
        break #Interrompe o Laço de repetição e encerra o sistema.

    else:
        print("OPÇÃO INVALIDA, TENTE NOVAMENTE...")




