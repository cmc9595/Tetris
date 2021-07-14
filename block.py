import numpy as np
block_shape = [[[0, 0, 0, 0],
                [0, 0, 1, 0],
                [0, 1, 1, 1],
                [0, 0, 0, 0]],
               
               [[0, 0, 0, 0],
                [0, 0, 1, 1],
                [0, 1, 1, 0],
                [0, 0, 0, 0]],
               
               [[0, 0, 0, 0],
                [0, 1, 1, 0],
                [0, 0, 1, 1],
                [0, 0, 0, 0]],
               
               [[0, 0, 1, 0],
                [0, 0, 1, 0],
                [0, 1, 1, 0],
                [0, 0, 0, 0]],
               
               [[0, 1, 0, 0],
                [0, 1, 0, 0],
                [0, 1, 1, 0],
                [0, 0, 0, 0]],
               
               [[0, 0, 1, 0],
                [0, 0, 1, 0],
                [0, 0, 1, 0],
                [0, 0, 1, 0]],
               
               [[0, 0, 0, 0],
                [0, 1, 1, 0],
                [0, 1, 1, 0],
                [0, 0, 0, 0]]
] # block_shape[0~6]
block_size = 4

class Block():
    def __init__(self, n, x, y, rotate=0):
        self.n = n
        self.shape = block_shape[n]
        self.x = x
        self.y = y
        self.rot = rotate
        
    def rotate(self): # left 90 angle
        self.shape = np.array(self.shape)
        self.shape = np.rot90(self.shape)
        self.rot = (self.rot + 1)%4
        
class Board():
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0 for _ in range(width)] for _ in range(height)]
    
        
    
