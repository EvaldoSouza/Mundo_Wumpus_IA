#o que fazer no agente?
#preciso do sensor, do atuador, motor de inferencia e base de conhecimento fazer separado
#o agente pega as informações do sensor, passa para o motor, pegar as respostas do motor, e passa para o atuador
from unittest import case
import sensor
import motor
import ambiente



class Agete:
    def __init__(self) -> None:
        self.caverna = None
        self.lado_que_olho = [0,1]
        self.posicao_atual = [0,0]
        pass

    def entrar_caverna(self, linhas, colunas):
        caverna = ambiente.Ambiente(linhas, colunas) #receber isso depois
        caverna.distribuir()
        self.caverna = caverna

    def cachola(self, linhas, colunas):
        self.pensador = motor.Motor(linhas, colunas)
    
    #conferindo se é uma parede. Retorna false se for
    def parede(self):
        linhas = len(self.caverna)
        colunas = len(self.caverna[0])
        if self.lado_que_olho[0] > linhas or self.lado_que_olho[1] > colunas:
            return False
        elif self.lado_que_olho[0] < 0 or self.lado_que_olho[1] < 0:
            return False
        else:
            return True
    
    #ando um quadrado pra frente, ou seja, troco posição atual com lado que olho
    #conferindo se tem parede antes de andar
    def andar(self):
        if self.parede():
            self.posicao_atual = self.lado_que_olho
    
    #recebe  "norte", "sul", "leste", "oeste" e virar
    def virar(self, direcao):
        linha_atual = self.posicao_atual[0]
        coluna_atual = self.posicao_atual[1]
        if direcao == "norte":
            self.lado_que_olho = [linha_atual - 1, coluna_atual]
        elif direcao == "leste":
            self.lado_que_olho = [linha_atual, coluna_atual+1]
        elif direcao == "sul":
            self.lado_que_olho = [linha_atual +1, coluna_atual]
        elif direcao == "oeste":
            self.lado_que_olho = [linha_atual, coluna_atual -1]

    def olhar_quadrado(self):
        #esse local é um Quadrado
        local = self.caverna[self.posicao_atual[0]][self.posicao_atual[1]]
        return local.retorna_dict()
#como fazer esse agente?
#preciso me mover pelo ambiente
#---o ambiente é uma matriz, então eu me "movo" somando e subtraindo das posições


#preciso passar essas informações para o motor
#preciso receber do motor deduções
#com base nessas deduções, preciso tomar decisões para onde me mover ou o que fazer
#---essa é a parte mais dificil. Porem tem que ser a ultima, já que precisa das outras

