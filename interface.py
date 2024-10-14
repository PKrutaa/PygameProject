import pygame
import sys
import geracao_mapa as gm_mapa
import cores

pygame.font.init()
pygame.init()

# Coletar as informações da tela do usuário para deixar padronizado para cada tela
info = pygame.display.Info() 
screen_width, screen_height = info.current_w, info.current_h
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN) # deixa a tela fullscreen
font = pygame.font.SysFont("JetBrains-Mono", 35) # fonte e tamanho 


# Função para sair do jogo
def quit_game():
    pygame.quit()
    sys.exit()


# Função para desenhar um botão e executar ação se clicado
def draw_button(text, x, y, width, height, inactive_color, action=None):

    mouse = pygame.mouse.get_pos()  # Posição do mouse
    click = pygame.mouse.get_pressed()  # Estado de clique do mouse

    # Verificar se o mouse está sobre o botão
    if x < mouse[0] < x + width and y < mouse[1] < y + height: 
        pygame.draw.rect(screen, inactive_color, (x, y, width, height), 0, border_radius=10)  # Desenha retângulo cheio
        if click[0] == 1 and action is not None:  # Se o botão esquerdo for clicado
            som_botao = pygame.mixer.Sound('Musicas/som_botao.wav')
            som_botao.play()
            print(f"Botão {text} clicado!")  # Exibir no console para confirmar o clique
            return action()  # Retorna o valor da função 'action'
    else:
        pygame.draw.rect(screen, inactive_color, (x, y, width, height), 1, border_radius=10)  # Desenha borda do retângulo

    # Desenhar o texto no botão
    text_surf = font.render(text, True, cores.AMARELO)
    text_rect = text_surf.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(text_surf, text_rect)

# Função da tela inicial (homepage)
def homepage():

    # Carregar a imagem de fundo

    background_image = pygame.image.load(r'Imagens\wallpaper.jpg')
    background_image = pygame.transform.scale(background_image, (screen_width, screen_height))
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)

    rodando = True
    while rodando:
        screen.fill((0,0,0))
        screen.blit(background_image, (0, 0))  # Desenha a imagem de fundo

        # Desenhar botões e capturar retorno de ações
        result = draw_button("Start", screen_width // 2 - 80, screen_height-800 , 150, 50, (66, 133, 244), action=interPage) #AQUI JOÃO
        if result is not None:
            print(f"Transição para: {result}")  # Verifica qual valor foi retornado
            return result  # Se houver um valor retornado, ele será a nova tela a ser exibida

        draw_button("Quit", screen_width // 2 - 80, screen_height-200, 150, 50, (66, 133, 244), action=quit_game)

        # Gerenciar eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit_game()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    quit_game()

        pygame.display.update()  # Atualizar a tela

# Função da tela de jogo (startPage)
def startPage(linhas):

    # Carregar a imagem de fundo
    background_image = pygame.image.load(r'Imagens\wallpaper.jpg')
    background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

    # Carregar imagens dos elementos do jogo
    img_buraco = pygame.image.load(r'Imagens\buraco.png')
    img_tesouro = pygame.image.load(r'Imagens\tesouro.png')


    pontuacao_jogador1 = 0
    pontuacao_jogador2 = 0
    count_jogadas = 0

    # Obter o número de linhas do usuário

    # Calcular o lado da célula
    lado_celula = min(screen_width, screen_height) // linhas

    # Redimensionar imagens de acordo com o tamanho do lado da célula
    img_buraco = pygame.transform.scale(img_buraco, (lado_celula, lado_celula))
    img_tesouro = pygame.transform.scale(img_tesouro, (lado_celula, lado_celula))

    # Chama a função do geracao_mapa para construir a matriz do jogo
    matriz_laco = gm_mapa.geracao_matriz(linhas)  

    # Lógica de abrir células a partir de uma matriz False
    celulas_abertas = [[False] * linhas for _ in range(linhas)]

    # Define a fonte para a pontuação,numero de tesouros e mensagem final
    font_ntesouros = pygame.font.SysFont('JetBrains-Mono', 70)
    font = pygame.font.SysFont('JetBrains-Mono', 36)
    font_final = pygame.font.SysFont('JetBrains-Mono', 72)  # Fonte maior para mensagem final

    # Calcular a posição inicial para centralizar o tabuleiro
    x_offset = (screen_width - (linhas * lado_celula)) // 2
    y_offset = (screen_height - (linhas * lado_celula)) // 2

    # Loop da parte visual do jogo
    rodando = True
    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                mouse_x, mouse_y = evento.pos
                
                # Calcular as coordenadas da célula
                celula_x = (mouse_y - y_offset) // lado_celula
                celula_y = (mouse_x - x_offset) // lado_celula

                # Verificar se as coordenadas estão dentro dos limites e se a célula já não foi aberta
                if 0 <= celula_x < linhas and 0 <= celula_y < linhas and not celulas_abertas[celula_x][celula_y]:
                    # Abrir a célula e atualizar a jogada
                    celulas_abertas[celula_x][celula_y] = True  
                    count_jogadas += 1

                    # Atualizar pontuação com base no conteúdo da célula
                    # Pontuação não pode ficar negativa
                    if matriz_laco[celula_x][celula_y] == "B":
                        if count_jogadas % 2 == 0:
                            pontuacao_jogador1 -= 50
                            if pontuacao_jogador1 < 0:
                                pontuacao_jogador1 = 0
                        else:
                            pontuacao_jogador2 -= 50
                            if pontuacao_jogador2 < 0:
                                pontuacao_jogador2 = 0

                    elif matriz_laco[celula_x][celula_y] == "T":
                        if count_jogadas % 2 == 0:
                            pontuacao_jogador1 += 100
                        else:
                            pontuacao_jogador2 += 100

        # Redesenhar a tela a cada iteração
        screen.blit(background_image, (0, 0))  

        # Revelar as imagens/números de acordo com as interações do usuário
        for i in range(linhas):
            for j in range(linhas):
                x = x_offset + j * lado_celula
                y = y_offset + i * lado_celula
            
                if celulas_abertas[i][j]:
                    if matriz_laco[i][j] == "B":
                        screen.blit(img_buraco, (x, y))

                    elif matriz_laco[i][j] == "T":
                        screen.blit(img_tesouro, (x, y))

                    else:
                        # Renderiza o número com fundo transparente
                        text_surface = font_ntesouros.render(str(matriz_laco[i][j]), True, cores.AMARELO)
                        text_rect = text_surface.get_rect(center=(x + lado_celula // 2, y + lado_celula // 2))
                        screen.blit(text_surface, text_rect)  # Coloca o texto na tela

                # Desenhar o contorno do quadrado
                pygame.draw.rect(screen, (0, 0, 0), (x, y, lado_celula, lado_celula), 2)

        # Exibir a pontuação na tela 
        score_surface1 = font.render(f'Jogador 1: {pontuacao_jogador2}', True, cores.AMARELO)
        screen.blit(score_surface1, (screen_width//10, screen_height//5))

        score_surface2 = font.render(f'Jogador 2: {pontuacao_jogador1}', True, cores.AMARELO)
        screen.blit(score_surface2, (screen_width//2+(screen_width//3), screen_height//5))
        pygame.display.update()

        # Verificar se todas as células foram abertas para finalizar o jogo
        todas_celulas_abertas = all(all(celulas_abertas[i][j] for j in range(linhas)) for i in range(linhas))

        if todas_celulas_abertas:
            final(pontuacao_jogador1,pontuacao_jogador2,font_final)
            
    pygame.display.update()

    pygame.quit()



# Tela final do jogo
def final(pontuacao_jogador1, pontuacao_jogador2, font_final):
    # Carregar o background
    background_final = pygame.image.load(r'Imagens\background_final.jpg')
    background_final = pygame.transform.scale(background_final, (screen_width, screen_height))

    # Determinar o vencedor
    if pontuacao_jogador1 > pontuacao_jogador2:
        mensagem = "Jogador 1 Ganhou!"
        pygame.mixer.init()
        pygame.mixer.music.load(r"Musicas\vitoria.wav")
        pygame.mixer.music.play(0)
    elif pontuacao_jogador1 < pontuacao_jogador2:
        mensagem = "Jogador 2 Ganhou!"
        pygame.mixer.init()
        pygame.mixer.music.load(r"Musicas\vitoria.wav")
        pygame.mixer.music.play(0)
    else:
        mensagem = "Empate!"
        pygame.mixer.init()
        pygame.mixer.music.load(r"Musicas\angra.wav")
        pygame.mixer.music.play(0)

    # Mostrar o background e a mensagem de fim de jogo
    screen.blit(background_final, (0, 0))  # Exibir o background antes de qualquer outra coisa

    # Renderizar a mensagem de fim de jogo
    mensagem_surface = font_final.render(mensagem, True, (255, 255, 255))
    mensagem_rect = mensagem_surface.get_rect(center=(screen_width // 2, screen_height // 2))
    screen.blit(mensagem_surface, mensagem_rect)

    # Desenhar o botão "Jogar novamente"
    draw_button("Jogar novamente", screen_width // 2 - 150, (screen_height * 1//3) , 300, 75, cores.AMARELO, action=homepage)
    pygame.display.update()  # Atualizar a tela para mostrar background, mensagem e botão

    #desenhar o botão "quit"
    draw_button("Quit", screen_width // 2 - 50, (screen_height * 2//3) , 100, 50, cores.AMARELO , action=quit_game)
    # Esperar por um evento de fechamento ou clique para sair

    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT or (evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1):
                esperando = False
        pygame.display.update()




# Função para criar uma caixa de entrada de texto
def draw_input_box(x, y, width, height, text):

    # Certifique-se de que o texto é uma string
    if not isinstance(text, str):
        text = str(text)  # Converte para string se necessário

    # Desenhar a caixa de entrada
    pygame.draw.rect(screen, (200, 200, 200), (x, y, width, height), 0, border_radius=5)

    # Renderizar o texto usando a fonte
    text_surface = font.render(text, True, (0, 0, 0))

    # Exibir o texto na caixa de entrada
    screen.blit(text_surface, (x + 5, y + 5))  # Texto com um espaçamento de 5 pixels das bordas

    # Atualizar a tela para refletir as mudanças
    pygame.display.update()




#função para desenhar um texto com borda
def draw_text_with_border(text, font, text_color, border_color, pos):
    # Renderizar a borda (desenhando o texto várias vezes ao redor do centro)
    font = pygame.font.SysFont("JetBrains-Mono", 40)

    text_surface = font.render(text, True, border_color)

    for offset in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
        screen.blit(text_surface, (pos[0] + offset[0], pos[1] + offset[1]))

    # Renderizar o texto principal
    text_surface = font.render(text, True, text_color)
    screen.blit(text_surface, pos)




# Função da tela intermediária (interPage)
def interPage():
    font = pygame.font.SysFont("JetBrains-Mono", 40,)

    linhas = "4"  # Inicializar 'linhas' como string

    # Carregar a imagem de fundo
    background_image = pygame.image.load(r'Imagens\wallpaper.jpg')
    background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

    # Iniciar o mixer e tocar música

    rodando = True
    while rodando:
        screen.blit(background_image, (0, 0))  # Desenha a imagem de fundo

        draw_button("Iniciar jogo", (screen_width //2)-150, (screen_height*2)//3 +50, 300, 50, (66, 133, 244), action=lambda: startPage(int(linhas)))  # Converter 'linhas' para inteiro
        draw_text_with_border("Digite a quantidade de linhas para o tabuleiro!", "JetBrains-Mono", (255,255,255), (0,0,0), ((screen_width//2)-325, (screen_height//2-50)))
        draw_input_box((screen_width // 2)-150, (screen_height//2), 300, 50, str(linhas))

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit_game()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    homepage()

                # Captura o texto digitado na caixa de entrada e atribui à variável 'linhas'
                if evento.unicode.isnumeric():  # Aceitar apenas números
                    linhas += evento.unicode
                if evento.key == pygame.K_BACKSPACE and len(linhas) > 0:  # Corrige o erro ao pressionar backspace
                    linhas = linhas[:-1]  # Remover o último caractere de 'linhas'

                # Se pressionar Enter, imprime o valor de 'linhas'
                if evento.key == pygame.K_RETURN:
                    print(f"Linhas: {linhas}")

        pygame.display.update()  # Atualizar a tela