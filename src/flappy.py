##Configurando os leds
##importando as bibliotecas de integração com o raspberry
import RPi.GPIO as gp
import time

gp.setmode(gp.BCM)
##definindo os leds
gp.setup(17, gp.OUT, initial = gp.LOW)
gp.setup(18, gp.OUT, initial = gp.LOW)

##importando pygame
import pygame, random
from pygame.locals import *

##definindo variaveis 
LARGURA_TELA = 400
ALTURA_TELA = 800
VELOCIDADE = 10
GRAVIDADE = 1
VELOCIDADE_JOGO = 10

LARGURA_CHAO = 2 * LARGURA_TELA
ALTURA_CHAO = 100

LARGURA_CANO = 80
ALTURA_CANO = 500
VAO_CANO = 200

##Classe bird (personagem)
class Passaro(pygame.sprite.Sprite):
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        
        ##definindo os sprites do passaro
        self.images = [pygame.image.load('./assets/sprites/bluebird-upflap.png').convert_alpha(),
                       pygame.image.load('./assets/sprites/bluebird-midflap.png').convert_alpha(),
                       pygame.image.load('./assets/sprites/bluebird-downflap.png').convert_alpha()]  
        
        self.velocidade = VELOCIDADE
        
        self.imagem_atual = 0
        
        ##começando o jogo com essa sprite!
        self.image = pygame.image.load('./assets/sprites/bluebird-upflap.png').convert_alpha()
        #criando mascara de colisão
        self.mascara = pygame.mask.from_surface(self.image)
        
        self.rect = self.image.get_rect()
        ##Colocando o passaro no meio da tela divindo os tamanhos por 2 
        self.rect[0] = LARGURA_TELA / 2
        self.rect[1] = ALTURA_TELA / 2
        
    def update(self):
        self.imagem_atual = (self.imagem_atual + 1) % 3
        self.image = self.images [ self.imagem_atual ]
        
        self.velocidade += GRAVIDADE
        
        ## alterando o height fazendo o passaro cair
        self.rect[1] += self.velocidade
        
    def fly(self):
        self.velocidade = -VELOCIDADE
        ##a cada vez que o passo voar o led verde acende
        gp.output(18,gp.HIGH)
        time.sleep(0.5)
        gp.output(18,gp.LOW)
        
        
##Criando a classe cano
class Cano(pygame.sprite.Sprite):
            
    def __init__(self, isCanoInvertido, xPos, ySize):
           pygame.sprite.Sprite.__init__(self)
        
           self.image = pygame.image.load('./assets/sprites/pipe-red.png').convert_alpha()
           self.image = pygame.transform.scale(self.image, (LARGURA_CANO, ALTURA_CANO))
           
           self.rect = self.image.get_rect()
           self.rect[0] = xPos
           
           #IF PARA VER SE OS CANOS ESTAO INVERTIDOS
           #quando nao esta invertido a posição do canto superior esquerdo
           #ela depende da tela inteira - o tamanho que eu quero que o cano tenha
           #exemplo: se a tela for de 800px e eu quiser que o cano tenha 100px
           #o canto superior começa a contar de cima para baixo então o canto superior
           #tem que estar na altura 700px ou seja 800px - 100px (CANO NORMAL)
           ####################################################################################
           #para o cano invertido o canto superior esquerdo fica ao contrario então
           #a gente esconde um pedaço do cano para ele ter o tamanho que a gente quer
           #então por isso que nesse if utilizamos a posição negativa baseado na altura do cano
           # - o tamanho que eu quero que ele tenha, ou seja se meu cano por padrão tem 300px e eu quero
           #que ele tenha 200px. Então 300px - 200px = 100px. então aqui eu começaria ele com -100px
           #sobrando 200px ele inverte e fica um cano menor ou maior do original
           
           
           ## PASSAMOS PRIMEIRO O FALSE POIS NAO QUEREMOS INVERTER O X NÓS QUEREMOS INVERTER O Y
           if isCanoInvertido:
               self.image = pygame.transform.flip(self.image, False, True)
               self.rect[1] = - (self.rect[3] - ySize)
           else:
               self.rect[1] = ALTURA_TELA - ySize
               self.mascara = pygame.mask.from_surface(self.image)  
               
    def update(self): 
            self.rect[0] -= VELOCIDADE_JOGO  
         
                        
##Criando a classe chão      
class Chao(pygame.sprite.Sprite):
    def __init__(self, xPos):
        pygame.sprite.Sprite.__init__(self)
        
        ##adicionando a imagem
        self.image = pygame.image.load('./assets/sprites/base.png').convert_alpha()  
        self.image = pygame.transform.scale(self.image,(LARGURA_CHAO, ALTURA_CHAO))
        
        #criando mascara de colisão
        self.mascara = pygame.mask.from_surface(self.image)
        
        self.rect = self.image.get_rect()
        #definindo posição do segundo chão
        self.rect[0] = xPos
        #colocando o chão no chão
        self.rect[1] = ALTURA_TELA - ALTURA_CHAO
        
    def update(self):
        self.rect[0] -= VELOCIDADE_JOGO

def is_off_screen(sprite):
    #aqui fazemos uma função para veificar se o sprite saiu da tela
    return sprite.rect[0] < - (sprite.rect[2])

def get_random_canos(xPos):
    #criando os tamanhos dos canos aleatoriamente
    size = random.randint(100, 300)
    #criando o cano comum e passando os parametros da classe Cano()
    cano = Cano(False, xPos, size)
    #criando os canos invertidos passando os paramentros da classe Cano()
    cano_inverted = Cano(True, xPos, ALTURA_TELA - size - VAO_CANO)
    #retornando tupla com os canos
    return(cano, cano_inverted)

#Iniciando Jogo com os tamanhos de tela
pygame.init()
screen = pygame.display.set_mode((LARGURA_TELA,ALTURA_TELA))

##definindo FUNDO e tamanho do mesmo
FUNDO = pygame.image.load('./assets/sprites/background-day.png')
FUNDO = pygame.transform.scale(FUNDO, (LARGURA_TELA, ALTURA_TELA))

##criando grupo de passaro
passaro_grupo = pygame.sprite.Group()
passaro = Passaro()
passaro_grupo.add(passaro)

##criando grupo de chão

chao_grupo = pygame.sprite.Group()
    # na primeira interação o i vale 0 sendo o primeiro chão
    # na segunda interação o i vale 1 sendo o segundo chão
    # se tornando um laço fazendo com que o chão se tenha um tamanho maior
for i in range (2): 
    chao = Chao(LARGURA_CHAO * i)
    chao_grupo.add(chao)

cano_grupo = pygame.sprite.Group()
for i in range(2):
    canos = get_random_canos(LARGURA_TELA * i + 800)
    cano_grupo.add(canos[0])
    cano_grupo.add(canos[1])

##definindo FPS do jogo
clock = pygame.time.Clock()

##Looping infinito ativar o jogo
while True:
    clock.tick(15)
    for event in pygame.event.get(): 
        if event.type == QUIT:
            pygame.quit()
            
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                passaro.fly()
            
    screen.blit(FUNDO, (0, 0))
    
    #usando a função que criamos para deixar o chão infinito e não bugar o sprite
    if is_off_screen(chao_grupo.sprites()[0]):
        chao_grupo.remove(chao_grupo.sprites()[0])
        
        new_chao = Chao(LARGURA_CHAO - 20)
        chao_grupo.add(new_chao)
        
        #verificando se os canos ja estao fora da tela para apaga-los
        #e liberar memoria
    if is_off_screen(cano_grupo.sprites()[0]):
        #removendo canos normais
        cano_grupo.remove(cano_grupo.sprites()[0])
        #removendo canos invertidos
        cano_grupo.remove(cano_grupo.sprites()[0])
        
        #gerando canos mais a frente do personagem
        canos = get_random_canos(LARGURA_TELA * 2)
        
        #criando canos normais
        cano_grupo.add(canos[0])
        #criando canos invertidos
        cano_grupo.add(canos[1])
        
    
    ##atualizando sprites
    passaro_grupo.update()
    chao_grupo.update()
    cano_grupo.update()
    
    ##desenhar todos que estão no grupo
    passaro_grupo.draw(screen)
    chao_grupo.draw(screen)
    cano_grupo.draw(screen)
    
    ##definindo colisão para o personagem morrer
    if (pygame.sprite.groupcollide(passaro_grupo, chao_grupo, False, False, pygame.sprite.collide_mask) or
       pygame.sprite.groupcollide(passaro_grupo, cano_grupo, False, False, pygame.sprite.collide_mask)):
        #GameOver
        ##quando o personagem colidir ele acende o led vermelho
        gp.output(17,gp.HIGH)
        gp.output(18,gp.LOW)
        break
                
    pygame.display.update()