import time
import pygame as pg
from pygame import mixer
import random
from math import sqrt

# initialize the pygame

pg.init()

screen = pg.display.set_mode((800, 600))

# background
background = pg.image.load('imagens/brasilia.jpg')

# background music
mixer.music.load('sons/background_music.mp3')
mixer.music.play(-1)

# title and icon
pg.display.set_caption("Gôtcha!")
icon = pg.image.load('imagens/icone-gotinha.png')
pg.display.set_icon(icon)

# Player
playerImg = pg.image.load('imagens/jogador.png')
playerX = 10
playerY = 500
playerX_change = 0
playerY_change = 0

# seringa
seringaImg = pg.image.load('imagens/seringa.png')
seringaX = -50
seringaY = -50
seringaX_change = 1.5
seringaY_change = 0  # a bala nao sobe!
# ready: nao se ve a seringa na tela
# fire: a seringa esta se movendo
seringa_state = "ready"

# Cloroquina
cloroquinaImg = pg.image.load('imagens/cloroquina.png')
cloroquinaX = 1500
cloroquinaY = random.randint(64, 536)
cloroquinaX_change = -0.3  # anda constantemente

# coronavirus
coronavirusImg = pg.image.load('imagens/coronavirus.png')
coronavirusX = 790
coronavirusY = random.randint(64, 536)
coronavirusX_change = -0.3  # anda constantemente

# Pontuacao
score_value = 0
font = pg.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

# Texto Game Over
over_font = pg.font.Font('freesansbold.ttf', 64)


def show_score(x, y):
    score = font.render(f"Score: {str(score_value)}", True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render(f"GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def player(x, y):
    screen.blit(playerImg, (x, y))  # "desenha" na tela


def cloroquina(x, y):
    screen.blit(cloroquinaImg, (x, y))


def coronavirus(x, y):
    screen.blit(coronavirusImg, (x, y))


def fire_seringa(x, y):
    global seringa_state
    seringa_state = "fire"
    screen.blit(seringaImg, (x + 60, y + 16))


def is_collision(cloroquina_x, cloroquina_y, seringa_x, seringa_y, corona_x, corona_y):
    distancia_cloroq = sqrt((cloroquina_x - seringa_x) ** 2 + (cloroquina_y - seringa_y) ** 2)
    distancia_corona = sqrt((corona_x - seringa_x) ** 2 + (corona_y - seringa_y) ** 2)
    if distancia_cloroq <= 27:
        matou_cloroq = True
    else:
        matou_cloroq = False
    if distancia_corona <= 27:
        matou_corona = True
    else:
        matou_corona = False
    return matou_cloroq, matou_corona


def is_gameover(player_x, player_y, corona_x, corona_y):
    distancia_gameover = sqrt((player_x - corona_x) ** 2 + (player_y - corona_y) ** 2)
    if distancia_gameover <= 48:
        return True
    else:
        return False


# game loop
running = True
while running:

    # RGB
    screen.fill((0, 0, 128))

    # background image
    screen.blit(background, (0, 0))

    for event in pg.event.get():

        # para sair do loop (fechar o programa) quando clicar no 'X'
        if event.type == pg.QUIT:
            running = False

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
                fire_seringa(seringaX, seringaY)

        # quando deixa de pressionar uma tecla, zera o acrescimo de movimento
        if event.type == pg.KEYUP:
            if event.key == pg.K_LEFT or event.key == pg.K_RIGHT or \
                    event.key == pg.K_UP or event.key == pg.K_DOWN:
                playerX_change = 0
                playerY_change = 0

    # movimento inimigos
    cloroquinaX += cloroquinaX_change  # constante!
    coronavirusX += coronavirusX_change
    # não deixa a caixa de cloroquina ir ao infinito e além
    if cloroquinaX <= -60:
        cloroquinaX = 1250
        cloroquinaY = random.randint(64, 536)
    if coronavirusX <= -60:
        coronavirusX = 790
        coronavirusY = random.randint(64, 536)

    # movimento jogador
    playerX += playerX_change
    playerY += playerY_change
    # não deixa o jogador passar das bordas
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736
    if playerY >= 536:
        playerY = 536
    elif playerY <= 0:
        playerY = 0

    # mostra elementos do jogo
    player(playerX, playerY)
    cloroquina(cloroquinaX, cloroquinaY)
    coronavirus(coronavirusX, coronavirusY)
    show_score(textX, textY)

    # movimento da seringa
    if seringaX >= 800:
        seringaX = 800
        seringa_state = "ready"
    if seringa_state == "fire":
        fire_seringa(seringaX, seringaY)
        seringaX += seringaX_change

    # colisão
    collision = is_collision(cloroquinaX, cloroquinaY, seringaX, seringaY, coronavirusX, coronavirusY)

    # colisao com a cloroquina
    if collision[0]:
        mixer.Sound('sons/estouro.mp3').play()
        seringa_state = "ready"
        seringaX, seringaY = playerX, playerY  # retorna a origem
        score_value += 1
        cloroquinaX = 1250
        cloroquinaY = random.randint(64, 536)

    # colisao com o coronavirus
    if collision[1]:
        mixer.Sound('sons/estouro.mp3').play()
        seringa_state = "ready"
        seringaX, seringaY = playerX, playerY  # retorna a origem
        score_value += 1
        coronavirusX = random.randint(790, 1250)
        coronavirusY = random.randint(64, 536)

    # game over
    game_over = is_gameover(playerX, playerY, coronavirusX, coronavirusY)

    if game_over:
        mixer.Sound('sons/oof.wav').play()
        game_over_text()
        running = False
    pg.display.update()
time.sleep(2)
