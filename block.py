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
        self.sound = random.choice(os.listdir(os.getcwd()+'/soundeffect'))
        self.soundObj = pygame.mixer.Sound('soundeffect/' + self.sound)
        
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
        