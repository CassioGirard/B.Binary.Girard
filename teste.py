from iqoptionapi.stable_api import IQ_Option
from datetime import datetime
import time
from configobj import ConfigObj
import json, sys

config = ConfigObj('config.txt')
email = config['LOGIN']['login']
senha = config['LOGIN']['senha']
valor_entrada = config['AJUSTES']['valor_entrada']
tipo = config['AJUSTES']['tipo']


API = IQ_Option(email, senha)

check, reason = API.connect()
if check:
    print('conectado com sucesso')
else:
    print('Não conectou')
    print(reason)
    sys.exit()

while True:
    escolha = input('selecione a conta em que deseja conectar: demo ou real - ')
    if escolha == 'demo':
        conta = 'PRACTICE'
        print('Conta demo selecionada')
        break
    if escolha == 'real':
        conta = 'REAL'
        print('Conta real selecionada')
        break
    else:
        print('Escolha incorreta! Digite demo ou real!| - ')

API.change_balance(conta)


def compra(ativo, valor_entrada, direcao, exp, tipo):
    if tipo == 'digital':
        check, id = API.buy_digital_spot_v2(ativo, valor_entrada, direcao, exp)
    else: 
        check, id = API.buy(valor_entrada, ativo, direcao, exp)
    
    if check:
        print('\n>>Ordem aberta \n>>Par:', ativo,'\n>>Timeframe:', exp,'\n>>Entrada de:',cifrao,valor_entrada)

        while True:
            time.sleep(0.1)
            status, resultado = API.check_win_digital_v2(id) if tipo == 'digital' else API.check_win_v4(id)
            if status:
                if resultado > 0:
                    print('\nWIN', round(resultado,2))
                elif resultado == 0:
                    print('\nEMPATE', round(resultado,2))
                else:
                    print('\nLOSS', round(resultado,2))
                break

    else:
        print('Erro na abertura da ordem,' , id)

def estrategia_mhi():
    while True:
        time.sleep(0.1)

        minutos = float(datetime.fromtimestamp(API.get_server_timestamp()).strftime('%M.%$')[:1])
        entrar = True if (minutos >= 4.59 and minutos <= 5.00) or minutos > == 9.59

ativo = input('\n >> Digite o ativo: ').upper()
direcao = input('\n >> Entrada para call ou put? ').lower()
exp = input('\n >> Qual o timeframe? ')

perfil = json.loads(json.dumps(API.get_profile_ansyc()))
cifrao = str(perfil['currency_char'])
nome = str(perfil['name'])
valor_conta = float(API.get_balance())

print('\n\n Olá, ', nome, '\nSeja bem vindo ao Robô')
print('\n Seu saldo na conta ', escolha, 'é de', cifrao,valor_conta)
print('\n Seu valor de entrada é de', cifrao,valor_entrada)


compra(ativo, valor_entrada, direcao, exp, tipo)