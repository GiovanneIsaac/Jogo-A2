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

    def draw(self, tela):
        tela.blit(self.image, self.rect)


class Chao(pygame.sprite.Sprite):
    """Classe que cria uma plataforma no lado inferior da tela"""

    def __init__(self):
        super().__init__()

        self.image = pygame.Surface((c.LARGURA, 1))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 0, c.ALTURA + 1

    def draw(self):
        pass


class Plataforma(pygame.sprite.Sprite):
    """
    Classe para criação de uma plataforma

    Args:
        y (int) : Posição y do canto superior esquerdo da plataforma.
        indice (int) : Define o tamanho da plataforma, o tamanho será (em pixels) indice * 16.
        movel (bool) : Define se a plataforma será móvel ou não, o padrão é False e esse indica que a plataforma é fixa.
    """

    def __init__(self, y, indice, movel=False):
        super().__init__()

        x = randint(0, 480)
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
        self.rect.x = randint(40, 600)
        self.rect.y = randint(40, 600)

    def update(self):
        """Atualiza a posição da fruta"""
        self.rect.x = randint(40, 600)
        self.rect.y = randint(40, 600)

    def draw(self, tela):
        tela.blit(self.image, self.rect)


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
        self.rect.x = c.INITIAL_POS[0]
        self.rect.y = c.INITIAL_POS[1]

        self.velocidade_y = 0  # Usado para controlar a queda ou subida do personagem
        self.pulo = False

    def update(self):
        """Método de movimentação do jogador"""

        teclas = pygame.key.get_pressed()

        # ANDANDO PARA DIREITA OU ESQUERDA
        if teclas[K_d] or teclas[K_RIGHT]:
            self.rect.x += c.MOVIMENTO
        elif teclas[K_a] or teclas[K_LEFT]:
            self.rect.x -= c.MOVIMENTO

        # Caso o jogador saia do limite lateral da tela, ele é movido para o outro lado
        if self.rect.x > c.LARGURA - 4:
            self.rect.x = -60
        elif self.rect.x < -60:
            self.rect.x = c.LARGURA - 4

        # LÓGICA DE PULO
        if (teclas[K_w] or teclas[K_UP]) and not self.pulo:
            self.velocidade_y += -c.PULO
            self.pulo = True

        # GRAVIDADE
        self.velocidade_y += 1
        self.rect.y += self.velocidade_y

    def draw(self, tela):
        tela.blit(self.image, self.rect)


class Inimigo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Definindo a direção e o sentido para onde o inimigo se moverá:
        # Direção definirá se o inimigo se move horizontalmente ou verticalmente e
        # sentido defenirá para qual lado ( Direita ou esquerda / Para cima ou para baixo)
        self.direcao, self.sentido = self.__set_direcao_e_sentido()

        # Definindo a imagem do inimigo
        self.image = self.__set_sprite()

        # Criando máscara de colisão do inimigo
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect.x = 800
        self.rect.y = 800

    @staticmethod
    def __set_direcao_e_sentido():
        """
        Método usado para definir de modo aleatório o sentido e a
        direção de um objeto da classe Inimigo.
        :return: Tupla contendo dois inteiros que podem ser 0 ou 1
        """

        direcao = randint(0, 1)
        sentido = randint(0, 1)

        return direcao, sentido

    def __set_sprite(self):
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

    def update(self):
        """Método responsável por atualizar a localização do inimigo"""

        if self.direcao == 0:
            self.__movimentacao_horizontal()

        else:
            self.__movimentacao_vertical()

    def __movimentacao_horizontal(self):
        """Lógica de movimentação caso o inimigo esteja se movendo verticalmente"""

        # MOVIMENTANDO HORIZONTALMENTE ATRAVÉS DA TELA
        if self.sentido == 0:
            self.rect.x += c.MOVIMENTO
        else:
            self.rect.x -= c.MOVIMENTO

        # SAINDO DOS LIMITES DA TELA
        if self.rect.x > c.LARGURA or self.rect.x < - 32:
            self.reiniciar_posicao()

    def __movimentacao_vertical(self):
        """Lógica de movimentação caso o inimigo esteja se movendo verticalmente"""

        # MOVIMENTANDO VERTICALMENTE ATRAVÉS DA TELA
        if self.sentido == 0:
            self.rect.y -= c.MOVIMENTO
        else:
            self.rect.y += c.MOVIMENTO

        # SAINDO DOS LIMITES DA TELA
        if self.rect.y > c.ALTURA or self.rect.y < - 32:
            self.reiniciar_posicao()

    def reiniciar_posicao(self):
        """Aleatoariza a posição do inimigo"""

        # REDEFININDO A DIREÇÃO, SENTIDO E A IMAGEM DO INIMIGO
        self.direcao, self.sentido = self.__set_direcao_e_sentido()
        self.image = self.__set_sprite()

        # DEFININDO PARA ONDE O INIMIGO SERÁ MANDADO DE ACORDO COM PARA ONDE ELE ESTÁ SE MOVENDO
        match (self.direcao, self.sentido):
            case (0, 0):
                self.rect.x = 0
                self.rect.y = randint(0, 640 - 32)
            case (0, 1):
                self.rect.x = 640
                self.rect.y = randint(0, 640 - 32)
            case (1, 0):
                self.rect.x = randint(0, 640 - 32)
                self.rect.y = 640
            case (1, 1):
                self.rect.x = randint(0, 640 - 32)
                self.rect.y = 0


# FUNÇÕES

def jogador_coleta(jogador, coletaveis):
    """
        Recebe um objeto da classe Jogador e um grupo de Coletáveis
        (Frutas) e verifica se o jogador colidiu com algum dos coletáveis,
        caso tenha colidido, a posição do coletável é atualizada.
    """

    # Verificando se houve colisão entre o jogador e os coletáveis
    coletado = pygame.sprite.spritecollide(jogador, coletaveis, False, pygame.sprite.collide_mask)

    # Caso tenha havido coleta, aumenta o número de pontos do jogador e redefine a posição do coletável
    if coletado:
        # Redefinindo a posição dos coletáveis
        for coletavel in coletado:
            coletavel.update()

        # Aumentando o número de pontos do jogador
        jogador.pontos += 1


def jogador_colide_inimigo(jogador, inimigos):
    """
    Recebe um objeto da classe Jogador e um grupo de Inimigos
    e verifica se o jogador colidiu com algum dos inimigos,
    caso tenha colidido, o número de vidas do jogador é diminuido.
    """

    bate = pygame.sprite.spritecollide(jogador, inimigos, True, pygame.sprite.collide_mask)

    if bate:
        jogador.vida -= 1
        inimigo = Inimigo()
        inimigos.add(inimigo)


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
