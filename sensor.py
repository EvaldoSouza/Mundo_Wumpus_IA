
import ambiente

class Sensor:
    def __init__(self, caverna: ambiente.Ambiente) -> None:
        self.vivo = True
        self.pegou_ouro = False
        self.caverna = caverna
        self.posicao = [0,0]
        self.frente = [0,1]
        self.atual = caverna[0][0] #isso é um Quadrado
        pass
    
    def atualizar(self, linha, coluna):
        #pegar as informações do quadrado e passar para o motor de inferencia
        self.atual = self.caverna[linha][coluna]
        self.posicao = [linha, coluna]
        #preciso atualizar a "frente" também
        self.frente = [linha+1, coluna]
        
    def parede(self):
        linhas = len(self.caverna)
        colunas = len(self.caverna[0])
        if self.frente[0] > linhas or self.frente[1] > colunas:
            return False
        else:
            return True
        
    
    def ver_a_frente(self):
        return self.frente
    
    def girar_visao(self, direcao: list):
        self.frente = direcao
    
    #retorna um dicionario com as percepções do local
    def conteudo(self):
        percepicoes = {
            "wumpus" : self.atual.wumpus,
            "ouro" : self.atual.ouro,
            "buraco" : self.atual.buraco,
            "fedor": self.atual.fedor,
            "brilho" : self.atual.brilho,
            "brisa" :self.atual.brisa
        }
        return percepicoes