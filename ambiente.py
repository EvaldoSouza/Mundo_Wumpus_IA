#criar a matriz: Vai ser uma lista, de listas, onde cada posição é uma lista do que tem naquele quadrado
#[Wumpus, Ouro, (formula)*poço] e [Fedor, Brilho, Vento]
#[[[A],[],[],[]],
# [[A],[],[],[]],
# [[A],[],[],[]],
# [[A],[],[],[]]]

from operator import contains
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
        self.brilho = False
        self.brisa = False
        pass
    
class Ambiente:
    def __init__(self, linhas, colunas) -> None:
        self.linhas = linhas
        self.colunas = colunas
        self.quant_quad = linhas*colunas
    
    #recebe um dicionario com os valores que devem ser contidos no quadrado
    def espace(self,*conteudos):
        #quadrado = conteudos.values()
        quadrado = list(conteudos)
        quadrado.append("Nada")
        return quadrado
    
    #cria uma lista com o que deve conter : [Wumpus, Ouro, (formula)*poço]
    def conteudo(self):
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
    

    def criar(self):
        #regras: O ouro pode estar com o Wumpus. Primeira casa e adjacentes tem que ter nada. 
        espaco = []
        conteudo = self.conteudo()
        random.shuffle(conteudo)
        for l in range(self.linhas):
            linha = []
            espaco.append(linha)
            for c in range(self.colunas):
                if l == 0 and c == 0:
                    coluna = []
                    coluna.append("Nada")
                elif l == 0 and c == 1:
                    coluna = []
                    coluna.append("Nada")
                elif l == 1 and c == 0:
                    coluna = []
                    coluna.append("Nada")
                else:
                   coluna = []
                   coluna.append(conteudo.pop(0)) 

                linha.append(coluna)
        
        #agora preencher os sinais
        for l in range(self.linhas):
            for c in range(self.colunas):
                quadrado = espaco[l][c]
                for conteudo in quadrado:
                    if conteudo == "Buraco":
                        #adicionando Brisas
                        try:
                            espaco[l-1][c].append("Brisa")
                        except IndexError:
                            pass
                        try:
                            espaco[l+1][c].append("Brisa")
                        except IndexError:
                            pass
                        try:
                            espaco[l][c-1].append("Brisa")
                        except IndexError:
                            pass
                        try:
                            espaco[l][c+1].append("Brisa")
                        except IndexError:
                            pass
                    
                    if conteudo == "Wumpus":
                        try:
                            espaco[l-1][c].append("Fedor")
                        except IndexError:
                            pass
                        try:
                            espaco[l+1][c].append("Fedor")
                        except IndexError:
                            pass
                        try:
                            espaco[l][c-1].append("Fedor")
                        except IndexError:
                            pass
                        try:
                            espaco[l][c+1].append("Fedor")
                        except IndexError:
                            pass
                    
                    if conteudo == "Ouro":
                        try:
                            espaco[l-1][c].append("Brilho")
                        except IndexError:
                            pass
                        try:
                            espaco[l+1][c].append("Brilho")
                        except IndexError:
                            pass
                        try:
                            espaco[l][c-1].append("Brilho")
                        except IndexError:
                            pass
                        try:
                            espaco[l][c+1].append("Brilho")
                        except IndexError:
                            pass
                        
                    
        return espaco            
    
# teste = [[["Wumpus", "Vento"],2,3],[4,5,6],[7,8,9],[10,11,12]]
# print(teste[0][0][0])
novo = Ambiente(4,4)
espaco = novo.criar()
for linha in espaco:
    print(linha)