import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime

class NoticiasInvesting:
    def __init__(self):
        self.df_noticias = None

    def buscar_e_avaliar_ativo(self, ativo):
        dados_compra = []   
        pode_comprar = 'sim'
        if self.df_noticias is None:
            print("DataFrame não está inicializado. Por favor, execute o método 'obter_noticias' primeiro.")
            return

        # Remover a parte '-otc' do ativo, se estiver presente
        ativo = ativo.split('-')[0]

        # Obter a hora atual
        hora_atual = datetime.datetime.now().time()

        # Separar as duas moedas
        ativo1 = ativo[:3]  # Os primeiros três caracteres representam a primeira moeda
        #ativo2 = ativo[3:]  # Os caracteres restantes representam a segunda moeda

        # Filtrar o DataFrame para o ativo específico
        #df_ativo = self.df_noticias[self.df_noticias['moeda_ativo'] == ativo1]
        # Limpar espaços em branco extras da coluna 'moeda_ativo'
        self.df_noticias['moeda_ativo'] = self.df_noticias['moeda_ativo'].str.strip()

        # Filtrar o DataFrame para os ativos específicos
        df_ativo = self.df_noticias[
            (self.df_noticias['moeda_ativo'].str.contains(ativo1)) #|
            #(self.df_noticias['moeda_ativo'].str.contains(ativo2))
        ]


        # Percorrer todas as linhas do DataFrame do ativo
        for index, row in df_ativo.iterrows():
            # Obter a hora do DataFrame
            hora_df = datetime.datetime.strptime(row['hora'], "%H:%M:%S").time()

            # Calcular a diferença de tempo entre a hora atual e a hora do DataFrame
            diferenca_tempo = abs(datetime.datetime.combine(datetime.date.today(), hora_atual) - datetime.datetime.combine(datetime.date.today(), hora_df))

            # Verificar se a diferença de tempo é maior ou igual a xx minutos
            if diferenca_tempo <= datetime.timedelta(minutes=60):
                pode_comprar = 'nao'

                # Adicionar hora e moeda_ativo aos dados_compra apenas quando pode_comprar é 'nao'
                dados_compra.append({'hora': row['hora'], 'moeda_ativo': row['moeda_ativo'], 'pode_comprar': pode_comprar})
        # Transformar em DataFrame
        df_dados_compra = pd.DataFrame(dados_compra)
        return pode_comprar,df_dados_compra,ativo1

    def obter_noticias(self, url):
        # Realiza a requisição e obtém o conteúdo HTML
        response = requests.get(url)
        html_content = response.content

        # Cria um objeto BeautifulSoup a partir do HTML
        soup = BeautifulSoup(html_content, "lxml")

        # Seleciona a tabela com o id "economicCalendarData"
        tabela = soup.find("table", id="economicCalendarData")

        # Extrai as linhas com a classe "js-event-item"
        linhas = tabela.find_all("tr", class_="js-event-item")

        # Lista para armazenar os dados das notícias
        dados_noticias = []

        # Extrai dados de cada linha e adiciona à lista de dados das notícias
        for linha in linhas:
            count = 0
            noticia = {}
            for coluna_linha in linha.find_all("td"):
                if count == 3:
                    # Extrai o título
                    noticia["titulo"] = coluna_linha.text.strip()
                elif count == 0:
                    # Extrai a hora
                    hora_str = coluna_linha.text.strip()
                    hora = datetime.datetime.strptime(hora_str, "%H:%M")
                    noticia["hora"] = hora.strftime("%H:%M:%S")  # Formata a hora
                elif count == 2:
                    # Extrai o impacto
                    noticia["impacto"] = coluna_linha.text.strip()
                elif count == 1:
                    # Extrai a moeda/ativo
                    noticia["moeda_ativo"] = coluna_linha.text.strip()
                count += 1
            dados_noticias.append(noticia)

        # Cria um DataFrame a partir da lista de dados das notícias
        self.df_noticias = pd.DataFrame(dados_noticias)

        # Exibe as primeiras linhas do DataFrame
        #print(self.df_noticias.head())