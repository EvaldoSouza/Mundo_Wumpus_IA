def vizinhos(coordenadas, dimensoes):
    #coordenadas é uma lista no formato [1,1]
    #dimensoes tmb

    # norte = [coordenadas[0]-1, coordenadas[1]]
    # leste = [coordenadas[0], coordenadas[1]+1]
    # sul = [coordenadas[0]+1, coordenadas[1]]
    # oeste = [coordenadas[0], coordenadas[1]-1]
    vizin = [[coordenadas[0]-1, coordenadas[1]], [coordenadas[0], coordenadas[1]+1], [coordenadas[0]+1, coordenadas[1]], [coordenadas[0], coordenadas[1]-1] ]

    for posicao in vizin:
        if posicao[0] < 0 or posicao[1] < 0:
            vizin.remove(posicao)
        if posicao[0] > dimensoes[0]:
            vizin.remove(posicao)
        if posicao[1] > dimensoes[1]:
            vizin.remove(posicao)
    
    return vizin

