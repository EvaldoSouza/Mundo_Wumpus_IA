#criar a matriz: Vai ser uma lista, de listas, onde cada posição é uma lista do que tem naquele quadrado
#[Wumpus, Ouro, (formula)*poço] e [Fedor, Brilho, Vento]
#[[[A],[],[],[]],
# [[A],[],[],[]],
# [[A],[],[],[]],
# [[A],[],[],[]]]

import random
#criar uma lista com o que o espaço vai ter
#criar a matriz com todo o ambiente
#uma função randomica para preencher o ambiente
class Quadrado:
    def __init__(self) -> None:
        self.wumpus = False
        self.ouro = False
        self.buraco = False
        self.fedor = False
        self.brisa = False
    
    #vou acessar as variaveis diretamente
    def imprimir(self):
        print("Wumpus: ", self.wumpus, ". Ouro: ", self.ouro, ". Buraco:", self.buraco, ". Fedor:", self.fedor, ". Brilho: ", self.brilho, ". Brisa: ", self.brisa)

    def retorna_dict(self):
        percepicoes = {
            "wumpus" : self.wumpus,
            "ouro" : self.ouro,
            "buraco" : self.buraco,
            "fedor": self.fedor,
            "brisa" :self.brisa
        }
        return percepicoes
class Ambiente:
    def __init__(self, linhas, colunas) -> None:
        self.linhas = linhas
        self.colunas = colunas
        self.quant_quad = linhas*colunas
    
    def _conteudo(self):
        contem = []
        contem.append("Wumpus")
        contem.append("Ouro")
        buracos = int(self.quant_quad / 5)
        for b in range(buracos):
            contem.append("Buraco")
        
        #quantidade de quadrados com nada, excluindo sinais
        nada = self.quant_quad - buracos - 5 #1 Wumpus e 1 ouro, e 3 nadas que já são obrigatórios no começo
        for n in range(nada):
            contem.append("Nada")
        return contem
    
    def imprimir(self, espaco):
        for l in range(self.linhas):
            for c in range(self.colunas):
                print( l, c, ":")
                espaco[l][c].imprimir()

               
    def distribuir(self):
        espaco = []
        for l in range(self.linhas):
            linha = []
            espaco.append(linha)
            for c in range(self.colunas):
                quadro = Quadrado()
                linha.append(quadro)
        
        conteudos = self._conteudo()
        random.shuffle(conteudos)
        
        for l in range(self.linhas):
            for c in range(self.colunas):
                if l == 0 and c == 0:
                    #manter tudo falso
                    pass
                elif l == 0 and c == 1:
                    pass
                elif l==1 and c == 0:
                    pass
                else:
                    coisa = conteudos.pop(0)
                    if coisa == "Buraco":
                        espaco[l][c].buraco = True
                    if coisa == "Wumpus":
                        #fazer o wumpus ter chance cair em um buraco ou em cima do ouro
                        lin = random.randrange(self.linhas)
                        col = random.randrange(self.colunas)
                        espaco[lin][col].wumpus = True
                    if coisa == "Ouro":
                        espaco[l][c].ouro = True
        
        for l in range(self.linhas):
            for c in range(self.colunas):
                if espaco[l][c].buraco:
                    #print("Buraco em: ", l, c)
                    try:
                        espaco[l-1][c].brisa = True
                        #print("Brisa em:", l-1, c)
                    except IndexError:
                        pass
                    try:
                        espaco[l+1][c].brisa = True
                        #print("Brisa em:", l+1, c)
                    except IndexError:
                        pass
                    try:
                        espaco[l][c-1].brisa = True
                        #print("Brisa em:", l, c-1)
                    except IndexError:
                        pass
                    try:
                        espaco[l][c+1].brisa = True
                        #print("Brisa em:", l, c+1)
                    except IndexError:
                        pass
                elif espaco[l][c].wumpus:
                    #print("Wumpus em: ", l, c)
                    try:
                        espaco[l-1][c].fedor = True
                    except IndexError:
                        pass
                    try:
                        espaco[l+1][c].fedor = True
                    except IndexError:
                        pass
                    try:
                        espaco[l][c-1].fedor = True
                    except IndexError:
                        pass
                    try:
                        espaco[l][c+1].fedor = True
                    except IndexError:
                        pass
        
        return espaco
        #self.imprimir(espaco)

quad = Quadrado()
print(quad.wumpus)