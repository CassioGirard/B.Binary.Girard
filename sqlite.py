import sqlite3

class bd_sqlite:
    def __init__(self):
        self.nome_banco = 'dados_operacoes.db'

    def criar_tabela(self,conn):
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS operacoes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                estrategia_nome TEXT,
                ativo TEXT,
                resultado TEXT
            )
        ''')
        conn.commit()

    # Função para inserir dados na tabela do banco de dados SQLite
    def inserir_dados(self,conn, estrategia_nome, ativo, resultado_extenso):
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO operacoes (estrategia_nome, ativo, resultado)
            VALUES (?, ?, ?)
        ''', (estrategia_nome, ativo, resultado_extenso))
        conn.commit()
        conn.close()

    # Função para conectar ao banco de dados SQLite
    def conectar_banco(self):
        conn = sqlite3.connect('dados_operacoes.db')  # Nome do arquivo do banco de dados SQLite
        return conn
    
    def listar_estrategias_por_vitoria(self):
        conn = self.conectar_banco()
        cursor = conn.cursor()

        # Consulta SQL para obter todas as estratégias únicas na tabela
        cursor.execute('SELECT DISTINCT estrategia_nome FROM operacoes')

        estrategias = cursor.fetchall()

        # Lista para armazenar o nome das estratégias e seus resultados
        estrategias_resultados = []

        # Iterar sobre as estratégias e calcular a porcentagem de vitória para cada uma
        for estrategia in estrategias:
            estrategia_nome = estrategia[0]
            porcentagem_win = self.calcular_porcentagem_win(estrategia_nome=estrategia_nome)
            estrategias_resultados.append((estrategia_nome, porcentagem_win))

        # Ordenar as estratégias pelo cálculo de vitória em ordem decrescente
        #estrategias_ordenadas = sorted(estrategias_resultados, key=lambda x: x[1], reverse=True)

        # Ordenar as estratégias pelo cálculo de vitória em ordem crescente
        estrategias_ordenadas = sorted(estrategias_resultados, key=lambda x: x[1], reverse=False)

        # Obter o nome da estratégia com a maior taxa de sucesso
        estrategia_mais_acertada = estrategias_ordenadas[0][0] if estrategias_ordenadas else None

        conn.close()

        return estrategias_ordenadas, estrategia_mais_acertada

    # Função para consultar os dados na tabela e calcular a porcentagem de operações vencedoras (win)
    #def calcular_porcentagem_win(self, ativo_atual, estrategia_nome):
    def calcular_porcentagem_win(self,estrategia_nome):
        conn = self.conectar_banco()
        cursor = conn.cursor()

        # Consulta SQL para selecionar apenas os registros com o ativo atual e estratégia nome especificados
        #consulta_sql = 'SELECT * FROM operacoes WHERE ativo = ? AND estrategia_nome = ?'
        #cursor.execute(consulta_sql, (ativo_atual, estrategia_nome))
        consulta_sql = 'SELECT * FROM operacoes WHERE estrategia_nome = ?'
        cursor.execute(consulta_sql, (estrategia_nome,))

        # Obter todos os resultados da consulta
        resultados = cursor.fetchall()

        # Contadores para operações win e loss
        operacoes_win = 0
        total_operacoes = len(resultados)

        # Iterar sobre os resultados e contar operações win
        for resultado in resultados:
            if resultado[3] == 'Win':  # Assumindo que a coluna 'resultado' é a quarta coluna na tabela
                operacoes_win += 1

        # Calcular a porcentagem de operações win
        if total_operacoes > 0:
            porcentagem_win = (operacoes_win / total_operacoes) * 100
        else:
            porcentagem_win = 0

        conn.close()

        return porcentagem_win
