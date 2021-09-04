import pygame as pg
from pygame import mixer
import random
from math import sqrt

# initialize the pygame
pg.init()

screen = pg.display.set_mode((800, 600))

# background jogo
background = pg.image.load('imagens/brasilia2.jpg')

# menu do jogo
menu_image = pg.image.load('imagens/menu.jpeg')
menu_arrow = pg.image.load('imagens/menu_seta.png')
menu_about = pg.image.load('imagens/sobre.jpeg')

# imagens auxiliares
quadro_fundo = pg.image.load('imagens/quadro_fundo.jpg')
coracao = pg.image.load('imagens/coracao.png')
coracao2 = pg.image.load('imagens/coracao.png')
coracao3 = pg.image.load('imagens/coracao.png')

# Ze gotinha
gotinha = pg.image.load('imagens/ze-gota.png')
you_tried = pg.image.load('imagens/at_least.jpg')

# title and icon
pg.display.set_caption("Gôtcha!")
icon = pg.image.load('imagens/icone-gotinha.png')
pg.display.set_icon(icon)

# Player
playerImg = pg.image.load('imagens/jogador.png')

# seringa
seringaImg = pg.image.load('imagens/seringa.png')

# Cloroquina
cloroquinaImg = pg.image.load('imagens/cloroquina.png')

# coronavirus
coronavirusImg = pg.image.load('imagens/coronavirus.png')

# carta pfizer
pfizerImg = pg.image.load('imagens/carta-pfizer.png')

# Score
textX = 10
textY = 10
font = pg.font.Font('freesansbold.ttf', 32)

# Virus and chloroquine passed count
passed_font = pg.font.Font('freesansbold.ttf', 14)

# Texts Game Over
big_over_font = pg.font.Font('freesansbold.ttf', 64)
small_over_font = pg.font.Font('freesansbold.ttf', 16)


def new_game():
    global playerX, playerY, playerX_change, playerY_change, seringaX, seringaY, seringaX_change, seringa_state
    global cloroquinaX, cloroquinaY, cloroquinaX_change, coronavirusX, coronavirusY, coronavirusX_change, pfizerX
    global pfizerY, pfizerX_change, score_value, count_miss_virus, count_chloroquine, count_miss_chloroquine
    global count_letters, count_missed_letters

    playerX = 10
    playerY = 500
    playerX_change = 0
    playerY_change = 0

    seringaX = -50
    seringaY = -50
    seringaX_change = 1.5
    seringa_state = "ready"  # 'ready': nao se ve a seringa na tela / 'fire': a seringa esta se movendo

    cloroquinaX = 1500
    cloroquinaY = random.randint(52, 536)
    cloroquinaX_change = -0.4  # anda constantemente

    coronavirusX = 1300
    coronavirusY = random.randint(52, 536)
    coronavirusX_change = -0.5

    pfizerX = 1600
    pfizerY = random.randint(52, 536)
    pfizerX_change = -0.3

    score_value = 0

    count_miss_virus = 0
    count_chloroquine = 0
    count_miss_chloroquine = 0
    count_letters = 0
    count_missed_letters = 0


def seta_menu(x, y):
    screen.blit(menu_arrow, (x, y))


def hearts(x, y):
    if count_chloroquine <= 0:
        screen.blit(coracao, (x + 700, y + 5))
    if count_chloroquine <= 1:
        screen.blit(coracao2, (x + 730, y + 5))
    if count_chloroquine <= 2:
        screen.blit(coracao3, (x + 760, y + 5))


def show_score(x, y):
    score = font.render(f"Score: {str(score_value)}", True, (255, 255, 255))
    virus_pass = passed_font.render(f"Vírus passados: {str(count_miss_virus)}", True, (204, 204, 0))
    letter_pass = passed_font.render(f"Cartas perdidas: {str(count_missed_letters)}", True, (204, 204, 0))
    letter_get = passed_font.render(f"Cartas adquiridas: {str(count_letters)}", True, (0, 204, 0))
    chloroquine_pass = passed_font.render(f"Caixas passadas: {str(count_miss_chloroquine)}", True,
                                          (204, 204, 0))
    screen.blit(score, (x, y))
    screen.blit(virus_pass, (x + 320, y))
    screen.blit(letter_pass, (x + 150, y))
    screen.blit(letter_get, (x + 150, y + 20))
    screen.blit(chloroquine_pass, (x + 320, y + 20))


def game_over_text():
    over_text = big_over_font.render(f"GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def player(x, y):
    screen.blit(playerImg, (x, y))  # "desenha" na tela


def cloroquina(x, y):
    screen.blit(cloroquinaImg, (x, y))


def coronavirus(x, y):
    screen.blit(coronavirusImg, (x, y))


def pfizer(x, y):
    screen.blit(pfizerImg, (x, y))


def fire_seringa(x, y):
    screen.blit(seringaImg, (x + 60, y + 16))


def is_collision(cloroquina_x, cloroquina_y, seringa_x, seringa_y,
                 corona_x, corona_y, pfizer_x, pfizer_y, player_x, player_y):
    distancia_cloroq = sqrt((cloroquina_x - seringa_x) ** 2 + (cloroquina_y - seringa_y) ** 2)
    distancia_corona = sqrt((corona_x - seringa_x) ** 2 + (corona_y - seringa_y) ** 2)
    distancia_pfizer = sqrt((pfizer_x - seringa_x) ** 2 + (pfizer_y - seringa_y) ** 2)
    dist_player_pfizer = sqrt((pfizer_x - player_x) ** 2 + (pfizer_y - player_y) ** 2)
    dist_player_chloroq = sqrt((cloroquina_x - player_x) ** 2 + (cloroquina_y - player_y) ** 2)

    if distancia_cloroq <= 27:
        matou_cloroq = True
    else:
        matou_cloroq = False
    if distancia_corona <= 27:
        matou_corona = True
    else:
        matou_corona = False
    if distancia_pfizer <= 27:
        matou_pfizer = True
    else:
        matou_pfizer = False
    if dist_player_pfizer <= 48:
        pegou_pfizer = True
    else:
        pegou_pfizer = False
    if dist_player_chloroq <= 48:
        pegou_cloroq = True
    else:
        pegou_cloroq = False

    return matou_cloroq, matou_corona, matou_pfizer, pegou_pfizer, pegou_cloroq


def best_end_game():
    main_text = big_over_font.render(f"PARABÉNS!", True, (255, 255, 255))
    small_text = small_over_font.render(f"10 cartas da Pfizer obtidas!"
                                        f" Imunização da população garantida!", True, (255, 255, 255))
    small_text2 = small_over_font.render(f"Nenhum coronavírus ou caixa de cloroquina foi deixado pra trás!"
                                         f"", True, (255, 255, 255))
    small_text3 = small_over_font.render(f"Muitas vidas foram salvas!", True, (255, 255, 255))
    screen.blit(quadro_fundo, (100, 100))
    screen.blit(gotinha, (370, 210))
    screen.blit(main_text, (200, 120))
    screen.blit(small_text, (150, 375))
    screen.blit(small_text2, (150, 400))
    screen.blit(small_text3, (300, 425))


def cloroq_end_game():
    main_text = big_over_font.render(f"PARABÉNS!", True, (255, 255, 255))
    small_text = small_over_font.render(f"Todas as 10 cartas da Pfizer obtidas!"
                                        f" Imunização da população garantida!", True, (255, 255, 255))
    small_text2 = small_over_font.render(f"Nenhum coronavírus ou caixa de pacote foi deixado pra trás!"
                                         f"", True, (255, 255, 255))
    small_text3 = small_over_font.render(f"Muitas vidas foram salvas!", True, (255, 255, 255))
    screen.blit(quadro_fundo, (100, 100))
    screen.blit(gotinha, (370, 190))
    screen.blit(main_text, (200, 120))
    screen.blit(small_text, (110, 325))
    screen.blit(small_text2, (110, 350))
    screen.blit(small_text3, (110, 375))


def medium_end_game():
    main_text = big_over_font.render(f"Muito bem!", True, (255, 255, 255))
    small_text = small_over_font.render(f"10 cartas da Pfizer obtidas!"
                                        f" Imunização da população garantida!", True, (255, 255, 255))
    small_text2 = small_over_font.render(f"Porém, alguns coronavírus e/ou caixas de cloroquina passaram :("
                                         f"", True, (255, 255, 0))
    small_text3 = small_over_font.render(f"Se esforce mais e tente eliminar todos na próxima. Você consegue!", True,
                                         (255, 255, 255))
    screen.blit(quadro_fundo, (100, 100))
    screen.blit(you_tried, (325, 200))
    screen.blit(main_text, (220, 120))
    screen.blit(small_text, (150, 375))
    screen.blit(small_text2, (140, 400))
    screen.blit(small_text3, (135, 425))


def is_gameover(player_x, player_y, corona_x, corona_y):
    dist_gameover_corona = sqrt((player_x - corona_x) ** 2 + (player_y - corona_y) ** 2)
    if dist_gameover_corona <= 48:
        return True
    else:
        return False


# menu arrow Y
arrow_Y = 0

game_run = True
while game_run:
    new_game()  # novo jogo, reseta tudo

    # background menu music
    mixer.music.load('sons/menu_music.mp3')
    mixer.music.set_volume(0.1)
    mixer.music.play(-1)  # o -1 faz tocar em loop

    # menu inicial
    exit_game = False
    menu = True
    show_about = False
    while menu:
        screen.fill((255, 255, 255))
        screen.blit(menu_image, (0, 0))

        if arrow_Y == 0:
            seta_menu(230, 297)  # começar
        if arrow_Y == 1:
            seta_menu(285, 393)  # creditos
        if arrow_Y == 2:
            seta_menu(320, 490)  # sair

        for event in pg.event.get():
            if event.type == pg.QUIT:
                menu = False
                exit_game = True
                game_run = False

            if event.type == pg.KEYDOWN:

                if event.key == pg.K_UP:
                    mixer.Sound('sons/click_menu.wav').play()
                    arrow_Y += -1
                if event.key == pg.K_DOWN:
                    mixer.Sound('sons/click_menu.wav').play()
                    arrow_Y += 1
                if event.key == pg.K_KP_ENTER or event.key == pg.K_RETURN:
                    if arrow_Y == 0:
                        mixer.Sound('sons/game_init.wav').play()
                        pg.time.delay(2000)
                        menu = False
                    if arrow_Y == 1:
                        mixer.Sound('sons/sair_creditos.wav').play()
                        show_about = True
                    if arrow_Y == 2:
                        mixer.Sound('sons/sair_creditos.wav').play()
                        pg.time.delay(1000)
                        menu = False
                        exit_game = True
                        game_run = False

        # Menu Sobre
        while show_about:
            screen.blit(menu_about, (100, 100))
            for about_event in pg.event.get():
                if about_event.type == pg.KEYDOWN:
                    show_about = False
            pg.display.update()

        # limita a seta
        if arrow_Y >= 2:
            arrow_Y = 2
        if arrow_Y <= 0:
            arrow_Y = 0

        pg.display.update()

    # background game music
    mixer.music.load('sons/background_music.mp3')
    mixer.music.set_volume(0.1)
    mixer.music.play(-1)  # o -1 faz tocar em loop

    # game inicia
    running = True
    while running:

        if exit_game:
            break

        # RGB
        screen.fill((0, 0, 128))

        # background image
        screen.blit(background, (0, 0))

        for event in pg.event.get():  # eventos

            # para sair do loop (fechar o programa) quando clicar no 'X'
            if event.type == pg.QUIT:
                running = False
                game_run = False

            # se uma tecla é pressionada, verifica a direção e anda nela
            if event.type == pg.KEYDOWN:

                if event.key == pg.K_LEFT:
                    playerX_change = -0.6
                if event.key == pg.K_RIGHT:
                    playerX_change = 0.6
                if event.key == pg.K_UP:
                    playerY_change = -0.6
                if event.key == pg.K_DOWN:
                    playerY_change = 0.6

                if event.key == pg.K_SPACE and seringa_state == "ready":
                    mixer.Sound('sons/disparo_seringa.mp3').play()
                    seringaX, seringaY = playerX, playerY  # 1ª coord é no player
                    seringa_state = "fire"
                    fire_seringa(seringaX, seringaY)

            # quando deixa de pressionar uma tecla, zera o acrescimo de movimento
            if event.type == pg.KEYUP:
                if event.key == pg.K_LEFT or event.key == pg.K_RIGHT:
                    playerX_change = 0

                if event.key == pg.K_UP or event.key == pg.K_DOWN:
                    playerY_change = 0

        # movimento objetos
        cloroquinaX += cloroquinaX_change  # constante!
        coronavirusX += coronavirusX_change
        pfizerX += pfizerX_change
        # não deixa ir ao infinito e além
        if cloroquinaX <= -60:
            count_miss_chloroquine += 1
            cloroquinaX = 1250
            cloroquinaY = random.randint(52, 536)
        if coronavirusX <= -60:
            count_miss_virus += 1
            coronavirusX = 790
            coronavirusY = random.randint(52, 536)
        if pfizerX <= -60:
            count_missed_letters += 1
            pfizerX = 1000
            pfizerY = random.randint(52, 536)

        # movimento jogador
        playerX += playerX_change
        playerY += playerY_change
        # não deixa o jogador passar das bordas
        if playerX <= 0:
            playerX = 1
        elif playerX >= 736:
            playerX = 734
        if playerY >= 536:
            playerY = 535
        elif playerY <= 52:
            playerY = 53

        # mostra elementos do jogo
        player(playerX, playerY)
        cloroquina(cloroquinaX, cloroquinaY)
        coronavirus(coronavirusX, coronavirusY)
        pfizer(pfizerX, pfizerY)
        show_score(textX, textY)

        # movimento da seringa
        if seringaX >= 800:
            # seringaX = 800
            seringa_state = "ready"
            seringaX = -50
            seringaY = -50
        if seringa_state == "fire":
            fire_seringa(seringaX, seringaY)
            seringaX += seringaX_change

        # colisão
        collision = is_collision(cloroquinaX, cloroquinaY, seringaX, seringaY,
                                 coronavirusX, coronavirusY, pfizerX, pfizerY, playerX, playerY)

        # atirou na cloroquina
        if collision[0]:
            mixer.Sound('sons/estouro.mp3').play()
            seringa_state = "ready"
            seringaX, seringaY = -100, -100  # vai pra longe
            score_value += 1
            cloroquinaX = 1250
            cloroquinaY = random.randint(52, 536)

        # atirou no coronavirus
        if collision[1]:
            mixer.Sound('sons/estouro.mp3').play()
            seringa_state = "ready"
            seringaX, seringaY = -100, -100  # vai para longe
            score_value += 1
            coronavirusX = random.randint(790, 1250)
            coronavirusY = random.randint(52, 536)

        # atirou na carta pfizer
        if collision[2]:
            count_missed_letters += 1
            mixer.Sound('sons/estouro.mp3').play()
            seringa_state = "ready"
            seringaX, seringaY = -100, -100  # vai para longe
            pfizerX = random.randint(1000, 1300)
            pfizerY = random.randint(52, 536)

        # pegou carta pfizer
        if collision[3]:
            count_letters += 1
            which_sound = str(random.randint(0, 9))
            if which_sound in '0123456':
                mixer.Sound('sons/pick_letter.wav').play()
            elif which_sound in '78':
                mixer.Sound('sons/pfizer.mp3').play()
            else:
                mixer.Sound('sons/pfizer ta passada.mp3').play()
            pfizerX = random.randint(1500, 2000)
            pfizerY = random.randint(52, 536)

        # pegou a cloroquina
        if collision[4]:
            count_chloroquine += 1
            mixer.Sound('sons/pegou_cloroquina.wav').play()
            cloroquinaX = random.randint(1500, 2000)
            cloroquinaY = random.randint(52, 536)

        hearts(textX, textY)  # remove vidas

        # Ze Gotinha pega coronavirus. Game Over.
        game_over = is_gameover(playerX, playerY, coronavirusX, coronavirusY)
        if game_over:
            pg.mixer.music.stop()
            mixer.Sound('sons/oof.wav').play()
            game_over_text()
            pg.display.update()
            pg.time.delay(500)
            mixer.Sound('sons/espirro_mascara.wav').play()
            pg.time.delay(3000)
            break

        # 10 cartas coletadas, sem deixar nada passar
        if count_miss_chloroquine + count_miss_virus + \
                count_missed_letters == 0 and count_letters >= 10:
            pg.mixer.music.stop()
            mixer.Sound('sons/palmas.wav').play()
            best_end_game()
            pg.display.update()
            pg.time.delay(8000)
            break

        # 3 caixas de cloroquina coletadas, Zé Gotinha adquire hepatite medicamentosa.
        if count_chloroquine == 3:
            pg.mixer.music.stop()
            game_over_text()
            pg.display.update()
            pg.time.delay(500)  # delay do dano
            mixer.Sound('sons/cloroquinado.wav').play()
            pg.time.delay(4000)
            break

        # 10 cartas coletadas, passam virus e/ou caixas.
        if count_miss_chloroquine + count_miss_virus != 0 and count_letters >= 10:
            pg.mixer.music.stop()
            mixer.Sound('sons/yay.wav').play()
            medium_end_game()
            pg.display.update()
            pg.time.delay(8000)
            break

        pg.display.update()  # atualiza o frame

    # reseta tudo para um novo jogo
    player(playerX, playerY)
    cloroquina(cloroquinaX, cloroquinaY)
    coronavirus(coronavirusX, coronavirusY)
    pfizer(pfizerX, pfizerY)
