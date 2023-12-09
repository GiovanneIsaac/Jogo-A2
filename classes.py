# ARQUIVO PARA CONSTRUÇÃO DAS CLASSES

import pygame
from pygame.locals import *
from random import randint, choice

import constantes as const
import assets

pygame.init()

class Fundo(pygame.sprite.Sprite):
    """Classe para imagens de fundo de cenário"""
    def __init__(self, sprite):
        super().__init__()

        self.image = sprite
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 0)

class Plataforma(pygame.sprite.Sprite):

    """
    Classe para criação de uma plataforma

    Args:
        x (int) : Posição x do canto superior esquerdo da plataforma
        y (int) : Posição y do canto superior esquerdo da plataforma
        indice (int) : Define o tamanho da plataforma, o tamanho será (em pixels) indice * 16
        movel (bool) : Define se a plataforma será móvel ou não, o padrão é False e esse indica que a plataforma é fixa
    """

    def __init__(self, x, y, indice, movel=False):
        super().__init__()

        self.indice = indice
        self.movel = movel

        self.grupo_sprites = [assets.plataforma] * self.indice
        self.grupo_rect = []

        for sprite in self.grupo_sprites:
            self.grupo_rect.append(sprite.get_rect())

        self.image = pygame.Surface((self.indice * 16, 16))

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

        self.sentido = choice(["ESQUERDA", "DIREITA"])

        for i in range(self.indice):
            if i == 0:
                self.grupo_rect[i].x = x
            else:
                self.grupo_rect[i].x = x + i * self.grupo_sprites[i].get_width()
            self.grupo_rect[i].y = y
            i += 1
