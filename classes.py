# ARQUIVO PARA CONSTRUÇÃO DAS CLASSES
import pygame
from pygame.locals import *
from random import randint, choice

import constantes as c
import assets

pygame.init()


# CLASSES
class Fundo(pygame.sprite.Sprite):
    """
    Classe que recebe uma sprite como argumento e usa ela como imagem de fundo do cenário
    """

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

        # Criando grupos com as sprites e que serão usadas para formar a plataforma
        self.grupo_sprites = [assets.plataforma] * self.indice
        self.grupo_rect = []
        for sprite in self.grupo_sprites:
            self.grupo_rect.append(sprite.get_rect())
        # Posicionando as sprites
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
        """Movimenta e posiciona a plataforma na tela que recebe como argumento"""
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
        elif self.rect.right >= c.LARGURA:
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

    # CRIAR MAIS COLETÁVEIS!!!


class Jogador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.vida = c.VIDA
        self.pontos = 0

        # Sprite e colisão do jogador
        self.image = assets.jogador
        self.mask = pygame.mask.from_surface(self.image)

        # Posicionamento do jogador
        self.rect = self.image.get_rect()
        self.x = c.INITIAL_POS[0]
        self.y = c.INITIAL_POS[1]
        self.rect.center = (self.x, self.y)

        self.velocidade_y = 0  # Usado para controlar a queda ou subida do personagem
        self.pulo = False

    def update(self):
        """Movimenta o jogador"""

        teclas = pygame.key.get_pressed()

        # Andando direita ou esquerda
        if teclas[K_RIGHT] or teclas[K_d]:
            self.rect.x += c.MOVIMENTO
        elif teclas[K_LEFT] or teclas[K_a]:
            self.rect.x -= c.MOVIMENTO

        # Caso o jogador saia do limite lateral da tela, ele é movido para o outro lado
        if self.rect.x > c.LARGURA - 4:
            self.rect.x = -60
        elif self.rect.x < -60:
            self.rect.x = c.LARGURA - 4

        # Lógica de pulo
        if (teclas[K_w] or teclas[K_UP]) and not self.pulo:
            self.velocidade_y += -c.PULO
            self.pulo = True

        # Gravidade
        self.velocidade_y += 1
        self.rect.y += self.velocidade_y


class Inimigo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Definindo a direção e o sentido para onde o inimigo se moverá
        self.direcao, self.sentido = self.set_direcao_e_sentido()

        # Definindo a imagem do inimigo
        self.image = self.set_sprite()

        # Criando máscara de colisão do inimigo
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.x = 800
        self.y = 800
        self.rect = (self.x, self.y)

    @staticmethod
    def set_direcao_e_sentido():
        """
        Método usado para definir de modo aleatório o sentido e a
        direção de um objeto da classe Inimigo.
        :return: Tupla contendo dois inteiros que podem ser 0 ou 1
        """

        direcao = randint(0, 1)
        sentido = randint(0, 1)

        return direcao, sentido

    def set_sprite(self):
        """
        Método que retorna a sprite do inimigo de acordo com
        a direção e com o sentido para o qual ele se move
        """

        if self.direcao == 0:
            if self.sentido == 0:
                sprite = assets.inimigo_R

            else:
                sprite = assets.inimigo_L

        else:
            if self.sentido == 0:
                sprite = assets.inimigo_U

            else:
                sprite = assets.inimigo_D

        return sprite

    def reiniciar_posicao(self):
        self.x = 800
        self.y = 800
        self.rect.center = (self.x, self.y)

    def update(self):
        """Método responsável por atualizar a localização do inimigo"""
        if self.direcao == 0:
            self.__movimentacao_horizontal()

        else:
            self.__movimentacao_vertical()

    def __movimentacao_horizontal(self):
        # MOVIMENTANDO HORIZONTALMENTE ATRAVÉS DA TELA
        if self.sentido == 0:
            self.x += c.MOVIMENTO
        else:
            self.x -= c.MOVIMENTO

        self.rect = (self.x, self.y)

        # SAINDO DOS LIMITES DA TELA
        if self.x > c.LARGURA - 4:
            self.y = randint(0, c.tam_fundo - c.Tam_inimigo)
            self.x = -28

            self.direcao, self.sentido = self.set_direcao_e_sentido()
            self.image = self.set_sprite()

        elif self.x < -28:
            self.y = randint(10, c.tam_fundo - c.Tam_inimigo)
            self.x = c.LARGURA - 4

            self.direcao, self.sentido = self.set_direcao_e_sentido()
            self.image = self.set_sprite()

    def __movimentacao_vertical(self):
        # MOVIMENTANDO VERTICALMENTE ATRAVÉS DA TELA
        if self.sentido == 0:
            self.y -= c.MOVIMENTO
        else:
            self.y += c.MOVIMENTO

        self.rect = (self.x, self.y)

        # SAINDO DOS LIMITES DA TELA
        if self.y > c.ALTURA - 4:
            self.x = randint(0, c.tam_fundo - c.Tam_inimigo)
            self.y = -28

            self.direcao, self.sentido = self.set_direcao_e_sentido()
            self.image = self.set_sprite()

        elif self.y < -28:
            self.x = randint(0, c.tam_fundo - c.Tam_inimigo)
            self.y = c.ALTURA - 4

            self.direcao, self.sentido = self.set_direcao_e_sentido()
            self.image = self.set_sprite()


# FUNÇÕES
def jogador_em_plataforma(jogador, plataformas):
    """
    Recebe um objeto da classe Jogador e um grupo de Plataformas
    e verifica se o jogador colidiu com alguma das plataformas,
    caso tenha colidido, a posição desse é atualizada.
    """

    # Verificando se o jogador colidiu com alguma plataforma do grupo "plataformas"
    plataformas_colisao = pygame.sprite.spritecollide(jogador, plataformas, False)

    for plataforma in plataformas_colisao:
        if jogador.velocidade_y > 0:
            # Se o jogador está caindo (velocidade_y > 0) e colide com uma plataforma, ele fica em cima dela
            jogador.rect.bottom = plataforma.rect.top
            jogador.velocidade_y = 0
            jogador.pulo = False

        elif jogador.velocidade_y < 0:
            # Se o jogador está caindo (velocidade_y < 0) e colide com uma plataforma, ele bate nela e para de subir
            jogador.rect.top = plataforma.rect.bottom
            jogador.velocidade_y = 0
