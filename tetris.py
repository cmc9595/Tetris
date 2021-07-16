import pygame
import time
import block
from block import Board, Block, block_size, blockColor
import random
import requests

pygame.init()
pygame.key.set_repeat(400, 75)

screen = None
volume = 0.5
key = None
gridSize = 20
pygame.mixer.music.load('전투3.mp3')
#pygame.mixer.music.play()

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
    screen.blit(pygame.font.Font(None, 30).render("Time: " + str(elapsed_time), True, block.BLACK), (10,10))
    screen.blit(pygame.font.Font(None, 30).render("Level: " + str(board.level), True, block.RED), (10, 30))
    screen.blit(pygame.font.Font(None, 30).render("Score: " + str(board.score), True, block.BLUE), (10, 50))
    screen.blit(pygame.font.Font(None, 30).render("Speed: " + str(board.speed), True, (0, 102, 0)), (10, 70))
    
    screen.blit(pygame.font.Font(None, 30).render("volume  +      -", True, block.BLUE), (420, screen.get_height()//2))
    screen.blit(pygame.font.Font(None, 30).render("EXIT", True, block.BLUE), (500, screen.get_height()//2 + 50))
    screen.blit(pygame.font.Font(None, 25).render("NEXTBLOCK", True, block.BLACK), (450, 25))

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

def server(id, score):
    current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    datas = {
        'id': id,
        'score': score,
        'time': current_time
    }
    response = requests.post('http://54.180.131.80:5000/post', data=datas)

def drawScoreBoard():
    #inputbox = pygame.Rect(screen.get_width()//2 - 150, screen.get_height()//2 - 200, 300, 400)
    #pygame.draw.rect(screen, block.WHITE, inputbox)
    pass
    
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
    
    # button list
    vol_rect_1 = pygame.Rect(500, screen.get_height()//2, 20, 20)
    vol_rect_2 = pygame.Rect(540, screen.get_height()//2, 20, 20)
    quit_rect = pygame.Rect(500, screen.get_height()//2 + 40, 50, 40)
    
    while not done:
        mouse = pygame.mouse.get_pos()
        clock.tick(12)
        screen.fill(block.WHITE)
        drawBackground(board)
        drawBoard(board)
        drawBlock(curBlock, nextBlock, board_x, board_y)
        
        # draw button
        pygame.draw.rect(screen, block.WHITE, vol_rect_1)
        pygame.draw.rect(screen, block.WHITE, vol_rect_2)
        pygame.draw.rect(screen, block.WHITE, quit_rect)
        
        drawText(board)
        
        if finish:
            screen.blit(pygame.font.Font(None, 50).render("Name : " + text + " < type", True, block.WHITE, 1), (150,100))
            screen.blit(pygame.font.Font(None, 50).render("Level : " + str(board.level), True, block.WHITE, 1), (150,150))
            screen.blit(pygame.font.Font(None, 50).render("Score : " + str(board.score), True, block.WHITE, 1), (150,200))
            #text_surf = pygame.font.SysFont('malgungothic', 50).render(text, True, block.WHITE, 0)
            #text_surf.get_rect().center = (150, 150)
            #screen.blit(text_surf, text_surf.get_rect())
            
            
            # 엔터 -> input_active = False
            if not input_active:
                if send_server:
                    server("temp", 100)
                    send_server = False
                    
                drawScoreBoard()
                
                gameover = pygame.font.Font(None, 70).render("Press R to Respawn", True, (255, 255, 255), 1)
                rect = gameover.get_rect()
                rect.center = screen.get_rect().center
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
                        input_active = True
                        board.finish_time = pygame.time.get_ticks()
                        break
                    board.updateBoard()
                    curBlock = nextBlock
                    nextBlock = createBlock(board)
                    
            elif event.type == pygame.KEYDOWN and input_active:
                if event.key == pygame.K_RETURN: # 엔터
                    input_active = False
                elif event.key == pygame.K_BACKSPACE: # 뒤로가기
                    text = text[:-1]
                else: 
                    text += event.unicode
                    
            
                
        keys = pygame.key.get_pressed()
        if finish:
            if not input_active and keys[pygame.K_r]: # respawn
                done = True
                main()
        
        else:
            if keys[pygame.K_LEFT]:
                if curBlock.checkLeft(board):
                    curBlock.x -= 1
            #test용
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