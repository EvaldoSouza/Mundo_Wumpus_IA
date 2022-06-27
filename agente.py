#o que fazer no agente?
#preciso do sensor, do atuador, motor de inferencia e base de conhecimento fazer separado
#o agente pega as informações do sensor, passa para o motor, pegar as respostas do motor, e passa para o atuador
import motor
import ambiente
import utils

class Agete:
    def __init__(self) -> None:
        self.caverna = None
        self.wumpus = True
        self.atirei = False
        self.lado_que_olho = [0,1]
        self.posicao_atual = [0,0]
        self.lista_visitados = [] #salvando quadrados
        self.seguros_inexplorados = [] #será que é util?
        pass

    def entrar_caverna(self, linhas, colunas):
        caverna = ambiente.Ambiente(linhas, colunas) #receber isso depois
        caverna.distribuir()
        self.caverna = caverna

    def cachola(self, linhas, colunas, marcar):
        self.pensador = motor.Motor(linhas, colunas, marcar)
    
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
    
    def atirar(self):
        self.atirei = True
        #preciso checar todos os quadrados na direção que to olhando
        linha_atual = self.posicao_atual[0]
        coluna_atual = self.posicao_atual[1]

        linhas = len(self.caverna)
        colunas = len(self.caverna[0])

        if self.lado_que_olho[0] < linha_atual:
            #to olhando pra norte
            for i in range(self.lado_que_olho[0], -1, -1):
                if self.caverna[i][coluna_atual].wumpus:
                    self.wumpus = False
                    break
        if self.lado_que_olho[0] > linha_atual:
            #to olhando pro sul
            for i in range(self.lado_que_olho[0], linhas, 1):
                if self.caverna[i][coluna_atual].wumpus:
                    self.wumpus = False
                    break
        if self.lado_que_olho[1] < coluna_atual:
            #to olhando pro oeste
            for i in range(self.lado_que_olho[1], -1, -1):
                if self.caverna[linha_atual][i].wumpus:
                    self.wumpus = False
                    break
        if self.lado_que_olho[1] > coluna_atual:
            #to olhando pro leste
            for i in range(self.lado_que_olho[1], colunas, 1):
                if self.caverna[linha_atual][i].wumpus:
                    self.wumpus = False
                    break

    def pegar_ouro(self):
        if self.caverna[self.posicao_atual[0]][self.posicao_atual[1]].ouro:
            #ativar o caminho de volta
            self.caminho_de_volta()
            return True
        else:
            return False
    
    def caminho_de_volta():
        pass

    def controle_seguros(self, atual):
        for seg in self.seguros_inexplorados:
            if atual == seg:
                self.seguros_inexplorados.pop(atual)
                return

    def adicionar_seguros(self, novos: list):
        for n in novos:
            flag = True
            for seg in self.seguros_inexplorados:
                if seg == n:
                    flag = False
            if flag:
                self.seguros_inexplorados.append(n)
                    
    def consulta_seguros(self, coord):
        for seg in self.seguros_inexplorados:
            if coord == seg:
                return True
        
        return False
    
    def consulta_visitado(self, coord):
        for vis in self.lista_visitados:
            if coord == vis:
                return True
        
        return False

    def proximo_passo(self):
        atual = self.olhar_quadrado()
        self.lista_visitados.append(atual)
        self.controle_seguros(atual)
        vizinhos = utils.vizinhos()
        self.pensador.inferir(self.posicao_atual, atual) #escreve na base os pensamentos
        conhecimento = self.pensador.fatos(self.posicao_atual)
        inferencias = self.pensador.deducoes(self.posicao_atual)


        #criar uma lista de quadrados seguros, coordenadas
        seguros = [] #sempre pode andar para o seguro
        morte = []#nunca pode andar para o morte
        perigosos = []#não dá para se viver sem riscos

        #se a posição atual não tiver nem fedor nem brisa, vizinhos são seguros
        if not self.caverna[self.posicao_atual[0]][self.posicao_atual[1]].fedor and not self.caverna[self.posicao_atual[0]][self.posicao_atual[1]].brisa:
            seguros.append(vizinhos)

        #pega os seguros
        for dado in conhecimento:
            if dado.find("buraco") != -1 and dado.find("False") != -1:
                fato_coord = dado[5:12]
                seguros.append(fato_coord)
            if dado.find("wumpus") != -1 and dado.find("False") != -1:
                fato_coord = dado[5:12]
                seguros.append(fato_coord)
        
        self.adicionar_seguros(seguros)
        
        #pega os morte certa
        for dado in conhecimento:
            if dado.find("buraco") != -1 and dado.find("True") != -1:
                fato_coord = dado[5:12]
                morte.append(fato_coord)
            if self.wumpus: #se o wumpus tiver vivo
                if dado.find("wumpus") != -1 and dado.find("True") != -1:
                    fato_coord = dado[5:12]
                    morte.append(fato_coord)

        #pega os perigosos
        #As deduções são no formato [x,y] (b v w) (T)
        #aqui usa as deduções. Elas podem ser contraditórias?
        #Não tem dedução de False. Então n tem contraditórias
        for deducao in inferencias:
            dedu_coord = deducao[8:15]
            perigosos.append(dedu_coord)

        #tenho uma lista com os seguros, com os perigosos e com os mortes

        #escrever a posição atual, o conhecimento e as inferencias em um txt

        #tomar as decisões
        #se tiver um quadrado seguro ao lado, ir pra ele...apenas se não foi explorado!
        #decide pelo vizinho seguro não explorado
        if len(seguros) > 0:
            for s in seguros:
                if self.consulta_seguros(s):
                    return s

        #se ainda tiver quadrados seguros que não foram explorados, ir para eles
        if len(self.seguros_inexplorados) != 0:
            #ir para o quadrado seguro mais perto, passando por um caminho seguro
            #fazer essa função
            pass
        

        #acabou os quadrados seguros inexplorados
        vizinho_inexplorado = []
        if len(self.seguros_inexplorados) == 0:
            #começa a deduzir. Quanto mais menções na lista de perigosos, menos vontade de ir pra la
            for viz in vizinhos:
                if self.consulta_visitado(viz):
                    pass
                else:
                    vizinho_inexplorado.append(viz)

        #pegando o vizinho menos perigoso da lista dos perigosos
        bom_vizin = vizinho_inexplorado[0]
        periculosidade = perigosos.count(bom_vizin)

        for vizin in vizinho_inexplorado:
            if perigosos.count(vizin) < periculosidade:
                bom_vizin = vizin

        return bom_vizin


#como fazer esse agente?
#preciso me mover pelo ambiente
#---o ambiente é uma matriz, então eu me "movo" somando e subtraindo das posições


#preciso passar essas informações para o motor
#preciso receber do motor deduções
#com base nessas deduções, preciso tomar decisões para onde me mover ou o que fazer
#---essa é a parte mais dificil. Porem tem que ser a ultima, já que precisa das outras

