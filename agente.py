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
        self.ouro = False
        self.lado_que_olho = [0,1]
        self.posicao_atual = [0,0]
        self.lista_visitados = [] #salvando quadrados
        self.seguros_inexplorados = [] #será que é util?
        self.perigosos_inexplorados = []
        pass

    #estou criando a caverna aqui...uma boa solução? Não
    def entrar_caverna(self, linhas, colunas):
        caverna = ambiente.Ambiente(linhas, colunas)
        self.caverna = caverna.distribuir()
        self._cachola(linhas, colunas, "Nova")

    #inicializando o motor de inferencias
    def _cachola(self, linhas, colunas, marcar):
        self.pensador = motor.Motor(linhas, colunas)
        self.pensamento = open("pensamento.txt", "a")
    
    #conferindo se é uma parede. Retorna false se for
    def _parede(self):
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
    #retorna true se andou, false se não
    def _andar(self):
        if self._parede():
            self.posicao_atual = self.lado_que_olho
            return True
        
        return False
    
    #recebe  "norte", "sul", "leste", "oeste" e virar
    def _virar(self, direcao):
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

    #retorna o conteudo do quadrado atual
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
        #Não precisa desse check, mas redundância tmb n é tão ruim assim
        if self.caverna[self.posicao_atual[0]][self.posicao_atual[1]].ouro:
            #ativar o caminho de volta
            self.ouro = True
            self._caminhar_para(self.posicao_atual, [0,0])

    def _remove_seguro_inexp(self, atual):
        for seg in self.seguros_inexplorados:
            if atual == seg:
                self.seguros_inexplorados.remove(atual)
                break

    def _adicionar_seguros(self, novos: list):
        for n in novos:
            flag = True
            for seg in self.seguros_inexplorados:
                if seg == n:
                    flag = False
            if flag:
                self.seguros_inexplorados.append(n)
                    
    def _consulta_seguros(self, coord):
        for seg in self.seguros_inexplorados:
            if coord == seg:
                return True
        
        return False
    
    def _consulta_visitado(self, coord):
        for vis in self.lista_visitados:
            if coord == vis:
                return True
        
        return False

    def _remove_perigoso_inexp(self,atual):
        for seg in self.perigosos_inexplorados:
            if atual == seg:
                self.perigosos_inexplorados.remove(atual)
                break
    
    def _adicionar_perigoso_inexp(self, novos: list):
        for n in novos:
            flag = True
            for seg in self.perigosos_inexplorados:
                if seg == n:
                    flag = False
            if flag:
                self.perigosos_inexplorados.append(n)
    
    #retorna o perigoso_inexplorado menos mencionado até então
    def _consulta_perigoso(self):
        countado = 999 #o risco tem que inciar em um valor fora do boundary pra começar a seleção
        
        if len(self.perigosos_inexplorados) > 0:
            candidato = self.perigosos_inexplorados[0]
        else:
            return [0,0] #se n tiver nenhum perigoso inexplorado, acabou a exploração, e o ouro esta fora de alcance

        for p in self.perigosos_inexplorados:
            risco_p = self.perigosos_inexplorados.count(p)
            if risco_p < countado:
                candidato = p
        
        return candidato
    

    def analisar_vizinhos(self):
        dados_atual = self.olhar_quadrado()
        self.lista_visitados.append(self.posicao_atual)
        self._remove_seguro_inexp(self.posicao_atual)
        self._remove_perigoso_inexp(self.posicao_atual)
        vizinhos = utils.vizinhos(self.posicao_atual, [4,4])
        self.pensador.inferir(self.posicao_atual, dados_atual) #escreve na base os pensamentos
        conhecimento = self.pensador.fatos(self.posicao_atual)
        inferencias = self.pensador.deducoes(self.posicao_atual)

        #criar uma lista de quadrados seguros, coordenadas
        seguros = [] #sempre pode andar para o seguro
        morte = []#nunca pode andar para o morte
        perigosos = []#não dá para se viver sem riscos

        #se a posição atual não tiver nem fedor nem brisa, vizinhos são seguros
        if not self.caverna[self.posicao_atual[0]][self.posicao_atual[1]].fedor and not self.caverna[self.posicao_atual[0]][self.posicao_atual[1]].brisa:
            for v in vizinhos:
                seguros.append(v)

        #pega os seguros
        for dado in conhecimento:
            if dado.find("buraco") != -1 and dado.find("False") != -1:
                fato_coord = dado[5:12]
                seguros.append(fato_coord)
            if dado.find("wumpus") != -1 and dado.find("False") != -1:
                fato_coord = dado[5:12]
                seguros.append(fato_coord)
        
        self._adicionar_seguros(seguros)
        
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
        
        self._adicionar_perigoso_inexp(perigosos)

        #anotando as paradas tudo, para facilitar os testes?
        self.pensamento.write(str(seguros)+'\n')
        self.pensamento.write(str(morte)+'\n')
        self.pensamento.write(str(perigosos)+'\n')
        self.pensamento.write("Percepts Atuais:")
        self.pensamento.write(str(dados_atual)+'\n')

    
    def proximo_passo(self):
        
        vizinhos = utils.vizinhos(self.posicao_atual, [4,4]) #trocar por valores variaveis
        #tenho uma lista com os seguros, com os perigosos e com os mortes...n tenho com os morte!
        #explorar um dos seguros, ou um dos perigosos

        #escrever a posição atual, o conhecimento e as inferencias em um txt

        #tomar as decisões
        #se tiver um quadrado seguro ao lado, ir pra ele...apenas se não foi explorado!
        #decide pelo vizinho seguro não explorado. Se n tiver seguro, 
        for v in vizinhos:
            if self._consulta_seguros(v):
                self._caminhar_para(self.posicao_atual, v)
                self.pensamento.write("Indo para:")
                self.pensamento.write(str(v))
                return True
        
        if len(self.seguros_inexplorados) > 0:
            print(self.seguros_inexplorados)
            self._caminhar_para(self.posicao_atual, self.seguros_inexplorados[0])
            self.pensamento.write("Indo para: ")
            self.pensamento.write(self.seguros_inexplorados[0])
            return True
        
        #arriscar
        arriscado = self._consulta_perigoso()

        #consulta_perigoso retorna [0,0] se não tiver mais nenhum lugar para explorar
        if arriscado != [0,0]:
            self._caminhar_para(self.posicao_atual, arriscado)
            self.pensamento.write("Arriscando em: ")
            self.pensamento.write(arriscado)
            return True
        elif self.wumpus: #se não tem mais nenhum quadrado para explorar, tenta matar o wumpus, e explora
            #tentar matar o wumpus...fazer depois de por pra funcionar
            #
            # KILL COMMAND
            #
            return False
        else: #se o wumpus esta morto, e msm assim n encontrou ouro, é pq ta inalcançvel, então sai da caverna
            self._caminhar_para(self.posicao_atual, arriscado)
            self.pensamento.write("Não Achei")
            return False


    def _caminhar_para(self, atual, destino):
        #começar na atual, e ir para o desstino
        #fazer ela recursiva? Sim!
        #se a linha_atual for menor que destino, virar sul, else virar norte
        #se a coluna atual for menor que destino, virar oeste, else, virar sul
        #depois que virou, conferir se o quadrado é seguro (list check) e chama o andar
        #e chama de novo a caminhar_para, com o novo quadrado
        #direções = ["norte", "leste", "sul", "oeste"]

        #condição de parada
        if atual == destino:
            #escrever em algum lugar que saiu com sucesso
            return 
        
        virar_para=[]

        #linhas são n-s, colunas o-l. Se menor, n,o. Maior s-l
        #pq <=? Pq se topar com um buraco ou wumpus, precisa de outra direção pra virar, ai tenta manter a direção
        if atual[0] <= destino[0]:
            virar_para.append("norte")
        else:
            virar_para.append("sul")
        
        if atual[1] <= destino[1]:
            virar_para.append("oeste")
        else:
            virar_para.append("leste")
        
        self._virar(virar_para[0])
        #tento ir pra um lado
        if self._andar():
            self._caminhar_para(self.posicao_atual, destino)
            return

        #se n der certo, vou pro outro
        self._virar(virar_para[1])
        del virar_para[0:2] #esvaziando a lista do que já foi tentado

        if self._andar():
            self._caminhar_para(self.posicao_atual, destino)
            return
        
        #se não achei nenhum quadrado seguro indo pro lado certo, tenta pro outro lado
        if len(virar_para) == 0:
            if atual[0] >= destino[0]:
                virar_para.append("norte")
            else:
                virar_para.append("sul")
        
            if atual[1] >= destino[1]:
                virar_para.append("oeste")
            else:
                virar_para.append("leste")

        self._virar(virar_para[0])
        #tento ir pra um lado
        if self._andar():
            self._caminhar_para(self.posicao_atual, destino)
            return

        #se n der certo, vou pro outro
        self._virar(virar_para[1])
        del virar_para[0:2] #esvaziando a lista do que já foi tentado

        if self._andar():
            self._caminhar_para(self.posicao_atual, destino)
            return

#como fazer esse agente?
#preciso me mover pelo ambiente
#---o ambiente é uma matriz, então eu me "movo" somando e subtraindo das posições?


#preciso passar essas informações para o motor
#preciso receber do motor deduções
#com base nessas deduções, preciso tomar decisões para onde me mover ou o que fazer
#---essa é a parte mais dificil. Porem tem que ser a ultima, já que precisa das outras

