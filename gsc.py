import pygame
from assets.dados.parametros import *
import random

def gamescreen(window):
    font = pygame.font.SysFont(None, 48)
    #Telas iniciais e finais
    IMGINICIAL = pygame.image.load('assets/imagens/SandMice.png').convert()
    #Player 1 - Rato
    IMG = pygame.image.load('assets/imagens/mouse-face.png').convert_alpha()
    IMG = pygame.transform.scale(IMG, (IMG_WIDTH, IMG_HEIGHT))
    #Player 2 - Inimigo
    GRANDMA_IMG = pygame.image.load('assets/imagens/grandma.png').convert_alpha()
    GRANDMA_RIGTH = pygame.transform.scale(GRANDMA_IMG, (ENEMY_WIDTH, ENEMY_HEIGHT))
    GRANDMA_LEFT = pygame.transform.flip(GRANDMA_RIGTH, True, False)
    #Moeda
    IMG3 = pygame.image.load('assets/imagens/coin.png').convert_alpha()
    IMG3 = pygame.transform.scale(IMG3, (COIN_WIDTH, COIN_HEIGHT))
    #Queijo
    IMG4 = pygame.image.load('assets/imagens/cheese.png').convert_alpha()
    IMG4 = pygame.transform.scale(IMG4, (COIN_WIDTH, COIN_HEIGHT))
    #Gato Inimigo
    CAT_IMG = pygame.image.load('assets/imagens/cat.png').convert_alpha()
    CAT_RIGTH = pygame.transform.scale(CAT_IMG, (CAT_WIDTH, CAT_HEIGHT))
    CAT_LEFT = pygame.transform.flip(CAT_RIGTH, True, False)
    # background = pygame.image.load('assets/imagens/planodefundo.png').convert()
    IMG5 = pygame.image.load('assets/imagens/cat.png').convert_alpha()
    IMG5 = pygame.transform.scale(IMG5, (CAT_WIDTH, CAT_HEIGHT))
    background = pygame.image.load('assets/imagens/chao2.png').convert()
    background = pygame.transform.scale(background, (WIDTH,HEIGHT))

    # Carrega os sons do jogo
    pygame.mixer.music.load('assets/sons/intro-jogo.mp3')
    pygame.mixer.music.set_volume(0.5)
    cat_sound = pygame.mixer.Sound('assets/sons/gato-som.mp3')
    coin_sound = pygame.mixer.Sound('assets/sons/coin.mp3')
    cheese_sound = pygame.mixer.Sound('assets/sons/crunch_sound.mp3')
    caught_sound = pygame.mixer.Sound('assets/sons/rat-sound.mp3')
    risada_sound = pygame.mixer.Sound('assets/sons/vovo-rindo.mp3')
                        
    # ----- Inicia estruturas de dados
    class jogador(pygame.sprite.Sprite):
        def __init__(self, img, sound):
            pygame.sprite.Sprite.__init__(self)

            self.image = img
            self.mask = pygame.mask.from_surface(self.image)
            self.rect = self.image.get_rect()
            self.rect.centerx = WIDTH/2
            self.rect.bottom = HEIGHT - 40
            self.speedx = 0
            self.speedy = 0
            self.moedas = 0
            self.queijos = 0
            self.pontos = 0
            self.sound_caught = sound

        def update(self):
            self.rect.x += self.speedx
            self.rect.y += self.speedy

            if self.rect.right > WIDTH:
                self.rect.right = WIDTH
            if self.rect.left < 0:
                self.rect.left = 0
            if self.rect.top < 0:
                self.rect.top = 0
            if self.rect.bottom > HEIGHT:
                self.rect.bottom = HEIGHT

    class inimigo(pygame.sprite.Sprite):
        def __init__(self, imgs, cat_sound, riso_sound):
            pygame.sprite.Sprite.__init__(self)
            self.images = imgs
            self.image = imgs[0]
            self.mask = pygame.mask.from_surface(self.image)
            self.rect = self.image.get_rect()
            self.rect.centerx = WIDTH/2
            self.rect.bottom = 0 + 100
            self.speedx = 0
            self.speedy = 0
            self.cat_sound = cat_sound
            self.vovo_sound = riso_sound

        def update(self):
            self.rect.x += self.speedx
            self.rect.y += self.speedy
            i = 0
            if self.speedx < 0:
                i = 1
            elif self.speedx > 0:
                i = 0

            c = self.rect.center
            self.image = self.images[i]
            self.rect = self.image.get_rect()
            self.rect.center = c

            if self.rect.right > WIDTH:
                self.rect.right = WIDTH
            if self.rect.left < 0:
                self.rect.left = 0
            if self.rect.top < 0:
                self.rect.top = 0
            if self.rect.bottom > HEIGHT:
                self.rect.bottom = HEIGHT

    class coin(pygame.sprite.Sprite):
        def __init__(self,img, sound):
            pygame.sprite.Sprite.__init__(self)
            
            self.image = img
            self.rect = self.image.get_rect()
            self.rect.centerx = random.randint(COIN_WIDTH, WIDTH - COIN_WIDTH)
            self.rect.bottom = random.randint(COIN_HEIGHT, HEIGHT - COIN_HEIGHT)
            self.speedx = 0
            self.speedy = 0
            self.coin_sound = sound

    class cheese(pygame.sprite.Sprite):
        def __init__(self,img):
            pygame.sprite.Sprite.__init__(self)
            
            self.image = img
            self.rect = self.image.get_rect()
            self.rect.centerx = random.randint(CHEESE_WIDTH, WIDTH - CHEESE_WIDTH)
            self.rect.bottom = random.randint(CHEESE_HEIGHT, HEIGHT - CHEESE_HEIGHT)
            self.speedx = 0
            self.speedy = 0

    def respawnamoedas(state, grupomoedas):
        if state == TROCA_ROUND:
            grupomoedas = ''
            grupomoedas = pygame.sprite.Group()
        while len(grupomoedas) < totalmoedas:
            moeda = coin(IMG3,coin_sound)
            grupomoedas.add(moeda)
        if state != INICIO and state != TROCA_ROUND:
            coin_sound.set_volume(0.1)
            moeda.coin_sound.play()
            
            
        return grupomoedas

    def respawnoqueijo(state, grupoqueijos):
        if state == TROCA_ROUND:
            grupoqueijos = pygame.sprite.Group()
        queijos = coin(IMG4,cheese_sound)
        grupoqueijos.add(queijos)
        if state != INICIO and state != TROCA_ROUND:
            queijos.coin_sound.play()
        return grupoqueijos

    def respawnogato(enemies_gato):
        while True:
            NovoInimigo = inimigo([CAT_RIGTH, CAT_LEFT],cat_sound, '')
            NovoInimigo.rect.centerx = random.randint(CAT_WIDTH, WIDTH - CAT_WIDTH)
            NovoInimigo.rect.bottom = random.randint(CAT_HEIGHT, HEIGHT - CAT_HEIGHT)
            cat_sound.set_volume(0.3)
            NovoInimigo.cat_sound.play()
            manobra = pygame.sprite.Group()
            manobra.add(NovoInimigo)
            if not pygame.sprite.spritecollide(player, manobra, True):
                enemies_gato.add(NovoInimigo)
                break
            manobra = pygame.sprite.Group()  
        return enemies_gato

    game = True
    pygame.mixer.music.play(loops=-1) # Inicia música de introdução

    INICIO = 0
    JOGANDO = 1
    TROCA_ROUND = 2
    FIM = 3
    ALTERA_MOVIMENTO_GATO = 667
    ALTERA_MOVIMENTO_VOVO = 666

    estado = INICIO
    # Variável para o ajuste de velocidade
    clock = pygame.time.Clock()
    FPS = 60
    vel_padrao_rato = 5
    vel_padrao_vovo = 2
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
    player = jogador(IMG,caught_sound)

    vovo = inimigo([GRANDMA_RIGTH, GRANDMA_LEFT],'', risada_sound)
    vovo.rect.x = random.randint(60, WIDTH-60)

    perto = True
    while(perto):
        x_enemy = random.randint(60, WIDTH-60)
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
    A = 0
    D = 0
    W = 0
    S = 0
    numrounds = 6
    #Tela Inicial

    while estado == INICIO:
        tempo = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                estado = TROCA_ROUND
            if event.type == pygame.QUIT:
                estado = FIM
                game = False
        window.blit(IMGINICIAL, (0, 0))
        ultimotempo.append(tempo)
        ultimotempogato.append(tempo)
        pygame.display.update()


    musica_fundo = False
    colisao = False
    # ===== Loop principal =====
    while game:
        clock.tick(FPS)
        tempo = pygame.time.get_ticks()

        # ----- Trata eventos
        for event in pygame.event.get():

            if(musica_fundo == False):
                pygame.mixer.music.load('assets/sons/musica-jogo.mp3')
                pygame.mixer.music.set_volume(0.4)
                pygame.mixer.music.play(loops=-1)
                musica_fundo = True
                pygame.time.set_timer(ALTERA_MOVIMENTO_VOVO, 100)

            # ----- Verifica consequências
            if len(queijos) < 1:
                queijo = coin(IMG4,cheese_sound)
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
                        gato.speedx = vel_padrao_vovo
                    if direita_esquerda == 2:
                        gato.speedx = -vel_padrao_vovo
                    if direita_esquerda == 0:
                        gato.speedx = 0
                    if cima_baixo == 1:
                        gato.speedy = vel_padrao_vovo
                    if cima_baixo == 2:
                        gato.speedy = -vel_padrao_vovo
                    if cima_baixo == 0:
                        gato.speedy = 0

            if event.type == ALTERA_MOVIMENTO_VOVO:
                pvovo_x = vovo.rect.x
                pvovo_y = vovo.rect.y

                pplayer_x = player.rect.x
                pplayer_y = player.rect.y
        
                if pvovo_x > pplayer_x:
                    vovo.speedx = -vel_padrao_vovo

                if pvovo_x < pplayer_x:
                    vovo.speedx = vel_padrao_vovo
                if pvovo_y > pplayer_y:
                    vovo.speedy = -vel_padrao_vovo
                if pvovo_y < pplayer_y:
                    vovo.speedy = vel_padrao_vovo
            
            if event.type == pygame.QUIT:
                game = False

            if estado == TROCA_ROUND: # Adicionar aqui a mudança de personagem (if numrounds<=3) e tela de fim do jogo (numrounds<=0)
                if numrounds <= 0:
                    pygame.quit()
                texto_round = font.render('ROUND {0}'.format(7-numrounds), True, WHITE)
                numrounds -= 1
                window.fill(BLACK)
                window.blit(texto_round, (WIDTH/2-70,HEIGHT/2-70))
                pygame.display.update()
                pygame.time.delay(2000)
                tempo = pygame.time.get_ticks()
                ultimotempo.append(tempo)
                ultimotempogato.append(tempo)
                A = 0
                D = 0
                W = 0
                S = 0
                player.rect.centerx = WIDTH/2
                player.rect.bottom = HEIGHT - 40
                moedas = respawnamoedas(estado, moedas)

                estado = JOGANDO

            if estado == JOGANDO:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT and Left == 0:
                        player.speedx -= vel_padrao_rato
                        Left += 1
                    if event.key == pygame.K_RIGHT and Right == 0:
                        player.speedx += vel_padrao_rato
                        Right += 1
                    if event.key == pygame.K_UP and Up == 0:
                        player.speedy -= vel_padrao_rato
                        Up += 1
                    if event.key == pygame.K_DOWN and Down == 0:
                        player.speedy += vel_padrao_rato
                        Down += 1
                # Verifica se soltou alguma tecla.
                if event.type == pygame.KEYUP:
                    # Dependendo da tecla, altera a velocidade.
                    if event.key == pygame.K_LEFT and Left == 1:
                        player.speedx += vel_padrao_rato
                        Left -= 1
                    if event.key == pygame.K_RIGHT and Right == 1:
                        player.speedx -= vel_padrao_rato
                        Right -= 1
                    if event.key == pygame.K_UP and Up == 1:
                        player.speedy += vel_padrao_rato
                        Up -= 1
                    if event.key == pygame.K_DOWN and Down == 1:
                        player.speedy -= vel_padrao_rato
                        Down -= 1
                    
        sprites.update()
        enemies.update()
        enemies_cat.update()
        pontuacao = font.render('Pontos: {0}'.format(player.moedas), True, YELLOW)
        display_queijos = font.render('Queijos: {0}'.format(player.queijos), True, YELLOW)
        texto_tempo = font.render('{0:.1f} s'.format((tempo - ultimotempo[-1])/1000), True, YELLOW)

        if pygame.sprite.spritecollide(player, enemies, True, pygame.sprite.collide_mask):
            risada_sound.set_volume(3)
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

            vovo = inimigo([GRANDMA_RIGTH, GRANDMA_LEFT],'', risada_sound)

            perto = True
            while(perto):
                x_enemy = random.randint(60, WIDTH-60)
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

            window.blit(background,(0,0)) # Coloca o background

            sprites.draw(window)
            enemies.draw(window)
            enemies_cat.draw(window)
            moedas.draw(window)
            queijos.draw(window)
            window.blit(pontuacao, (10, 10))
            window.blit(display_queijos, (10, 40))
            window.blit(texto_tempo, (10, 600))

        # ----- Atualiza estado do jogo
        pygame.display.update()  # Mostra o novo frame para o jogador