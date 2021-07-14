from collections import namedtuple

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
            [1, 1, 0, 0],
            [0, 1, 1, 0],
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
            [1, 1, 1, 0],
            [0, 0, 1, 0],
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
            [0, 0, 1, 0],
            [1, 1, 1, 0],
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
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [1, 1, 1, 1],
            [0, 0, 0, 0]],
        [
            [0, 0, 1, 0],
            [0, 0, 1, 0],
            [0, 0, 1, 0],
            [0, 0, 1, 0]]
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
blockColor = [RED, ORANGE, YELLOW, GREEN, CYAN, BLUE]

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
     
Pixel = namedtuple('Pixel', 'val color')

class Board():
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[Pixel(0, WHITE) for _ in range(width)] for _ in range(height)]
        # pixel = (val, color)
    
        
    
