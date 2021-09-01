import pygame as pg

# initialize the pygame
import pygame.display

pg.init()

screen = pg.display.set_mode((800, 600))

# title and icon
pygame.display.set_caption("TacaGota")
icon = pg.image.load('imagens/icone-gotinha.png')
pygame.display.set_icon(icon)

# game loop
running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
