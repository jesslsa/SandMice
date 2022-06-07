import pygame
from assets.dados.config import *
import random
from classes import *
from assets.dados.assets import load

def gamescreen(window):
    font = pygame.font.SysFont(None, 48)
    #Telas iniciais e finais
    dicionary_assets = load()
    
    def respawnamoedas(state, grupomoedas):
        if state == TROCA_ROUND:
            grupomoedas = ''
            grupomoedas = pygame.sprite.Group()
        while len(grupomoedas) < totalmoedas:
            moeda = coin(dicionary_assets['IMAGE_COIN'],dicionary_assets['SOUND_COIN'])
            grupomoedas.add(moeda)
        if state != INICIO and state != TROCA_ROUND:
            dicionary_assets['SOUND_COIN'].set_volume(EFFECTS_VOLUME_COIN)
            moeda.coin_sound.play()
            
            
        return grupomoedas

    def respawnoqueijo(state, grupoqueijos):
        if state == TROCA_ROUND:
            grupoqueijos = pygame.sprite.Group()
        queijos = coin(dicionary_assets['IMAGE_CHEESE'],dicionary_assets['SOUND_CHEESE'])
        grupoqueijos.add(queijos)
        if state != INICIO and state != TROCA_ROUND:
            queijos.coin_sound.play()
        return grupoqueijos

    def respawnogato(enemies_gato):
        while True:
            NovoInimigo = inimigo([dicionary_assets['IMAGE_CAT'], dicionary_assets['IMAGE_CAT']],dicionary_assets['SOUND_CAT'], '')
            NovoInimigo.rect.centerx = random.randint(CAT_WIDTH, SCREEN_WIDTH - CAT_WIDTH)
            NovoInimigo.rect.bottom = random.randint(CAT_HEIGHT, SCREEN_HEIGHT - CAT_HEIGHT)
            dicionary_assets['SOUND_CAT'].set_volume(EFFECTS_VOLUME_CAT)
            NovoInimigo.cat_sound.play()
            manobra = pygame.sprite.Group()
            manobra.add(NovoInimigo)
            if not pygame.sprite.spritecollide(player, manobra, True):
                enemies_gato.add(NovoInimigo)
                break
            manobra = pygame.sprite.Group()  
        return enemies_gato

    game = True

    estado = INICIO
    # Variável para o ajuste de velocidade
    clock = pygame.time.Clock()
    
    ultimotempo = [0]
    ultimotempogato = [0]
    tempo_respawn_gato = 5000 # A cada 5 segundos

    # Criando um grupo de sprites
    sprites = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    enemies_cat = pygame.sprite.Group()
    moedas = pygame.sprite.Group()
    queijos = pygame.sprite.Group()
    totalmoedas = 3
    # Criando o jogador
    player = jogador(dicionary_assets['IMAGE_MOUSE'],dicionary_assets['SOUND_MOUSE'])

    vovo = inimigo([dicionary_assets['IMAGE_GRANDMA_RIGHT'], dicionary_assets['IMAGE_GRANDMA_LEFT']],'', dicionary_assets['SOUND_GRANDMA'])
    vovo.rect.x = random.randint(60, SCREEN_WIDTH-60)

    perto = True
    while(perto):
        x_enemy = random.randint(60, SCREEN_WIDTH-60)
        if((x_enemy > (player.rect.x + 200)) or (x_enemy < (player.rect.x - 200))):
            perto = False
    vovo.rect.x = x_enemy
    
    sprites.add(player)
    enemies.add(vovo)
    moedas = respawnamoedas(estado, moedas)
    
    Left = 0
    Right = 0
    Up = 0
    Down = 0
    round = 1
    #Tela Inicial

    musica_fundo = False
    colisao = False
    # ===== Loop principal =====
    while game:
        clock.tick(FPS)
        tempo = pygame.time.get_ticks()

        # ----- Trata eventos
        for event in pygame.event.get():

            if(musica_fundo == False):
                pygame.mixer.music.load(dicionary_assets['SOUND_BACKGROUND'])
                pygame.mixer.music.set_volume(BACKGROUND_VOLUME)
                pygame.mixer.music.play(loops=-1)
                musica_fundo = True
                pygame.time.set_timer(ALTERA_MOVIMENTO_VOVO, 100)

            if estado == INICIO:
                pygame.mixer.music.load(dicionary_assets['SOUND_BACKGROUND_INTRO'])
                pygame.mixer.music.play(loops=-1)
                round = 1
                Left = 0
                Right = 0
                Up = 0
                Down = 0
                player.speedx = 0
                player.speedy = 0
                tempo = pygame.time.get_ticks()
                window.blit(dicionary_assets['START_IMAGE'], (0, 0))
                player.moedas = 0
                player.queijos = 0
                ultimotempo.append(tempo)
                ultimotempogato.append(tempo)
                pygame.display.update()
                while estado == INICIO:
                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN:
                            estado = TROCA_ROUND
                        if event.type == pygame.QUIT:
                            estado = FIM
                            game = False

            # ----- Verifica consequências
            if estado == JOGANDO:
                if len(queijos) < 1:
                    queijo = coin(dicionary_assets['IMAGE_CHEESE'],dicionary_assets['SOUND_CHEESE'])
                    queijos.add(queijo)

                if tempo-ultimotempogato[-1] > tempo_respawn_gato:
                    ultimotempogato.append(tempo)
                    enemies_cat = respawnogato(enemies_cat)
                    pygame.time.set_timer(ALTERA_MOVIMENTO_GATO, 500)

                if event.type == ALTERA_MOVIMENTO_GATO:
                    for gato in enemies_cat:
                        direita_esquerda = random.randint(0,2)
                        cima_baixo = random.randint(0,2)
                        if direita_esquerda == 1:
                            gato.speedx = SPEED_ENEMIES
                        if direita_esquerda == 2:
                            gato.speedx = -SPEED_ENEMIES
                        if direita_esquerda == 0:
                            gato.speedx = 0
                        if cima_baixo == 1:
                            gato.speedy = SPEED_ENEMIES
                        if cima_baixo == 2:
                            gato.speedy = -SPEED_ENEMIES
                        if cima_baixo == 0:
                            gato.speedy = 0

                if event.type == ALTERA_MOVIMENTO_VOVO:
                    pvovo_x = vovo.rect.x
                    pvovo_y = vovo.rect.y

                    pplayer_x = player.rect.x
                    pplayer_y = player.rect.y
            
                    if pvovo_x > pplayer_x:
                        vovo.speedx = -SPEED_ENEMIES

                    if pvovo_x < pplayer_x:
                        vovo.speedx = SPEED_ENEMIES
                    if pvovo_y > pplayer_y:
                        vovo.speedy = -SPEED_ENEMIES
                    if pvovo_y < pplayer_y:
                        vovo.speedy = SPEED_ENEMIES
                
            if event.type == pygame.QUIT:
                game = False

            if estado == TROCA_ROUND:
                pygame.mixer.music.load(dicionary_assets['SOUND_BACKGROUND'])
                pygame.mixer.music.play(loops=-1)
                Left = 0
                Right = 0
                Up = 0
                Down = 0
                player.speedx = 0
                player.speedy = 0
                if round > QUANTITY_ROUNDS:
                    estado = FIM
                else:
                    texto_round = font.render('ROUND {0}'.format(round), True, WHITE)
                    round += 1
                    window.fill(BLACK)
                    window.blit(texto_round, (SCREEN_WIDTH/2-70,SCREEN_HEIGHT/2-70))
                    pygame.display.update()
                    pygame.time.delay(2000)
                    tempo = pygame.time.get_ticks()
                    ultimotempo.append(tempo)
                    ultimotempogato.append(tempo)
                    
                    player.rect.centerx = SCREEN_WIDTH/2
                    player.rect.bottom = SCREEN_HEIGHT - 40
                    moedas = respawnamoedas(estado, moedas)

                    estado = JOGANDO

            if estado == FIM:
                if player.moedas >= 50 and player.queijos >= 30:
                    window.blit(dicionary_assets['IMAGE_VICTORY'], (0,0))
                    text_moedas = font.render(f'{player.moedas}', True, YELLOW)
                    text_queijos = font.render(f'{player.queijos}', True, YELLOW)
                    window.blit(text_queijos, (160, 340))
                    window.blit(text_moedas, (160, 420))
                    pygame.display.update()
                else:
                    window.blit(dicionary_assets['IMAGE_GAME_OVER'], (0,0))
                    text_moedas = font.render(f'{player.moedas}', True, YELLOW)
                    text_queijos = font.render(f'{player.queijos}', True, YELLOW)
                    window.blit(text_queijos, (160, 340))
                    window.blit(text_moedas, (160, 420))
                    pygame.display.update()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        estado = INICIO
                    if event.key == pygame.K_ESCAPE:
                        game = False

            if estado == JOGANDO:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT and Left == 0:
                        player.speedx -= SPEED_PLAYER
                        Left += 1
                    if event.key == pygame.K_RIGHT and Right == 0:
                        player.speedx += SPEED_PLAYER
                        Right += 1
                    if event.key == pygame.K_UP and Up == 0:
                        player.speedy -= SPEED_PLAYER
                        Up += 1
                    if event.key == pygame.K_DOWN and Down == 0:
                        player.speedy += SPEED_PLAYER
                        Down += 1
                # Verifica se soltou alguma tecla.
                if event.type == pygame.KEYUP:
                    # Dependendo da tecla, altera a velocidade.
                    if event.key == pygame.K_LEFT and Left == 1:
                        player.speedx += SPEED_PLAYER
                        Left -= 1
                    if event.key == pygame.K_RIGHT and Right == 1:
                        player.speedx -= SPEED_PLAYER
                        Right -= 1
                    if event.key == pygame.K_UP and Up == 1:
                        player.speedy += SPEED_PLAYER
                        Up -= 1
                    if event.key == pygame.K_DOWN and Down == 1:
                        player.speedy -= SPEED_PLAYER
                        Down -= 1
                    
        sprites.update()
        enemies.update()
        enemies_cat.update()
        pontuacao = font.render('Pontos: {0}'.format(player.moedas), True, BLACK)
        display_queijos = font.render('Queijos: {0}'.format(player.queijos), True, BLACK)
        texto_tempo = font.render('{0:.1f} s'.format((tempo - ultimotempo[-1])/1000), True, BLACK)

        if pygame.sprite.spritecollide(player, enemies, True, pygame.sprite.collide_mask):
            dicionary_assets['SOUND_GRANDMA'].set_volume(EFFECTS_VOLUME_GRANDMA)
            vovo.vovo_sound.play()
            colisao = True


        if pygame.sprite.spritecollide(player, enemies_cat, True, pygame.sprite.collide_mask):
            player.sound_caught.play()
            colisao = True

        if colisao: #Se colisao com inimigo -> morte
            colisao = False
            musica_fundo = False
            estado = TROCA_ROUND

            enemies_cat = pygame.sprite.Group()
            enemies = pygame.sprite.Group()
            queijos = pygame.sprite.Group()

            vovo = inimigo([dicionary_assets['IMAGE_GRANDMA_RIGHT'], dicionary_assets['IMAGE_GRANDMA_LEFT']],'', dicionary_assets['SOUND_GRANDMA'])

            perto = True
            while(perto):
                x_enemy = random.randint(60, SCREEN_WIDTH-60)
                if((x_enemy > (player.rect.x + 200)) or (x_enemy < (player.rect.x - 200))):
                    perto = False
            vovo.rect.x = x_enemy

            enemies.add(vovo)
            
            sprites.add(player)

            

        if pygame.sprite.spritecollide(player, moedas, True): #Se colisao com moeda -> ganha moeda e cria uma nova moeda
            player.moedas += 1
            moedas = respawnamoedas(estado, moedas)

        if pygame.sprite.spritecollide(player, queijos, True): #Se colisao com queijo -> ganha queijo e cria uma nova moeda
            player.queijos += 1
            queijos = respawnoqueijo(estado, queijos)

        # ----- Gera saídas
        if estado == JOGANDO:

            window.blit(dicionary_assets['IMAGE_BACKGROUND'],(0,0)) # Coloca o dicionary_assets['IMAGE_BACKGROUND']
            
            moedas.draw(window)
            queijos.draw(window)
            sprites.draw(window)
            enemies.draw(window)
            enemies_cat.draw(window)
            
            window.blit(pontuacao, (230, 630))
            window.blit(display_queijos, (450, 630))
            window.blit(texto_tempo, (10, 630))

        # ----- Atualiza estado do jogo
        pygame.display.update()  # Mostra o novo frame para o jogador