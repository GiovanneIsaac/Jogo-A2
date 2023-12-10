# ARQUIVO PARA CONSTRUÇÃO DAS CLASSES

import pygame
from pygame.locals import *
from random import randint, choice

import constantes as const
import assets

pygame.init()

class Fundo(pygame.sprite.Sprite):
    """
    Classe que recebe uma sprite como argumento e usa ela como imagem de fundo do cenário
    """

    def __init__(self, sprite):
        super().__init__()
        # Posicionamento do jogador
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

        # Criando e grupos com com as sprites que serão usadas para formar a plataforma
        self.grupo_sprites = [assets.plataforma] * self.indice
        self.grupo_rect = []
        for sprite in self.grupo_sprites:
            self.grupo_rect.append(sprite.get_rect())
        # Posicionando essas sprites
        for i, rect in enumerate(self.grupo_rect):
            rect.x = x + i * rect.width
            rect.y = y

        # Criando e posicionando o retângulo que será usado como área de colisão da plataforma
        self.image = pygame.Surface((self.indice * 16, 16))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

        # Escolhendo para qual sentido a plataforma se moverá
        self.sentido = choice(["ESQUERDA", "DIREITA"])
    
    def update(self, tela):
        """Movimenta e reposiciona a plataforma"""
        if self.movel:
            self.__movimentar()
            for rect in self.grupo_rect:
                self.__desenhar_sprites(tela)
        else:
            pass

    def __desenhar_sprites(self, tela):
        """Insere na tela as sprites que formam a plataforma"""

        for pos in range(self.indice):
            tela.blit(self.grupo_sprites[pos], self.grupo_rect[pos])

    def __movimentar(self):
        """Atualiza a posição da plataforma"""

        # Caso a plataforma bata em uma das laterais da tela, ela muda o sentido de movimento
        if self.rect.left <= 0:
            self.sentido = "DIREITA"
        elif self.rect.right >= const.LARGURA:
            self.sentido = "ESQUERDA"

        # Atualizando a posição da plataforma
        if self.sentido == "DIREITA":
            self.rect.x += 5
            for rect in self.grupo_rect:
                rect.x += 5
        elif self.sentido == "ESQUERDA":
            self.rect.x -= 5
            for rect in self.grupo_rect:
                rect.x -= 5


class Fruta(pygame.sprite.Sprite):
    """
    Classe para criação de uma fruta coletável
    """

    def __init__(self):
        super().__init__()
        # Sprite e colisão da Fruta
        self.image = assets.fruta
        self.mask = pygame.mask.from_surface(self.image)

        # Posicionamento da Fruta
        self.rect = self.image.get_rect()
        self.x = randint(40, 600)
        self.y = randint(50, 430)
        self.rect.center = (self.x, self.y)

    def update(self):
        """Atualiza a posição da fruta"""
        self.x = randint(40, 600)
        self.y = randint(50, 430)
        self.rect.center = (self.x, self.y)


class Jogador(pygame.sprite.Sprite):
    def __init__(self, nome):
        super().__init__()
        self.vida = const.VIDA
        self.pontos = 0

        # Sprite e colisão do jogador
        self.image = assets.jogador
        self.mask = pygame.mask.from_surface(self.image)

        # Posicionamento do jogador
        self.rect = self.image.get_rect()
        self.x = const.INITIAL_POS[0]
        self.y = const.INITIAL_POS[1]
        self.rect.center = (self.x, self.y)

        self.velocidade_y = 0  # Usado para controlar a queda ou subida do personagem
        self.pulo = False

    def update(self):
        teclas = pygame.key.get_pressed()

        # Andando direita ou esquerda
        if teclas[K_RIGHT] or teclas[K_d]:
            self.rect.x += const.MOVIMENTO
        elif teclas[K_LEFT] or teclas[K_a]:
            self.rect.x -= const.MOVIMENTO

        # Caso o jogador saia do limite lateral da tela, ele é movido para o outro lado
        if self.rect.x > const.LARGURA - 4:
            self.rect.x = -60
        elif self.rect.x < -60:
            self.rect.x = const.LARGURA - 4

        # Lógica de pulo
        if (teclas[K_w] or teclas[K_UP]) and not self.pulo:
            self.velocidade_y += -const.PULO
            self.pulo = True

        # Gravidade
        self.velocidade_y += 1
        self.rect.y += self.velocidade_y

