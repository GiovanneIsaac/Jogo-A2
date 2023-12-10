import pygame
from pygame.locals import *
from sys import exit
from random import randint, randrange

import constantes as cons
import assets
import classes

pygame.init()

# ===========================================================
# VARIÁVEIS
tela = pygame.display.set_mode((cons.LARGURA, cons.ALTURA))
pygame.display.set_caption(cons.TITULO)

relogio = pygame.time.Clock()

jogando = True

# ===========================================================
# UNIDADES
todas_as_sprite = pygame.sprite.Group()

sprites_cenario = pygame.sprite.Group()
sprites_jogador = pygame.sprite.Group()
sprites_coletavel = pygame.sprite.Group()
sprites_plataformas = pygame.sprite.Group()
sprites_inimigos = pygame.sprite.Group()

cenario = classes.Fundo(assets.cenario)
sprites_cenario.add(cenario)
todas_as_sprite.add(cenario)

jogador = classes.Jogador()
sprites_jogador.add(jogador)
todas_as_sprite.add(jogador)

fruta = classes.Fruta()
sprites_coletavel.add(fruta)
todas_as_sprite.add(fruta)

plataformas = []

for number in range(1, 4):
    plat = classes.Plataforma(cons.ALTURA/4 * number, 10, True)
    sprites_plataformas.add(plat)
    plataformas.append(plat)

chao = classes.Chao()
'''chao = classes.Plataforma(640, 40)'''
sprites_plataformas.add(chao)
plataformas.append(chao)

for i in range(4):
    inimigo = classes.Inimigo()
    sprites_inimigos.add(inimigo)
    todas_as_sprite.add(inimigo)

todas_as_sprite.add(cenario)
todas_as_sprite.add(jogador)
todas_as_sprite.add(inimigo)
todas_as_sprite.add(fruta)

# ===========================================================
# LOOP JOGO
while True:
    relogio.tick(cons.FPS)

    for evento in pygame.event.get():
        if evento.type == QUIT:
            pygame.quit()
            exit()

        if evento.type == KEYDOWN:
            if evento.key == K_ESCAPE:
                pygame.quit()
                exit()

            if evento.key == K_r and not jogando:
                jogando = True
                classes.reiniciar_jogo(jogador, sprites_inimigos, sprites_plataformas, sprites_coletavel)

    # Verificando se houve colisão entre o jogador e os coletáveis
    coleta = pygame.sprite.spritecollide(jogador, sprites_coletavel, False, pygame.sprite.collide_mask)
    # Caso tenha havido coleta, aumenta o número de pontos do jogador e redefine a posição do coletável
    if coleta:
        # Redefinindo a posição dos coletáveis
        sprites_coletavel.update()

        # Aumentando o número de pontos do jogador
        jogador.pontos += 1
        print(f"PONTOS: {jogador.pontos}")

    # Verificando se houve colisão entre o jogador e os inimigos
    bate = pygame.sprite.spritecollide(jogador, sprites_inimigos, True, pygame.sprite.collide_mask)
    if bate:
        jogador.vida -= 1
        inimigo = classes.Inimigo()
        sprites_inimigos.add(inimigo)
        todas_as_sprite.add(inimigo)
        print(f"VIDA: {jogador.vida}")
        if jogador.vida == 0:
            jogando = False
    else:
        sprites_inimigos.update()
        sprites_jogador.update()
        classes.jogador_em_plataforma(jogador, sprites_plataformas)

    # Desenhando as sprites na tela
    todas_as_sprite.draw(tela)
    sprites_plataformas.update(tela)

    pygame.display.update()
