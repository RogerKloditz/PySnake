import pygame,sys
from random import randint


pygame.init()

win = pygame.display.set_mode((400,400))
clock = pygame.time.Clock()

grid_x = [x for x in range(0,400,10)]
grid_y = [y for y in range(0,400,10)]

# Colors
BLACK = (0,0,0)
WHITE = (255,255,255)
SNAKE = (60,60,160)
FRAME = (160,70,70)

class Block():
    
    def __init__(self, x, y):
        
        self.x = x
        self.y = y
        self.width = 10
        self.height = 10
        self.hitbox = (self.x, self.y, self.width, self.height)
        self.snake = (self.x + 1, self.y + 1, self.width - 2, self.height - 2)

    def draw(self,win):
        pygame.draw.rect(win,SNAKE,self.snake)
        # pygame.draw.rect(win,(255,0,0),self.hitbox,1)

def redrawGameWindow(win,snake,food):
    win.fill(BLACK)
    for block in snake:
        block.draw(win)
    pygame.draw.rect(win,WHITE,(*food,10,10))
    pygame.draw.rect(win,FRAME,(0,0,400,400),12)
    
    pygame.display.update()    

def hitWall(block):
    
    hitLeft = (block.x) <= 0
    hitUp = block.y <= 0
    hitRight = block.x + block.width >= win.get_width()
    hitBottom = block.y + block.height >= win.get_height()

    if hitLeft or hitUp or hitRight or hitBottom:
        global run
        run = False

def hitSelf(snake):
    x_vals = [block.x for block in snake[:-1]]
    y_vals = [block.y for block in snake[:-1]]
    if snake[-1].x in x_vals and snake[-1].y in y_vals:
        global run
        run = False

def placeFood(snake):
    x_vals = [block.x for block in snake]
    y_vals = [block.y for block in snake]
    while True:
        i_x = randint(1,len(grid_x) - 3)
        i_y = randint(1,len(grid_y) - 3)
        x = grid_x[i_x]
        y = grid_y[i_y]
        if x not in x_vals and y not in y_vals:
            break
    return (x,y)

def findFood(food,block):
    if food[0] == block.x and food[1] == block.y:
        return True
    else:
        return False

snake = [Block(50,200),Block(60,200)]
old = 'R'
food = placeFood(snake)
run = True

while run:

    clock.tick(8)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    if not any(keys):    
        new = old

    if keys[pygame.K_UP]:
        if old in 'LR':
            new = 'U'
        else:
            new = old
            
    elif keys[pygame.K_DOWN]:
        if old in 'LR':
            new = 'D'
        else:
            new = old
            
    elif keys[pygame.K_LEFT]:
        if old in 'UD':
            new = 'L'
        else:
            new = old
            
    elif keys[pygame.K_RIGHT]:    
        if old in 'UD':
            new = 'R'
        else:
            new = old

    lastBlock = snake[-1]
    if new == 'U':
        x = lastBlock.x
        y = lastBlock.y - lastBlock.height
    elif new == 'D':
        x = lastBlock.x
        y = lastBlock.y + lastBlock.height
    elif new == 'L':
        x = lastBlock.x - lastBlock.width
        y = lastBlock.y
    elif new == 'R':
        x = lastBlock.x + lastBlock.width
        y = lastBlock.y
    
    snake.append(Block(x,y))
    
    old = new
        
    hitWall(snake[-1])
    #hitSelf(snake)
    
    found = findFood(food,snake[-1])

    if not found:
        snake.pop(0)
    else:
        food = placeFood(snake)

    redrawGameWindow(win,snake,food)

pygame.quit()
sys.exit()