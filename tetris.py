import pygame
import time
import block
from block import Board, Block, block_size, blockColor
import random
import requests
from collections import namedtuple
import pygame
import os
import random
from copy import deepcopy

block_shape = [
    [
        [
            [0, 0, 0, 0],
            [0, 0, 1, 0],
            [0, 1, 1, 1],
            [0, 0, 0, 0]],
        [
            [0, 0, 0, 0],
            [0, 0, 1, 0],
            [0, 1, 1, 0],
            [0, 0, 1, 0]],
        [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 1, 1, 1],
            [0, 0, 1, 0]],
        [
            [0, 0, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 1, 1],
            [0, 0, 1, 0]]
    ],

    [
        [
            [0, 0, 0, 0],
            [0, 0, 1, 1],
            [0, 1, 1, 0],
            [0, 0, 0, 0]],
        [
            [0, 1, 0, 0],
            [0, 1, 1, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 0]]
    ],

    [
        [
            [0, 0, 0, 0],
            [0, 1, 1, 0],
            [0, 0, 1, 1],
            [0, 0, 0, 0]],
        [
            [0, 0, 1, 0],
            [0, 1, 1, 0],
            [0, 1, 0, 0],
            [0, 0, 0, 0]]
    ],
    
    [      
        [
            [0, 0, 1, 0],
            [0, 0, 1, 0],
            [0, 1, 1, 0],
            [0, 0, 0, 0]],
        [
            [0, 0, 0, 0],
            [0, 1, 1, 1],
            [0, 0, 0, 1],
            [0, 0, 0, 0]],
        [
            [0, 1, 1, 0],
            [0, 1, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 0, 0]],
        [
            [0, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 1, 1, 1],
            [0, 0, 0, 0]]
    ],
    [      
        [
            [0, 1, 0, 0],
            [0, 1, 0, 0],
            [0, 1, 1, 0],
            [0, 0, 0, 0]],
        [
            [0, 0, 0, 0],
            [0, 0, 0, 1],
            [0, 1, 1, 1],
            [0, 0, 0, 0]],
        [
            [0, 1, 1, 0],
            [0, 0, 1, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 0]],
        [
            [0, 0, 0, 0],
            [0, 1, 1, 1],
            [0, 1, 0, 0],
            [0, 0, 0, 0]]
    ],
    
    [      
        [
            [0, 0, 1, 0],
            [0, 0, 1, 0],
            [0, 0, 1, 0],
            [0, 0, 1, 0]],
        [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [1, 1, 1, 1],
            [0, 0, 0, 0]]
    ],
    
    [      
        [
            [0, 0, 0, 0],
            [0, 1, 1, 0],
            [0, 1, 1, 0],
            [0, 0, 0, 0]]
    ]
]
block_size = 4

BLACK= ( 0,  0,  0)
WHITE= (255,255,255)
BLUE = ( 0,  0,255)
CYAN = (0, 255, 255)
GREEN= ( 0,255,  0)
RED  = (255,  0,  0)
YELLOW = (255, 255, 0)
ORANGE = (255, 128, 0)
blockColor = [(255, 51, 51)	,
(255, 102, 51)	,(255, 153, 51)	,
(255, 204, 51)	,
(255, 255, 51)	,
(204, 255, 51)	,
(153, 255, 51)	,
(102, 255, 51)	,
(51, 255, 51)	,
(51, 255, 102)	,
(51, 255, 153)	,
(51, 255, 204)	,
(51, 255, 255)	,
(51, 204, 255)	,
(51, 153, 255)	,
(51, 102, 255)	,
(51, 51, 255)	,
(102, 51, 255)	,
(153, 51, 255)	,
(204, 51, 255)	,
(255, 51, 255)	,
(255, 51, 204)	,
(255, 51, 153)	,
(255, 51, 102)	,
(255, 51, 51)]

class Block():
    def __init__(self, n, color, x, y, rot=0):
        self.n = n
        self.color = color
        self.shape = block_shape[n][rot]
        self.x = x
        self.y = y
        self.rot = rot
        
    def rotate(self): # left 90 angle
        if self.n in [0, 3, 4]:
            self.rot = (self.rot + 1) % 4
        elif self.n in [1, 2, 5]:
            self.rot = (self.rot + 1) % 2
        else:
            pass
        self.shape = block_shape[self.n][self.rot]
     
    def curPos(self): # current position on board
        pos = []
        for i in range(block_size):
            for j in range(block_size):
                if self.shape[i][j]==1:
                    pos.append([self.y+i, self.x+j])
        return pos
    
    def checkLeft(self, board):
        for [y, x] in self.curPos(): # coordinate list
            if x == 0 or board.board[y][x-1].val == 1:
                return False
        return True
    
    def checkRight(self, board):
        for [y, x] in self.curPos(): # coordinate list
            if x == board.width-1 or board.board[y][x+1].val == 1:
                return False
        return True
    
    def checkDown(self, board):
        for [y, x] in self.curPos(): # coordinate list
            if y < -1:
                continue
            if y == board.height-1 or board.board[y+1][x].val == 1:
                return False
        return True
    
    def checkRotate(self, board):
        nextBlock = deepcopy(self)
        nextBlock.rotate()
        nextShape = nextBlock.shape
        for i in range(block_size):
            for j in range(block_size):
                if nextShape[i][j]==1 and not (0<=self.x+j<=board.width-1 and 0<=self.y+i<=board.height-1):
                    return False
                if nextShape[i][j]==1 and board.board[self.y+i][self.x+j].val==1:
                    return False
        return True
    
    def blockToBoard(self, board):
        for i in range(block_size):
            for j in range(block_size):
                if self.shape[i][j]==1:
                    board.board[self.y+i][self.x+j] = Pixel(1, self.color)


class SoundEffect():
    def __init__(self):
        self.sound = random.choice(os.listdir(os.getcwd()+'/resource/soundeffect'))
        self.soundObj = pygame.mixer.Sound('resource/soundeffect/' + self.sound)
        
    def play(self):
        self.soundObj.play()
        
Pixel = namedtuple('Pixel', 'val color')
class Board():
    def __init__(self, x, y, width, height, start_time):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.board = [[Pixel(0, WHITE) for _ in range(width)] for _ in range(height)]
        # pixel = (val, color)
        
        self.score = 0
        self.level = 1
        self.speed = 1000
        
        self.alive = True
        self.start_time = start_time
        self.finish_time = None
    
    def updateBoard(self):
        tmp = []
        for i in reversed(range(self.height)):
            if any(j.val==0 for j in self.board[i]):
                tmp.append(self.board[i])
        cnt = self.height-len(tmp)
        for i in range(cnt):
            tmp.append([Pixel(0, WHITE) for _ in range(self.width)])
        self.board = tmp[::-1]
        # update score
        if 0 < cnt <= 4: # line pop!
            soundEffect = SoundEffect()
            soundEffect.play()
            
            self.score += self.getScore(self.level, cnt)
            self.level += 1
            if 0 <= self.level <= 3:
                self.speed = int(self.speed*0.5)
            elif 4 <= self.level <= 7:
                self.speed = int(self.speed*0.9)
            elif 8<= self.level <= 10:
                self.speed = int(self.speed*0.95)
            else:
                self.speed = int(self.speed*0.99)
            pygame.time.set_timer(pygame.USEREVENT, self.speed)
    
    def getScore(self, level, cnt):
        weight = [1, 2.5, 7.5, 30]
        return int(40*level*weight[cnt-1])
    
    def updateLevel(self):
        pass
    
    def updateSpeed(self):
        pass
        
pygame.init()
pygame.font.init()
pygame.key.set_repeat(400, 75)

myfont = 'Sans'
fontsize = 20

screen = None
volume = 0.5
key = None
gridSize = 20
pygame.mixer.music.load('resource/전투3.mp3')
pygame.mixer.music.play()

def createBlock(board):
    shapeNum = random.randrange(7)
    color = random.randrange(len(blockColor))
    newBlock = Block(shapeNum, color, x=board.width//2 - block_size//2, y=0)
    return newBlock

def drawBackground(board):
    gapX = board.x//4
    gapY = (screen.get_height() - board.height*gridSize)//4
    for i in range(4):
        pygame.draw.rect(screen, blockColor[i+2], 
                                 [i*gapX, 0, screen.get_width() - 2*i*gapX, screen.get_height()-i*gapY], 0)
    pygame.draw.rect(screen, block.BLACK, 
                                 [450, 50, 100, 125], 0)

def drawBoard(board):
    for i in range(0, board.height):
        for j in range(0, board.width):
            if board.board[i][j].val==0: # 배경
                pygame.draw.rect(screen, block.BLACK, 
                                 [board.x + j*gridSize, board.y + i*gridSize, gridSize, gridSize])
            elif board.board[i][j].val==1: # 블럭
                pygame.draw.rect(screen, blockColor[board.board[i][j].color], 
                                 [board.x + j*gridSize, board.y + i*gridSize, gridSize, gridSize])  
                
    pygame.draw.line(screen, block.RED, [board.x , board.y + 4*gridSize], 
                     [board.x + board.width*gridSize, board.y + 4*gridSize], 3)
            
def drawBlock(cur, nxt, board_x, board_y):
    for i in range(block_size):
        for j in range(block_size):
            if cur.shape[i][j] == 1: # curBlock
                pygame.draw.rect(screen, blockColor[cur.color], 
                                 [board_x+(cur.x+j)*gridSize, board_y+(cur.y+i)*gridSize, gridSize, gridSize])
            if nxt.shape[i][j] == 1: # nextBlock
                pygame.draw.rect(screen, blockColor[nxt.color], 
                                 [450 + j*gridSize, 75 + i*gridSize, gridSize, gridSize])
                
def drawText(board):
    if board.finish_time:
        elapsed_time = round((board.finish_time - board.start_time) / 1000, 1)
    else:
        elapsed_time = round((pygame.time.get_ticks() - board.start_time) / 1000, 1)
    screen.blit(pygame.font.SysFont(myfont, 30).render("Time: " + str(elapsed_time), True, block.BLACK), (10,10))
    screen.blit(pygame.font.SysFont(myfont, 30).render("Level: " + str(board.level), True, block.RED), (10, 30))
    screen.blit(pygame.font.SysFont(myfont, 30).render("Score: " + str(board.score), True, block.BLUE), (10, 50))
    screen.blit(pygame.font.SysFont(myfont, 30).render("Speed: " + str(board.speed), True, (0, 102, 0)), (10, 70))
    
    screen.blit(pygame.font.SysFont(myfont, 30).render("volume  +      -", True, block.BLUE), (420, screen.get_height()//2))
    screen.blit(pygame.font.SysFont(myfont, 30).render("EXIT", True, block.BLUE), (500, screen.get_height()//2 + 50))
    screen.blit(pygame.font.SysFont(myfont, 20).render("NEXTBLOCK", True, block.BLACK), (450, 25))

def drawButton(rect, color):
    pygame.draw.rect(screen, color, rect)
    
def musicVolume(string):
    global volume
    if string=="+":
        volume = min(volume+0.2, 1)
    else:
        volume = max(volume-0.2, 0)
    print(volume)
    pygame.mixer.music.set_volume(volume)

def server(name, score, scoreList):
    current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    datas = {
        'name': name,
        'score': score,
        'time': current_time
    }
    response = requests.post('http://54.180.131.80:5000/post', data=datas)
    scoreList = response.text
    return scoreList
    
def drawScoreBoard(text, board, scoreList):
    inputbox = pygame.Rect(screen.get_width()//2 - 150, screen.get_height()//2 - 200, 300, 400)
    pygame.draw.rect(screen, block.WHITE, inputbox)
    scoreList = list(eval(scoreList)) # string to list
    pos = [150, 100]
    Xgap = 200
    Ygap = 40
    for i, [name, score, time] in enumerate(scoreList[:10]):
        if name==text and score==str(board.score):
            color = block.RED
        else:
            color = block.BLACK
        screen.blit(pygame.font.SysFont(myfont, 40).render(str(i+1) + "> " + name, True, color), 
                    (pos[0], pos[1] + i*Ygap))
        screen.blit(pygame.font.SysFont(myfont, 40).render(score, True, color), 
                    (pos[0] + Xgap, pos[1] + i*Ygap))
    #screen.blit(pygame.font.SysFont('malgungothic', 30).render(f"너 존나못해", True, block.RED), 
    #            (pos[0], pos[1] + 10*Ygap))
    
def main():
    global screen
    screen = pygame.display.set_mode((600, 600))
    clock = pygame.time.Clock()
    start_ticks = pygame.time.get_ticks()
    
    board_x, board_y = screen.get_width()//3, 0
    board = Board(board_x, board_y, width=10, height=25, start_time=start_ticks)
    pygame.time.set_timer(pygame.USEREVENT, board.speed) # 초당 event occur
    
    curBlock = createBlock(board)
    nextBlock = createBlock(board)
    
    done = False
    finish = False
    music = True
    send_server = False
    input_active = False
    text = ""
    scoreList = []
    # button list
    vol_rect_1 = pygame.Rect(510, screen.get_height()//2 + 10, 20, 20)
    vol_rect_2 = pygame.Rect(560, screen.get_height()//2 + 10, 20, 20)
    quit_rect = pygame.Rect(500, screen.get_height()//2 + 50, 50, 40)
    
    while not done:
        mouse = pygame.mouse.get_pos()
        clock.tick(12)
        screen.fill(block.WHITE)
        drawBackground(board)
        drawBoard(board)
        drawBlock(curBlock, nextBlock, board_x, board_y)
        #print(pygame.time.get_ticks())
        # draw button
        pygame.draw.rect(screen, block.WHITE, vol_rect_1)
        pygame.draw.rect(screen, block.WHITE, vol_rect_2)
        pygame.draw.rect(screen, block.WHITE, quit_rect)
        
        drawText(board)
        
        if finish:
            screen.blit(pygame.font.SysFont(myfont, 40).render("Name :", True, block.WHITE, 1), (150,100))
            if 0 <= pygame.time.get_ticks()%1000 <= 500: # blink
                screen.blit(pygame.font.SysFont(myfont, 40).render(text + "_", True, block.WHITE, 1), (275,100))
            
            screen.blit(pygame.font.SysFont(myfont, 40).render("Score : " + str(board.score), True, block.WHITE, 1), (150,140))
            #text_surf = pygame.font.SysFont('malgungothic', 50).render(text, True, block.WHITE, 0)
            #text_surf.get_rect().center = (150, 150)
            #screen.blit(text_surf, text_surf.get_rect())
            
            
            # 엔터 -> input_active = False
            if not input_active:
                if send_server: #  3333333333
                    scoreList = server(text, board.score, scoreList)
                    send_server = False
                    
                drawScoreBoard(text, board, scoreList)
                
                if 0 <= pygame.time.get_ticks()%2000 <= 1000: # blink
                    gameover = pygame.font.SysFont(myfont, 70).render("Press R to Respawn", True, (255, 255, 255), 1)
                    rect = gameover.get_rect()
                    rect.center = (screen.get_width()//2, screen.get_height()//2)
                    screen.blit(gameover, rect)
            
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if vol_rect_1.collidepoint(event.pos):
                    musicVolume("+")
                if vol_rect_2.collidepoint(event.pos):
                    musicVolume("-")
                if quit_rect.collidepoint(event.pos):
                    done = True
                
            elif event.type == pygame.USEREVENT and not finish: # every 1sec
                if curBlock.checkDown(board):   # 내려갈 공간 있으면
                    curBlock.y += 1
                else:                           # 없으면
                    curBlock.blockToBoard(board) # 보드에 그리고, 선 넘는지 검사
                    if any([pixel.val==1 for pixel in board.board[3]]): 
                        finish = True
                        input_active = True # 죽으면 11111111111111111
                        board.finish_time = pygame.time.get_ticks()
                        break
                    board.updateBoard()
                    curBlock = nextBlock
                    nextBlock = createBlock(board)
                    
            elif event.type == pygame.KEYDOWN and input_active: # 222222222222
                if event.key == pygame.K_RETURN: # 엔터
                    input_active = False
                    send_server = True
                elif event.key == pygame.K_BACKSPACE: # 뒤로가기
                    text = text[:-1]
                else: 
                    text += event.unicode
                    
            
                
        keys = pygame.key.get_pressed()
        if finish:
            if not input_active and keys[pygame.K_r]: # respawn
                done = True
                main()
            if not input_active and keys[pygame.K_ESCAPE]: # respawn
                done = True
        
        else:
            if keys[pygame.K_LEFT]:
                if curBlock.checkLeft(board):
                    curBlock.x -= 1
            #test용-----------------지우기.
            
            elif keys[pygame.K_ESCAPE]:
                finish = True
                input_active = True
                board.finish_time = pygame.time.get_ticks()
                
            elif keys[pygame.K_RIGHT]:
                if curBlock.checkRight(board):
                    curBlock.x += 1
            elif keys[pygame.K_UP] or keys[pygame.K_SPACE]: # rotate
                if curBlock.checkRotate(board):
                    curBlock.rotate()
                else:
                    print("can't rotate")
            elif keys[pygame.K_DOWN]:
                if curBlock.checkDown(board):
                    curBlock.y += 1
            
        pygame.display.update()  
        
if __name__ == '__main__':
    main()
    pygame.quit()
# display.update -> parameter만 update가능
# display.flip -> 화면전체