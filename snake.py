# WRITTEN BY OM [byt-ctrl]

import pygame
import random
import sys
from pygame.math import Vector2

# Initialize pygame
pygame.init()

# Game settings
CELL_SIZE=20
GRID_WIDTH=30
GRID_HEIGHT=20
SCREEN_WIDTH=CELL_SIZE * GRID_WIDTH
SCREEN_HEIGHT=CELL_SIZE * GRID_HEIGHT
FPS=10

# colors
BLACK=(0,0,0)
GREEN=(0,255,0)
DARK_GREEN=(0,200,0)
RED=(255,0,0)
WHITE=(255,255,255)

class Snake:
    def __init__(self) :
        self.body=[Vector2(5,10),Vector2(4,10),Vector2(3,10)]
        self.direction=Vector2(1,0)
        self.new_block=False
        
        # loading the sound effects
        """ Used sfxr to make the sound effects""" # sound can be customized as per needed

        self.eat_sound=pygame.mixer.Sound("sound.wav") if pygame.mixer.get_init() else None
        self.game_over_sound=pygame.mixer.Sound("dead.wav") if pygame.mixer.get_init() else None
        
    def draw(self,screen) :

        for a, block in enumerate(self.body):

            # creating a rectangle for game
            x_pos=int(block.x*CELL_SIZE)
            y_pos=int(block.y*CELL_SIZE)
            block_rect=pygame.Rect(x_pos,y_pos,CELL_SIZE,CELL_SIZE)
            
            # drawing the snake

            if a==0 :  # head
                pygame.draw.rect(screen,GREEN,block_rect)
            else:  # body
                pygame.draw.rect(screen,DARK_GREEN,block_rect)
            
            # adding a border to the snake
            pygame.draw.rect(screen,BLACK,block_rect,1)
    
    def move(self) :
        if self.new_block :
            body_copy=self.body[:]
            body_copy.insert(0,body_copy[0] +self.direction)
            self.body=body_copy
            self.new_block=False
        else  :
            body_copy=self.body[:-1]
            body_copy.insert(0, body_copy[0]+self.direction)
            self.body= body_copy
    
    def grow(self) :
        self.new_block=True
        if self.eat_sound :
            self.eat_sound.play()
    
    def reset(self) :
        self.body=[Vector2(5,10),Vector2(4,10),Vector2(3,10)]
        self.direction=Vector2(1,0)

class Food :
    def __init__(self) :
        self.randomize_position()
    
    def draw(self,screen) :
        food_rect=pygame.Rect(int(self.pos.x*CELL_SIZE) , int(self.pos.y*CELL_SIZE),CELL_SIZE,CELL_SIZE)
        pygame.draw.rect(screen,RED,food_rect)
        pygame.draw.rect(screen,BLACK,food_rect,1)
    
    def randomize_position(self) :
        self.x=random.randint(0,GRID_WIDTH-1)
        self.y=random.randint(0,GRID_HEIGHT-1)
        self.pos=Vector2(self.x,self.y)

class Game :
    def __init__(self) :
        self.snake=Snake()
        self.food=Food()
        self.score=0
        self.game_over=False
        self.font=pygame.font.SysFont("Arial",26)
        
    def update(self) :
        if not self.game_over :
            self.snake.move()
            self.check_collision()
            self.check_fail()
    
    def draw(self,screen) :
        screen.fill(BLACK)
        self.draw_grid(screen)
        self.food.draw(screen)
        self.snake.draw(screen)
        self.draw_score(screen)
        
        if self.game_over :
            self.draw_game_over(screen)
    
    def draw_grid(self,screen) :
        for a in range(GRID_WIDTH) :
            pygame.draw.line(screen, (40,40,40), (a*CELL_SIZE,0), (a*CELL_SIZE,SCREEN_HEIGHT))
        for a in range(GRID_HEIGHT):
            pygame.draw.line(screen, (40,40,40), (0,a*CELL_SIZE), (SCREEN_WIDTH,a *CELL_SIZE))
    
    def check_collision(self) :
        if self.food.pos==self.snake.body[0] :
            self.food.randomize_position()

            # ensuring the food does not spawn on the snake body
            while self.food.pos in self.snake.body:
                self.food.randomize_position()
            self.snake.grow()
            self.score+=1
    
    def check_fail(self) :
        # checks if snake hits the wall
        if not 0 <= self.snake.body[0].x<GRID_WIDTH or not 0<=self.snake.body[0].y<GRID_HEIGHT:
            self.game_over=True
            if self.snake.game_over_sound :
                self.snake.game_over_sound.play()
        
        # checks if snake hits itself
        for block in self.snake.body[1:] :
            if block==self.snake.body[0] :
                self.game_over=True
                if self.snake.game_over_sound :
                    self.snake.game_over_sound.play()
    
    def draw_score(self, screen) :
        score_text=self.font.render(f"Score : {self.score}",True,WHITE)
        screen.blit(score_text,(11,11))
    
    def draw_game_over(self, screen) :
        game_over_surface=self.font.render(" GAME OVER! Press SPACE to restart ",True,WHITE)
        game_over_rect=game_over_surface.get_rect(center=(SCREEN_WIDTH/2,SCREEN_HEIGHT/2))
        screen.blit(game_over_surface,game_over_rect)
    
    def reset(self) :
        self.snake.reset()
        self.food.randomize_position()
        self.score=0
        self.game_over=False

def main() :
    # initiallize screen
    screen=pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
    pygame.display.set_caption (" Snake Game ")
    clock=pygame.time.Clock()
    
    # ceating game object
    game=Game()
    
    # creating game loop
    while True :
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type==pygame.KEYDOWN :
                if game.game_over and event.key==pygame.K_SPACE : 
                    game.reset()
                
                # snake controls
                if not game.game_over :
                    if event.key==pygame.K_UP and game.snake.direction.y != 1 :
                        game.snake.direction = Vector2(0,-1)
                    if event.key==pygame.K_DOWN and game.snake.direction.y != -1 :
                        game.snake.direction = Vector2(0,1)
                    if event.key==pygame.K_LEFT and game.snake.direction.x != 1 :
                        game.snake.direction = Vector2(-1,0)
                    if event.key==pygame.K_RIGHT and game.snake.direction.x != -1 :
                        game.snake.direction = Vector2(1,0)
        
        # updating game state
        game.update()
        
        # drawing game objects
        game.draw(screen)
        
        # updating the display
        pygame.display.update()
        clock.tick(FPS)

main()


# END OF FILE