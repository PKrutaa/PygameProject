import pygame

#o lado_celula só ta ai no que tange a pegar posição do mouse e pra front end
# contornar fácil isso e n precisar disso como parametro 
def laco_jogo(matriz_laco, lado_celula_laco):
    pygame.init()

    jogo_interrompido = False
    vitoria_jogador1 = False
    vitoria_jogador2 = False
    empate = False
    celulas_abertas = 0
    pontos_jogador1 = 0
    pontos_jogador2 = 0
    n_rodadas = 0

   
  
    while not jogo_interrompido:
        for evento in pygame.event.get():
           
            if evento.type == pygame.QUIT:
                jogo_interrompido = True
                break
            
            #quando alguém ganha ele fica infinito na capitação de evento mas n faz nada abaixo disso,
            # vc fica la no grid sem pode fazer nada, cuidado quando colocar algo dps desse if pq pode ficar
            #num puta loop
            if vitoria_jogador1 or vitoria_jogador2 or empate:
                continue

            #essa mudança de tela pode virar uma função 
            mudança_tela = False

            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                mouse_x, mouse_y = evento.pos


                celula_x = mouse_x // lado_celula_laco  
                celula_y = mouse_y // lado_celula_laco

                if celula_y > len(matriz_laco) - 1:
                    continue

                    #as células abertas recebem true, então se ja ta aberta não entra aqui
                if matriz_laco[celula_x][celula_y] is not True:
                    mudança_tela = True
                    celulas_abertas += 1
                    n_rodadas += 1
                   
                    print(matriz_laco)
                    print(celulas_abertas, len(matriz_laco) ** 2)
                    print(n_rodadas)
                      
                    #caso de ter encontrado buraco
                    if matriz_laco[celula_x][celula_y] == "B":
                        
                        #os pontos não podem ficar negativos, então eu retorno a 0 quando fica negativo
                        #fiz isso para os 2 jogadores logo abaixo
                        if n_rodadas % 2 == 0:
                            pontos_jogador2 -= 50
                            
                            if pontos_jogador2 < 0:
                                pontos_jogador2 = 0
                               
                        else:
                            pontos_jogador1 -= 50

                            if pontos_jogador1 < 0:
                                pontos_jogador1 = 0
                                
                    #no caso de ter aberto uma que tem tesouro
                    elif matriz_laco[celula_x][celula_y] == "T":

                        if n_rodadas % 2 == 0:
                            pontos_jogador2 += 100

                        else:
                            pontos_jogador1 += 100
                     
                  #verifica se todas as células foram abertas e fala quem ganhou
                    if celulas_abertas == len(matriz_laco) ** 2:
                        
                        if pontos_jogador2 > pontos_jogador1:
                            vitoria_jogador2 = True
                            
                        elif pontos_jogador1 == pontos_jogador2:
                            empate = True
                            
                        else:
                            vitoria_jogador1 = True

                    #matriz recebe true quando é aberta 
                    matriz_laco[celula_x][celula_y] = True
                  
            #entra aqui sempre que uma célula foi aberta, essa parte ae tu pode criar uma função pra tirar dai
            #eu só fiz teste com isso, nem leva muito a sério o que tem ai
            if mudança_tela:
                i, j = celula_x, celula_y

                if matriz_laco[i][j] == "T":
                    print("a")
                elif matriz_laco[i][j] == "B":
                    print("b")
                else: print(matriz_laco[i][j])       

        #desconsidere essa chamada dessa função, foi só pra eu ter uma ideia mais ou menos

    pygame.quit()


    