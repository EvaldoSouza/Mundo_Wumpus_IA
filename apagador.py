
def apaga_bc():
        
        bc = open('knowlede_base.txt', 'w')
        bc.write("#base de conhecimento do mundo de Wumpus\n")
        bc.close

def apaga_pensamento():
    bc = open('pensamento.txt', 'w')
    bc.close

apaga_bc()
apaga_pensamento()