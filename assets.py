# ARQUIVO PARA LIDAR COM OS ASSETS DO JOGO

import pygame
import os

pygame.init()

tela = pygame.display.set_mode()

diretorio_imagens = os.path.join(os.getcwd(), 'imagens')
sprites = os.path.join(diretorio_imagens, 'sprites.png')
sprites = pygame.image.load(sprites).convert_alpha()


# SPRITE JOGADOR
jogador = sprites.subsurface((64 * 2, 64 * 0), (64, 64))


# SPRITES INIMIGOS
inimigo_Right = sprites.subsurface((64 * 1, 64 * 1), (64, 64))
inimigo_R = pygame.transform.scale(inimigo_Right, (32, 32))

inimigo_Left = sprites.subsurface((64 * 2, 64 * 1), (64, 64))
inimigo_L = pygame.transform.scale(inimigo_Left, (32, 32))

inimigo_Up = sprites.subsurface((64 * 0, 64 * 2), (64, 64))
inimigo_U = pygame.transform.scale(inimigo_Up, (32, 32))

inimigo_Down = sprites.subsurface((64 * 1, 64 * 2), (64, 64))
inimigo_D = pygame.transform.scale(inimigo_Down, (32, 32))


# SPRITE FRUTA
fruta = sprites.subsurface((64 * 0, 64 * 1), (64, 64))


# SPRITE PLATAFORMA
plataforma = sprites.subsurface((64 * 1, 64 * 0), (64, 64))
plataforma = pygame.transform.scale(plataforma, (16, 16))


# TELA INICIAL
tl_inicial = sprites.subsurface((64 * 2, 64 * 2), (64, 64))
tl_inicial = pygame.transform.scale(tl_inicial, (64 * 10, 64 * 10))


# SPRITE CENÁRIO
cenario = sprites.subsurface((64 * 0, 64 * 0), (64, 64))
cenario = pygame.transform.scale(cenario, (64 * 10, 64 * 10))


# TELA FINAL
tl_final = sprites.subsurface((64 * 0, 64 * 3), (64, 64))
tl_final = pygame.transform.scale(tl_final, (64 * 10, 64 * 10))
