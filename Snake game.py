import sys
import pygame
from pygame.math import Vector2
import random
pygame.init()
pygame.display.init()

white = (255 , 255, 255)
black =  (0,0,0)
red = (255,0,0)
purple = (163, 73, 164)
green = (0, 255, 0)
blue = (114, 208, 214)
#change the path according to your folder location
fruit_img = pygame.image.load(r'C:\Users\Yousuf Traders\Desktop\Pfun-L3\Pfun\Python Project\Project-Orochimaru\apple.PNG')

#Setting the board
box_area = 25
box_num = 20 #This is done to simulate a grid.  
window = pygame.display.set_mode((box_area*box_num,box_area*box_num))    
caption = pygame.display.set_caption('Orochimaru') 
clock = pygame.time.Clock() 
game_font = pygame.font.Font(None,25)


class SNAKE():
    def __init__(self):
        self.bodypart = [Vector2(7,10),Vector2(6,10),Vector2(5,10),Vector2(4,10),Vector2(3,10),Vector2(2,10)]   #use vector method to represent the cooedinates, use a list to store the pats of the body
        self.direction = Vector2(1 , 0)
        self.new_block = False
        #change the path according to your folder location
        self.eating_sound = pygame.mixer.Sound(r'C:\Users\Yousuf Traders\Desktop\Pfun-L3\Pfun\Python Project\Project-Orochimaru\crunch.wav') #cite pygame documentation in report
    
    def draw_snake(self):
        for block in self.bodypart:
            x = block.x * box_area
            y = block.y * box_area
            body_part_rect = pygame.Rect(x, y , box_area , box_area)
            pygame.draw.rect(window, red, body_part_rect)

    def move(self):
        if self.new_block == True:
            new_pos = self.bodypart[:]       
            new_pos.insert(0,new_pos[0] + self.direction)  
            self.bodypart = new_pos[:]
            self.new_block = False # so that the snake doesn't grow infinitely 
        else:
            new_pos = self.bodypart[:-1] #we do this slicing because we want the last block to dissapear/be deleted.
            new_pos.insert(0,new_pos[0] + self.direction)  # new_pos[0] + direction | What we are doing here is inserting the new position of the head in our  new_pos (the new position) list.
            self.bodypart = new_pos[:]    

    def add_snake(self):
        self.new_block = True

    def eat_sound(self):
        self.eating_sound.play()    

class FRUIT():
    def __init__(self):
        self.change_pos_fruit() #By initializing this method we will be able to change the position of the fruit when the snake eats it. Because we have made a conditin in the main loop of checking when the snake and the fruit overlap    
        #create a square
    def drawing_fruit(self):
        fruit_rect = pygame.Rect(self.pos_fruit.x*box_area,self.pos_fruit.y*box_area,box_area/2,box_area/2)
        # pygame.draw.rect(window,green,fruit_rect) #if decide to change box to apple, load image, then use the blit() function and use fruit_rect for location of apple
        window.blit(fruit_img,fruit_rect)

    def change_pos_fruit(self ):
        self.x = random.randint(0,box_num - 1)
        self.y = random.randint(0,box_num -1)   
        #create an x and y coordinate| we will be using pygame.math.Vector2() for this, vector, we use vector because it is easy for vector addition which will help in movement of the snake
        self.pos_fruit = Vector2(self.x,self.y)        
            

class MAINLOOP():
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()

    def update(self):       #we have used a cutom user event (continous motion) and set a timer to it with time of 150 ns. Now we have used this custom event in line  
        self.snake.move()
        self.checkfruit_eat()
        self.snake_death()

    def drawing_fruit_and_snake(self):
        self.fruit.drawing_fruit()
        self.snake.draw_snake()
        self.score()
        
    def score(self):  #report 
        score_txt = str(len(self.snake.bodypart)-4)
        score = game_font.render(score_txt, True,red)
        s_x = int(box_area*box_num - 40)
        s_y = int(box_area*box_num - 30)
        scorerect = score.get_rect(center = (s_x,s_y))
        window.blit(score,scorerect)

    def checkfruit_eat(self): 
        if  self.fruit.pos_fruit ==  self.snake.bodypart[0]:  #everything that hppens after snake munches on the fruit
            self.fruit.change_pos_fruit()
            self.snake.add_snake()# Ading another block to snake after eating
            self.snake.eat_sound()

    def snake_death(self):
        if  self.snake.bodypart[0].x >= box_num  or self.snake.bodypart[0].x < 0 or self.snake.bodypart[0].y >= box_num  or self.snake.bodypart[0].y < 0:
            self.crashed() #if the snake is out of bounds
        
        #if the snake touches it self
        for block in self.snake.bodypart[1:]:
            if block == self.snake.bodypart[0]:
               self.crashed() 
   
    def crashed(self):
        pygame.quit()
        sys.exit()        

            







# fruit = FRUIT()  #instance if snake and fruit
# snake = SNAKE()

continous_motion = pygame.USEREVENT #custom event 
pygame.time.set_timer(continous_motion,100)

game_engine = MAINLOOP() #main game loop is like the engine of the game

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
 
        if event.type == pygame.KEYDOWN:
            if game_engine.snake.direction.x == 1 or game_engine.snake.direction.x == -1:
                if event.key == pygame.K_UP:
                    game_engine.snake.direction = Vector2(0, -1)
                if event.key == pygame.K_DOWN:
                    game_engine.snake.direction = Vector2(0,+1)
            elif game_engine.snake.direction.y == 1 or game_engine.snake.direction.y == -1:        
                if event.key == pygame.K_RIGHT:
                    game_engine.snake.direction = Vector2(1, 0)
                if event.key == pygame.K_LEFT:
                    game_engine.snake.direction = Vector2(-1,0)
# when i did not write the nested if statement the snake was able to change his direction in a manner which is not physically posible, i.e. it would change from righ to ledt without first going up or down



        if event.type == continous_motion:
            game_engine.update()  

        window.fill(blue)
        game_engine.drawing_fruit_and_snake()
        
        

        pygame.display.update()
        clock.tick(60)        


