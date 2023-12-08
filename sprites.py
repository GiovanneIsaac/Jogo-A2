# Arquivo para trabalhar com sprites e audios

import pygame
import os

pygame.init()

tela = pygame.display.set_mode((480, 640))
pygame.display.set_caption("TESTE")
relogio = pygame.time.Clock()

diretorio_imagens = os.path.join(os.getcwd(), 'imagens')
spritesheet = os.path.join(diretorio_imagens, 'spritesheet.png')
spritesheet = pygame.image.load(spritesheet).convert_alpha()


# SPRITE JOGADOR
jogador = spritesheet.subsurface((64 * 2, 64 * 0), (64, 64))
#jogador = pygame.transform.scale(jogador, (32 * 2, 32 * 2))


# SPRITE INIMIGO
inimigo_R = spritesheet.subsurface((64 * 1, 64 * 1), (64, 64))
inimigo_R = pygame.transform.scale(inimigo_R, (32, 32))

inimigo_L = spritesheet.subsurface((64 * 2, 64 * 1), (64, 64))
inimigo_L = pygame.transform.scale(inimigo_L, (32, 32))

inimigo_U = spritesheet.subsurface((64 * 0, 64 * 2), (64, 64))
inimigo_U = pygame.transform.scale(inimigo_U, (32, 32))

inimigo_D = spritesheet.subsurface((64 * 1, 64 * 2), (64, 64))
inimigo_D = pygame.transform.scale(inimigo_D, (32, 32))


# SPRITE CENÁRIO
cenario = spritesheet.subsurface((64 * 0, 64 * 0), (64, 64))
cenario = pygame.transform.scale(cenario, (64 * 10, 64 * 10))


# SPRITE FRUTA
fruta = spritesheet.subsurface((64 * 0, 64 * 1), (64, 64))


# SPRITE PLATAFORMA
plataforma = spritesheet.subsurface((64 * 1, 64 * 0), (64, 64))
plataforma = pygame.transform.scale(plataforma, (64 * 0.25, 64 * 0.25))
