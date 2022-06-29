#recebe percepções, e devolver novas informações
#unica função que escreve e lê da base de dados
#o objetivo é ir tirando todos os "ou" dos fatos, resolvendo os "se...então"

import utils
class Motor:
    def __init__(self, linhas, colunas) -> None:
        self.bc = None
        self.tam_ambiente = [linhas, colunas]
        self.abrir_bc()
    
    #cria o arquivo da base de conhecimento
    def cria_bc(self, marcar):
        
        bc = open(str(marcar)+'_knowlede_base.txt', 'a+')
        bc.write("#base de conhecimento do mundo de Wumpus\n")
        self.bc = bc
    
    def abrir_bc(self):
        bc = open('knowlede_base.txt', 'r+')
        self.bc = bc   
    
    def fechar_bc(self):
        self.bc.close()
    
    def _deletar_linha(self, linha):
        #tem que tirar o \n
        arquivo = self.bc.readlines()
        self.bc.seek(0)
        
        for l in arquivo:
            
            if l != linha:
                self.bc.write(l)
        
        self.bc.truncate()

    #limpa deducoes comprovadamente falsas (usando fatos)
    def _limpar_deducoes(self, fato: str):

        base_conhecimento = self.bc.readlines()
        fato_coord = fato[5:12]
        fato_tema = fato[13:19]
        fato_estado = fato[21:]
        #print(fato_estado)
        for linha in base_conhecimento:
            if linha.find("deducao") != -1:
                print(linha)
                #checando se a deducao é na msm quadrado e msm tema
                if linha.find(fato_coord) != -1 and linha.find(fato_tema) != -1:
                    self._deletar_linha(linha)

    #recebe as percepções do quadrado atual, e anota na KB
    def _anotar_bc(self, percepcoes: dict, coordenadas):
        #anotar essas percepções na KB
        #coordenada: percepção ( 1,1: brisa) (1,1: sem fedor)
        
        #preciso pegar os dados do perception e criar a string no formato adequado
        #os dados vem na forma "wumpus": False
        # se a percepção ja tiver (no caso de estar voltando), não escrever
        lista = []
        base_conhecimento = self.bc.readlines()
        for info in percepcoes.items():
            p = "fato " + str(coordenadas) + " " + str(info) + '\n'
            lista.append(p)
        
        #nao adiciona fatos repetidos
        for item in lista:
            flag = True
            for linha in base_conhecimento:
                if item == linha:
                    flag = False
                    break
            if flag:
                self.bc.write(item)
                self._limpar_deducoes(item)
        
    #pega as coordenas, a KB e faz inferencias. Só trabalha com fatos e conclusões fortes
    def inferir(self, coordenadas, percepcoes: dict):
        #pega as coordenas, as percepções a KB e faz inferencias
        #percepções é um dicionario
        #se (coordenada: percepção), então (coordenada_vizinha: contem)
        #(se 1,1: brisa) então ((1,2: buraco) ou (2,1: buraco) ou (0,1: buraco))
        #busca na KB as coordenadas referidas (as vizinhas)
        #se encontrar que uma vizinha já foi visitada, retira ela da proposição
        #(se 1,1: brisa) então ((1,2: buraco) ou (2,1: buraco) ou (0,1: buraco)), e (1,2: sem buraco), então ((2,1: buraco) ou (0,1: buraco))
        # anota apenas (se 1,1: brisa) então ((2,1: buraco) ou (0,1: buraco))
        #cuidado que essa lógica começa a ficar fudida
        self._anotar_bc(percepcoes, coordenadas)
        vizinhos = utils.vizinhos(coordenadas, self.tam_ambiente)
        self.abrir_bc()
        dados = []
        
        #inferindo ao redor
        for info in percepcoes.items():
            if info[0] == "fedor" and info[1]:
                for v in vizinhos:
                    inferencia = (v, "wumpus")
                    dados.append(inferencia)
            if info[0] == "brisa" and info[1]:
                for v in vizinhos:
                    inferencia = (v, "buraco")
                    dados.append(inferencia)
        
        #consultando a base e não anota deducao que já é provada como falsa
        base = self.bc.readlines()
        for deducao in dados:
            for conhecimento in base:
                if conhecimento.find(str(deducao[0])) != -1:
                    #conhecimento contem uma menção ao quadrado da deducao
                    if conhecimento.find(str(deducao[1])) != -1:
                        #contem uma menção tanto ao qadrado quanto ao conteudo
                        if conhecimento.find("False") != -1 and conhecimento.find("fato") != -1:
                            #print("removendo: ", deducao)
                            dados.remove(deducao)

        #preciso criar um tipo diferente de conhecimento? = deducao?
        for d in dados:
            flag = True
            frase = "deducao " + str(d[0])+ ' (' + d[1] + ", True)" +'\n'
            for conhecimento in base:
                if conhecimento.find(frase) != -1:
                    flag = False
            if flag:
                self.bc.write(frase)
            #vai escrever um monte de deducao repetida, acho que nao tem problema
            #quando provar que uma deducao é falsa, remove todas da base
            #quando for tomar uma decisao, usar um contador, quanto mais deducoes iguais, mais provavel
        
        #self._anotar_bc(percepcoes, coordenadas)


    def fatos(self, coordenadas):
        #pega as coordenadas e a KB e retornar todas os fatos a respeito dos vizinhos
        vizinhos = utils.vizinhos(coordenadas, self.tam_ambiente)
        base_conhecimento = self.bc.readlines()

        lista_de_fatos = []

        #para cada vizinho, consultar os fatos
        for linha in base_conhecimento:
            for viz in vizinhos:
                if linha.find(str(viz)) != -1 and linha.find("fato") != -1:
                    lista_de_fatos.append(linha)
                    
        return lista_de_fatos

    #retorna todas as deduções relacionadas aos vizinhos de coordenadas
    def deducoes(self, coordenadas):
        #pega as coordenadas e a KB, e retorna todas "se então" relacionadas com as vizinhas
        #(se 1,1: brisa) então ((2,1: buraco) ou (0,1: buraco))
        #sao as deducoes
        vizinhos = utils.vizinhos(coordenadas, self.tam_ambiente)
        base_conhecimento = self.bc.readlines()
        lista_de_deducoes = []
        for linha in base_conhecimento:
            for viz in vizinhos:
                if linha.find(str(viz)) != -1 and linha.find("deducao") != -1:
                    lista_de_deducoes.append(linha)

        return lista_de_deducoes


percepicoes = {
            "wumpus" : False,
            "ouro" : False,
            "buraco" : False,
            "fedor": True,
            "brisa" :True
        }
novo = Motor(4,4,)
#novo.cria_bc('Alpha')
novo.abrir_bc()
fato = "fato [0, 2] (wumpus, False)\n"
#novo._anotar_bc(percepicoes, [0,2])

# novo.abrir_bc('Alpha') #tenho que abrir de novo, pq a func fecha automaticamente
novo.inferir([1,2], percepicoes)
novo._limpar_deducoes(fato)
#novo._deletar_linha(fato)
#novo.fatos([2,1])