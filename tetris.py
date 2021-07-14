import pygame
import time
import numpy as np
from block import Board, Block, block_shape, block_size
from random import randrange

BLACK= ( 0,  0,  0)
WHITE= (255,255,255)
BLUE = ( 0,  0,255)
GREEN= ( 0,255,  0)
RED  = (255,  0,  0)

pygame.init()
screen = pygame.display.set_mode((600, 600))
clock = pygame.time.Clock()

music = True # 시작과 틀려면 True
done = False
key = None
gridSize = 20
board_x = screen.get_width()//3
board_y = 0
curBlock = None

pygame.mixer.music.load('POTC.mp3')
#pygame.mixer.music.play()

board = Board(width=10, height=20)

def createBlock():
    shape = randrange(7)
    return Block(shape, x=4, y=0)

def drawGrid():
    for i in range(0, screen.get_height(), gridSize):
        for j in range(0, screen.get_width(), gridSize):
            pygame.draw.rect(screen, BLUE, pygame.Rect(j, i, gridSize, gridSize), 1)

def drawBoard():
    for i in range(0, board.height):
        for j in range(0, board.width):
            if board.board[i][j]==0: # 배경색
                pygame.draw.rect(screen, BLACK, 
                                 [board_x + j*gridSize, board_y + i*gridSize, gridSize, gridSize], 1)
            elif board.board[i][j]==1: # 블럭색
                pygame.draw.rect(screen, BLUE, 
                                 [board_x + j*gridSize, board_y + i*gridSize, gridSize, gridSize])
                
def drawBlock(cur):
    for i in range(block_size):
        for j in range(block_size):
            if cur.shape[i][j]==1: # 블럭색
                pygame.draw.rect(screen, BLUE, 
                                 [board_x+(cur.x+j)*gridSize, board_y+(cur.y+i)*gridSize, gridSize, gridSize])

def curPos(cur):
    pos = []
    for i in range(block_size):
        for j in range(block_size):
            if cur.shape[i][j]==1:
                pos.append([cur.y+i, cur.x+j])
    return pos

def blockToBoard(cur):
    for i in range(block_size):
        for j in range(block_size):
            if cur.shape[i][j]==1:
                board.board[cur.y+i][cur.x+j] = 1

def checkLeft(cur):
    for [y, x] in curPos(cur): # coordinate list
            if x == 0 or board.board[y][x-1] == 1:
                return False
    return True
def checkRight(cur):
    for [y, x] in curPos(cur): # coordinate list
            if x == board.width-1 or board.board[y][x+1] == 1:
                return False
    return True
def checkDown(cur):
    for [y, x] in curPos(cur): # coordinate list
            if y == board.height-1 or board.board[y+1][x] == 1:
                return False
    return True

pygame.time.set_timer(pygame.USEREVENT, 1000)       
while not done:
    clock.tick(10)
    screen.fill(WHITE)
    drawBoard()
    if not curBlock:
        curBlock = createBlock()
        
    drawBlock(curBlock)
    pos = curPos(curBlock)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.USEREVENT:
            
            if checkDown(curBlock):
                curBlock.y += 1
            else: # 바닥 닿으면
                blockToBoard(curBlock)
                curBlock = createBlock()
                
            if 1 in board.board[0]: # 천장닿으면
                done = True
                
    keys = pygame.key.get_pressed() 
    if keys[pygame.K_LEFT]:
        if checkLeft(curBlock):
            curBlock.x -= 1
    elif keys[pygame.K_RIGHT]:
        if checkRight(curBlock):
            curBlock.x += 1
    elif keys[pygame.K_UP]:
        print("UP")
        curBlock.rotate()
        
    elif keys[pygame.K_DOWN]:
        if checkDown(curBlock):
            curBlock.y += 1
            
    elif keys[pygame.K_SPACE]:
        print("SPACE")
    elif keys[pygame.K_m]:
        print("music")
        if music:
            pygame.mixer.music.pause()
            music = False
        else:
            pygame.mixer.music.unpause()
            music = True

    pygame.display.update()  
    # display.update -> parameter만 update가능
    # display.flip -> 화면전체
pygame.quit()