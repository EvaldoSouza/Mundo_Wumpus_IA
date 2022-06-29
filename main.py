import agente

#fazer aqui as paradas
#o que meu agente precisa ter?
#precisa andar pela caverna
#precisa deduzir os lugares seguros para andar
#precisa atirar no wumpus (tentar fazer um "se necessário", para demonstrar a profundidade da BC)
#precisa pegar o ouro e voltar para a entrada -- o proximo_passo() já faz isso "automatico", antes das inferencias

#preciso fazer um loop que fica andando pela caverna até encontrar o ouro, quando encontrar sai do loop
#se não tiver mais nenhum movimento valido tmb sair do loop...como fazer isso?
#já ta feito na decisão. Falta fazer o kill_command pra sair caçando o wumpus
def main():
    #fazendo primeiro
    heroi = agente.Agete()
    heroi.entrar_caverna(4,4)
    ativo = True
    while ativo:
        if heroi.ouro:
            ativo = False
        
        heroi.analisar_vizinhos()
        heroi.pegar_ouro()
        ativo = heroi.proximo_passo()

if __name__ == "__main__":
    main()
