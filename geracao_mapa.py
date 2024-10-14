import random

def geracao_matriz (linhas):

    # Criação da matriz

    celula = [[None for i in range (linhas)] for j in range (linhas)]

    n_buracos = int((linhas**2) * 0.1875) # Quantidade de buracos em função das linhas
    n_tesouros = int((linhas**2) * 0.375) # Quantidade de tesouros em função das linhas
    
    buracos = 0
    # Alocação aleatoria dos buracos na matriz
    while buracos < n_buracos:
        i = random.randint(0, linhas-1)
        j = random.randint(0, linhas-1)

        if celula[i][j] == "B":
            continue
        if celula[i][j] is None:
            celula[i][j] = "B"
            buracos += 1


    # Alocação aleatória dos tesouros na matriz
    tesouros = 0
    while tesouros < n_tesouros:
        i = random.randint(0, linhas-1)
        j = random.randint(0,linhas-1)

        if celula[i][j] == "B" or celula[i][j] == "T":
            continue
        else: celula[i][j] = "T"
        tesouros += 1
        
    # Colocar número de tesouros ao redor da célula
    for i in range (linhas):
        for j in range (linhas):

            if celula[i][j] is None:

                buracos_proximos = 0
                if i-1 >= 0 and celula[i-1][j] == "T":
                    buracos_proximos += 1

                if j-1 >= 0 and celula [i][j-1] == "T":
                    buracos_proximos += 1

                if i+1 < linhas and celula[i+1][j] == "T":
                    buracos_proximos += 1

                if j+1 < linhas and celula[i][j+1] == "T":
                    buracos_proximos += 1

                celula[i][j] = buracos_proximos

    return celula

