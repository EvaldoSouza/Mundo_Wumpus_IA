#recebe percepções, e devolver novas informações
#unica função que escreve e lê da base de dados
#o objetivo é ir tirando todos os "ou" dos fatos, resolvendo os "se...então"
class Motor:
    def __init__(self) -> None:
        self.bc = None
        pass
    
    #cria o arquivo da base de conhecimento
    def cria_bc(self, marcar):
        
        bc = open(str(marcar)+'_knowlede_base.txt', 'a')
        bc.write("#base de conhecimento do mundo de Wumpus\n")
        self.bc = bc
    
    def abrir_bc(self, marcar):
        bc = open(str(marcar)+'_knowlede_base.txt', 'r+')
        self.bc = bc   
    
    def fechar_bc(self):
        self.bc.close()
    
    #recebe as percepções do quadrado atual, e anota na KB
    def atual(self, perceptions: dict, coordenadas):
        #anotar essas percepções na KB
        #coordenada: percepção ( 1,1: brisa) (1,1: sem fedor)
        
        #preciso pegar os dados do perception e criar a string no formato adequado
        #os dados vem na forma "wumpus": False
        # se a percepção ja tiver (no caso de estar voltando), não escrever
        lista = []
        base_conhecimento = self.bc.readlines()
        for info in perceptions.items():
            p = str(coordenadas) + " " + str(info) + '\n'
            lista.append(p)
            # if p in self.bc.readlines():
            #     print(p)
            # else:
            #     self.bc.write(p)
        # for item in lista:
        #     self.bc.write(item)
        
        for item in lista:
            flag = True
            for linha in base_conhecimento:
                if item == linha:
                    print("achei")
                    flag = False
                    break
            if flag:
                self.bc.write(item) 
                       
            
        
        # for line in self.bc.readlines():
        #     print(line)
        
        #chama a _inferir
        self._inferir(coordenadas)
        pass
    
    #pega as coordenas, a KB e faz inferencias. Só trabalha com fatos e conclusões fortes
    def _inferir(self, coordenadas):
        #pega as coordenas, a KB e faz inferencias
        #se (coordenada: percepção), então (coordenada_vizinha: contem)
        #(se 1,1: brisa) então ((1,2: buraco) ou (2,1: buraco) ou (0,1: buraco))
        #busca na KB as coordenadas referidas (as vizinhas)
        #se encontrar que uma vizinha já foi visitada, retira ela da proposição
        #(se 1,1: brisa) então ((1,2: buraco) ou (2,1: buraco) ou (0,1: buraco)), e (1,2: sem buraco), então ((2,1: buraco) ou (0,1: buraco))
        # anota apenas (se 1,1: brisa) então ((2,1: buraco) ou (0,1: buraco))
        #cuidado que essa lógica começa a ficar fudida
        
        #se brisa em atual, entao buraco em vizinho
        #se fedor em atual, entao wumpus em vizinho
        #se brilho em atual, entao ouro em vizinho
        # for lines in self.bc:
        #     print(lines)
        pass
    
    def informacoes(self, coordenadas):
        #pega as coordenadas e a KB e retornar todas os fatos a respeito dos vizinhos
        pass
    def duvidas(self, coordenadas):
        #pega as coordenadas e a KB, e retorna todas "se então" relacionadas com as vizinhas
        #(se 1,1: brisa) então ((2,1: buraco) ou (0,1: buraco))
        pass


percepicoes = {
            "wumpus" : False,
            "ouro" : False,
            "buraco" : False,
            "fedor": False,
            "brilho" : True,
            "brisa" :False
        }
novo = Motor()
#novo.cria_bc('Alpha')
novo.abrir_bc('Alpha')
novo.atual(percepicoes, [2,2])