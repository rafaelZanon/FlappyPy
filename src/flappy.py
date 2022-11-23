##importando pygame
import pygame
from pygame.locals import *

##definindo variaveis 
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 800
SPEED = 10
GRAVITY = 1
GAME_SPEED = 10

GROUND_WIDTH = 2 * SCREEN_WIDTH
GROUND_HEIGHT = 100

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
        
##Criando a classe chão      
class Ground(pygame.sprite.Sprite):
    def __init__(self, xPos):
        pygame.sprite.Sprite.__init__(self)
        
        ##adicionando a imagem
        self.image = pygame.image.load('./assets/sprites/base.png')  
        self.image = pygame.transform.scale(self.image,(GROUND_WIDTH, GROUND_HEIGHT))
        
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
    
    ##atualizando sprites
    bird_group.update()
    ground_group.update()
    
    ##desenhar todos que estão no grupo
    bird_group.draw(screen)
    ground_group.draw(screen)
            
    pygame.display.update()