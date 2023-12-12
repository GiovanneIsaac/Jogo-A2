# ARQUIVO PARA A CONSTRUÇÃO DO LOOP DO JOGO

import pygame
from pygame.locals import *
import constantes as con
import classes as cl
import assets as ast


class Jogo:
    def __init__(self):
        # Inicilaizando o que é necessário na biblioteca pygame
        pygame.init()
        # ===================================================
        # Criando a tela
        self.tela = pygame.display.set_mode((con.LARGURA, con.ALTURA))
        pygame.display.set_caption(con.TITULO)

        self.relogio = pygame.time.Clock()
        self.jogo_rodando = True

        self.fonte = pygame.font.match_font(con.FONTE)
        # ===================================================
        self.sprites_coletavel = pygame.sprite.Group()
        self.sprites_plataformas = pygame.sprite.Group()
        self.sprites_inimigos = pygame.sprite.Group()

    # OS MÉTODOS ABAIXO ESTÃO RELACIONADOS AO MOMENTO EM QUE O JOGADOR ESTÁ JOGANDO
    # (ou seja, não está nem na tela inicial, nem na tela final)

    def novo_jogo(self):
        """Dá inicio ao jogo, criando as instâncias e
            chamando a função responsável pelo loop"""

        # LIMPA OS GRUPOS DE SPRITES, PARA REINICIAR O JOGO
        self.sprites_coletavel.empty()
        self.sprites_plataformas.empty()
        self.sprites_inimigos.empty()

        self.cenario = cl.Fundo(ast.cenario)
        self.jogador = cl.Jogador()

        self.sprites_coletavel.add(cl.Fruta())

        for number in range(1, 4):
            plat = cl.Plataforma(con.ALTURA / 4 * number, 10, True)
            self.sprites_plataformas.add(plat)

        self.sprites_plataformas.add(cl.Chao())

        for i in range(4):
            self.sprites_inimigos.add(cl.Inimigo())

        self.tempo = 0
        self._rodar()

    def _rodar(self):
        """Loop do jogo para quando o jogador está jogando"""

        jogando = True

        while jogando:
            self.relogio.tick(con.FPS)
            self.tempo += 1
            self._eventos()
            self._update()
            self._draw()
            self._exibir_informacoes()
            pygame.display.update()

            if self.jogador.vida <= 0:
                jogando = False
    # ===================================================

    # OS MÉTODOS ABAIXO ESTÃO RELACIONADOS A ATUALIZAÇÕES DO JOGO
    # (possíveis eventos, mover os componentes e desenha-los na tela)

    def _eventos(self):
        """Checa possíveis acontecimentos no jogo"""

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._encerra_jogo()

            if event.type == KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self._encerra_jogo()

        cl.jogador_coleta(self.jogador, self.sprites_coletavel)

        cl.jogador_colide_inimigo(self.jogador, self.sprites_inimigos)

        cl.jogador_em_plataforma(self.jogador, self.sprites_plataformas)

    def _update(self):
        """Atualiza os objetos do jogo"""

        self.sprites_inimigos.update()
        self.jogador.update()

    def _draw(self):
        """Exibe as instâncias na tela"""

        self.cenario.draw(self.tela)
        self.jogador.draw(self.tela)
        self.sprites_plataformas.update(self.tela)
        self.sprites_inimigos.draw(self.tela)
        self.sprites_coletavel.draw(self.tela)

    # ===================================================
    def _exibir_texto(self, texto, tamanho, cor, pos):
        """
        Exibe um texto na tela.

        Args:
            texto (str) : Texto a ser exibido na tela.
            tamanho (int): Tamanho da fonte do texto.
            cor (Tuple[int, int, int]) : Cor do texto a ser exibido.
            pos (Tuple[int, int]) : Posição do centro do lado superior do texto.
        """

        fonte_tamanho = pygame.font.Font(self.fonte, tamanho)  # Alterando o tamanho da fonte
        texto_formatado = fonte_tamanho.render(texto, True, cor)  # Formatando o texto com a fonte e cor passados

        texto_rect = texto_formatado.get_rect()  # Obtendo a área que o texto ocupa
        texto_rect.midtop = pos  # Posiciona o centro do lado superior da área do texto na posição fornecida

        self.tela.blit(texto_formatado, texto_rect)  # Exibindo o texto na tela

    def _exibir_informacoes(self):
        self._exibir_texto(f"Vidas: {self.jogador.vida}", 30, con.WHITE, (65, 0))
        self._exibir_texto(f"Pontos: {self.jogador.pontos}", 30, con.WHITE, (70, 30))
        self._exibir_texto(f"Tempo: {self.tempo//30}", 30, con.WHITE, (560, 0))
    # ===================================================

    # OS MÉTODOS ABAIXO ESTÃO RELACIONADOS À TELA INICIAL E À TELA FINAL

    def tela_inicial(self):
        """Exibe a tela inicial, momento em que o jogo é aberto"""

        cl.Fundo(ast.tl_inicial).draw(self.tela)

        self._exibir_texto('- Precione ESPAÇO para jogar -', 32, con.WHITE, (con.LARGURA // 2, con.ALTURA//2))

        pygame.display.flip()
        self._esperar_por_jogador()

    def tela_final(self):
        """Exibe a tela final, momento em que o jogador perde o jogo"""

        cl.Fundo(ast.tl_final).draw(self.tela)

        self._exibir_texto('- FIM DE JOGO -', 50, con.BLACK, (con.LARGURA // 2, 140))
        self._exibir_texto('- Precione ESPAÇO para jogar novamente-', 30, con.BLACK, (con.LARGURA // 2, con.ALTURA//2))
        self._exibir_texto(f"Pontos : {self.jogador.pontos}", 30, con.BLACK, (con.LARGURA // 2, 500))
        self._exibir_texto(f"Tempo : {self.tempo//30}", 30, con.BLACK, (con.LARGURA // 2, 531))

        pygame.display.flip()
        self._esperar_por_jogador()

    def _esperar_por_jogador(self):
        """Espera até que o jogador de um comando para iniciar
            ou reiniciar o jogo, apertando uma tecla"""

        esperando = True

        while esperando:
            self.relogio.tick(con.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._encerra_jogo()

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE:
                        esperando = False

                    if event.key == pygame.K_ESCAPE:
                        self._encerra_jogo()
    # ===================================================

    @staticmethod
    def _encerra_jogo():
        """Encerra o jogo e o programa"""
        pygame.quit()
        exit()


jogo = Jogo()  # Criando objeto da classe Jogo

jogo.tela_inicial()  # Exibindo tela inicial

while jogo.jogo_rodando:

    jogo.novo_jogo()  # Iniciando o jogo

    jogo.tela_final()  # Exibindo tela final
