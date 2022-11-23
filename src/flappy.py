##importando pygame
import pygame, random
from pygame.locals import *

##definindo variaveis 
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 800
SPEED = 10
GRAVITY = 1
GAME_SPEED = 10

GROUND_WIDTH = 2 * SCREEN_WIDTH
GROUND_HEIGHT = 100

PIPE_WIDTH = 80
PIPE_HEIGHT = 500
PIPE_GAP = 200

##Classe bird (personagem)
class Bird(pygame.sprite.Sprite):
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        
        ##definindo os sprites do passaro
        self.images = [pygame.image.load('./assets/sprites/bluebird-upflap.png').convert_alpha(),
                       pygame.image.load('./assets/sprites/bluebird-midflap.png').convert_alpha(),
                       pygame.image.load('./assets/sprites/bluebird-downflap.png').convert_alpha()]  
        
        self.speed = SPEED
        
        self.current_image = 0
        
        ##começando o jogo com essa sprite!
        self.image = pygame.image.load('./assets/sprites/bluebird-upflap.png').convert_alpha()
        #criando mascara de colisão
        self.mask = pygame.mask.from_surface(self.image)
        
        self.rect = self.image.get_rect()
        ##Colocando o passaro no meio da tela divindo os tamanhos por 2 
        self.rect[0] = SCREEN_WIDTH / 2
        self.rect[1] = SCREEN_HEIGHT / 2
        
    def update(self):
        self.current_image = (self.current_image + 1) % 3
        self.image = self.images [ self.current_image ]
        
        self.speed += GRAVITY
        
        ## alterando o height fazendo o passaro cair
        self.rect[1] += self.speed
        
    def fly(self):
        self.speed = -SPEED  
        
        
##Criando a classe cano
class Pipe(pygame.sprite.Sprite):
            
    def __init__(self, invertedPipe, xPos, ySize):
           pygame.sprite.Sprite.__init__(self)
        
           self.image = pygame.image.load('./assets/sprites/pipe-red.png').convert_alpha()
           self.image = pygame.transform.scale(self.image, (PIPE_WIDTH, PIPE_HEIGHT))
           
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
           
           if invertedPipe:
               self.image = pygame.transform.flip(self.image, False, True)
               self.rect[1] = - (self.rect[3] - ySize)
           else:
               self.rect[1] = SCREEN_HEIGHT - ySize
               self.mask = pygame.mask.from_surface(self.image)  
               
    def update(self): 
            self.rect[0] -= GAME_SPEED  
         
                        
##Criando a classe chão      
class Ground(pygame.sprite.Sprite):
    def __init__(self, xPos):
        pygame.sprite.Sprite.__init__(self)
        
        ##adicionando a imagem
        self.image = pygame.image.load('./assets/sprites/base.png').convert_alpha()  
        self.image = pygame.transform.scale(self.image,(GROUND_WIDTH, GROUND_HEIGHT))
        
        #criando mascara de colisão
        self.mask = pygame.mask.from_surface(self.image)
        
        self.rect = self.image.get_rect()
        #definindo posição do segundo chão
        self.rect[0] = xPos
        #colocando o chão no chão
        self.rect[1] = SCREEN_HEIGHT - GROUND_HEIGHT
        
    def update(self):
        self.rect[0] -= GAME_SPEED

def is_off_screen(sprite):
    #aqui fazemos uma função para veificar se o sprite saiu da tela
    return sprite.rect[0] < - (sprite.rect[2])

def get_random_pipes(xPos):
    #criando os tamanhos dos canos aleatoriamente
    size = random.randint(100, 300)
    #criando o cano comum e passando os parametros da classe Pipe()
    pipe = Pipe(False, xPos, size)
    #criando os canos invertidos passando os paramentros da classe Pipe()
    pipe_inverted = Pipe(True, xPos, SCREEN_HEIGHT - size - PIPE_GAP)
    #retornando tupla com os canos
    return(pipe, pipe_inverted)

#Iniciando Jogo com os tamanhos de tela
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

##definindo background e tamanho do mesmo
BACKGROUND = pygame.image.load('./assets/sprites/background-day.png')
BACKGROUND = pygame.transform.scale(BACKGROUND, (SCREEN_WIDTH, SCREEN_HEIGHT))

##criando grupo de passaro
bird_group = pygame.sprite.Group()
bird = Bird()
bird_group.add(bird)

##criando grupo de chão

ground_group = pygame.sprite.Group()
    # na primeira interação o i vale 0 sendo o primeiro chão
    # na segunda interação o i vale 1 sendo o segundo chão
    # se tornando um laço fazendo com que o chão se tenha um tamanho maior
for i in range (2): 
    ground = Ground(GROUND_WIDTH * i)
    ground_group.add(ground)

pipe_group = pygame.sprite.Group()
for i in range(2):
    pipes = get_random_pipes(SCREEN_WIDTH * i + 800)
    pipe_group.add(pipes[0])
    pipe_group.add(pipes[1])

##definindo FPS do jogo
clock = pygame.time.Clock()

##Looping infinito ativar o jogo
while True:
    clock.tick(30)
    for event in pygame.event.get(): 
        if event.type == QUIT:
            pygame.quit()
            
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                bird.fly()
            
    screen.blit(BACKGROUND, (0, 0))
    
    #usando a função que criamos para deixar o chão infinito e não bugar o sprite
    if is_off_screen(ground_group.sprites()[0]):
        ground_group.remove(ground_group.sprites()[0])
        
        new_ground = Ground(GROUND_WIDTH - 20)
        ground_group.add(new_ground)
        
        #verificando se os canos ja estao fora da tela para apaga-los
        #e liberar memoria
    if is_off_screen(pipe_group.sprites()[0]):
        #removendo canos normais
        pipe_group.remove(pipe_group.sprites()[0])
        #removendo canos invertidos
        pipe_group.remove(pipe_group.sprites()[0])
        
        #gerando canos mais a frente do personagem
        pipes = get_random_pipes(SCREEN_WIDTH * 2)
        
        #criando canos normais
        pipe_group.add(pipes[0])
        #criando canos invertidos
        pipe_group.add(pipes[1])
        
    
    ##atualizando sprites
    bird_group.update()
    ground_group.update()
    pipe_group.update()
    
    ##desenhar todos que estão no grupo
    bird_group.draw(screen)
    ground_group.draw(screen)
    pipe_group.draw(screen)
    
    ##definindo colisão para o personagem morrer
    if (pygame.sprite.groupcollide(bird_group, ground_group, False, False, pygame.sprite.collide_mask) or
       pygame.sprite.groupcollide(bird_group, pipe_group, False, False, pygame.sprite.collide_mask)):
        #GameOver
        input()
        break
        
            
    pygame.display.update()