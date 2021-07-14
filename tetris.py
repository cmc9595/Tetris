import pygame
import time
import numpy as np
import block
from block import Pixel, Board, Block, block_shape, block_size, blockColor
from random import randrange
from copy import deepcopy

screen, clock = None, None
start_ticks = None
music = False # 시작과 틀려면 True
done, finish = False, False
key = None
gridSize = 20
board_x, board_y = 0, 0
board = None
curBlock = None
level, score = 1, 0
    
def createBlock():
    shapeNum = randrange(7)
    color = randrange(5)
    pos = [board.width//2 - block_size//2, 0]
    newBlock = Block(shapeNum, color, x=pos[0], y=pos[1])
    while not checkDown(newBlock):
        newBlock.y -= 1
    return newBlock

def drawBackground():
    gapX = board_x//4
    gapY = (screen.get_height() - board.height*gridSize)//4
    for i in range(4):
        pygame.draw.rect(screen, blockColor[i+2], 
                                 [i*gapX, 0, screen.get_width() - 2*i*gapX, screen.get_height()-i*gapY], 0)

def drawBoard():
    for i in range(0, board.height):
        for j in range(0, board.width):
            if board.board[i][j].val==0: # 배경
                pygame.draw.rect(screen, block.BLACK, 
                                 [board_x + j*gridSize, board_y + i*gridSize, gridSize, gridSize])
            elif board.board[i][j].val==1: # 블럭
                pygame.draw.rect(screen, blockColor[board.board[i][j].color], 
                                 [board_x + j*gridSize, board_y + i*gridSize, gridSize, gridSize])          
def drawBlock(cur):
    for i in range(block_size):
        for j in range(block_size):
            if cur.shape[i][j]==1: # 블럭색
                pygame.draw.rect(screen, blockColor[cur.color], 
                                 [board_x+(cur.x+j)*gridSize, board_y+(cur.y+i)*gridSize, gridSize, gridSize])
def drawText():
    game_font = pygame.font.Font(None, 30)
    elapsed_time = round((pygame.time.get_ticks() - start_ticks) / 1000, 1)
    timer = game_font.render("Time: " + str(elapsed_time), True, block.BLACK) # text, True, color
    screen.blit(timer, (10,10)) # 위치
    screen.blit(pygame.font.Font(None, 30).render("Level: " + str(level), True, block.RED), (10, 30))
    screen.blit(pygame.font.Font(None, 30).render("Score: " + str(score), True, block.BLUE), (10, 50))
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
                board.board[cur.y+i][cur.x+j] = Pixel(1, cur.color)
def checkLeft(cur):
    for [y, x] in curPos(cur): # coordinate list
        if x == 0 or board.board[y][x-1].val == 1:
            return False
    return True
def checkRight(cur):
    for [y, x] in curPos(cur): # coordinate list
        if x == board.width-1 or board.board[y][x+1].val == 1:
            return False
    return True
def checkDown(cur):
    for [y, x] in curPos(cur): # coordinate list
        if y < 0:
            continue
        if y == board.height-1 or board.board[y+1][x].val == 1:
            return False
    return True
def checkRotate(cur):
    nextBlock = deepcopy(cur)
    nextBlock.rotate()
    nextShape = nextBlock.shape
    for i in range(block_size):
        for j in range(block_size):
            if nextShape[i][j]==1 and not (0<=cur.x+j<=board.width-1 and 0<=cur.y+i<=board.height-1):
                return False
            if nextShape[i][j]==1 and board.board[cur.y+i][cur.x+j].val==1:
                return False
    return True
def Score(level, cnt):
    weight = [1, 2.5, 7.5, 30]
    return int(40*level*weight[cnt-1])
def updateBoard():
    global score
    tmpBoard = []
    for i in reversed(range(board.height)):
        if any(j.val==0 for j in board.board[i]):
            tmpBoard.append(board.board[i])
    cnt = board.height-len(tmpBoard)
    for i in range(cnt):
        tmpBoard.append([Pixel(0, block.WHITE) for _ in range(board.width)])
    board.board = tmpBoard[::-1]
    # update score
    if 0 < cnt <= 4:
        score += Score(level, cnt)
    print(cnt)
    
def main():
    global screen, clock, start_ticks, board, level, done, score, music, finish, curBlock
    global board_x, board_y
    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    clock = pygame.time.Clock()
    start_ticks = pygame.time.get_ticks()
    pygame.time.set_timer(pygame.USEREVENT, 1000) # 초당 event occur
    board_x, board_y = screen.get_width()//3, 0
    board = Board(width=10, height=20)
    level = 1
    score = 0
    done = False
    finish = False
    music = True
    pygame.mixer.music.load('POTC.mp3')
    pygame.mixer.music.play()
    
    while not done:
        clock.tick(12)
        screen.fill(block.WHITE)
        drawBackground()
        drawBoard()
        if not curBlock:
            curBlock = createBlock()
        drawBlock(curBlock)
        drawText()
        
        if finish:
            gameover = pygame.font.Font(None, 30).render("Press R to Respawn", False, (255, 255, 255))
            rect = gameover.get_rect()
            rect.center = screen.get_rect().center
            screen.blit(gameover, rect)
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.USEREVENT: # every 1sec
                
                if checkDown(curBlock):
                    curBlock.y += 1
                else: # 바닥 닿으면
                    if not finish:
                        blockToBoard(curBlock)
                        updateBoard()
                        curBlock = createBlock()
                        
                if 1 in [pixel.val for pixel in board.board[0]]: # 천장닿으면 finish
                    finish = True
                    break
                
        keys = pygame.key.get_pressed() 
        if keys[pygame.K_LEFT]:
            if checkLeft(curBlock):
                curBlock.x -= 1
        elif keys[pygame.K_RIGHT]:
            if checkRight(curBlock):
                curBlock.x += 1
        elif keys[pygame.K_UP] or keys[pygame.K_SPACE]:
            if checkRotate(curBlock):
                curBlock.rotate()
            else:
                print("can't rotate")
            
            # 다음 rotate한 shape 자리가 비었는지 확인하고
            # 비었으면 rotate
            # 하나라도 차있으면 안됨.
        elif keys[pygame.K_DOWN]:
            if checkDown(curBlock):
                curBlock.y += 1
                
        elif keys[pygame.K_r]:
            main()
            
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
    
if __name__ == '__main__':
    main()