# ARQUIVO PARA CONSTRUÇÃO DAS CLASSES

import pygame
from pygame.locals import *
from random import randint

import constantes as const
import assets

pygame.init()

class Fundo(pygame.sprite.Sprite):
    def __init__(self, sprite):
        super().__init__()

        self.image = sprite
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 0)
