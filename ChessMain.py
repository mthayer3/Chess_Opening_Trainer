
"""
Responsible for handling user input and displaying current game state object
"""

import pygame as p
from chess_opening_trainer import ChessEngine

WIDTH = HEIGHT = 512
DIMENSION = 8 #Dimensions of a chess board are 8x8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15 # For animation
IMAGES = {}

'''
Initialize a global dictionary of images. This will be called exactly once in the main
'''
def loadImages():
    pieces = ['wp', 'bp', 'wR', 'bR', 'wK', 'bK', 'wQ', 'bQ', 'wB', 'bB', 'wN', 'bN']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))

'''
The main driver of the code. This will handle user input and updating the graphics
'''
def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    print(gs.board)




