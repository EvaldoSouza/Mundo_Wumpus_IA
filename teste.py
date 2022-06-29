#preciso de um jeito para contar quantas vezes um quadrado perigoso é mencionado
#estão armazenados em uma lista, apenas com as coordenadas, não quero fazer um tuple
#não arrisco um vizinho perigoso de cara!
#o arriscar perigo é global!
import ambiente

cav = ambiente.Ambiente(4,4)
caverna = cav._distribuir()
caverna[0][0].imprimir()
#print(caverna[0][0].imprimir)