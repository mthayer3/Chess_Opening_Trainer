
"""
Responsible for handling user input and displaying current game state object
"""

import pygame as p
import ChessEngine

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
    validMoves = gs.getValidMoves()
    moveMade = False #Flag variable for when a move is made
    animate = False ##Flag variable for when to animate a move
    loadImages() #Do before while loop to ensure it is only done once
    running = True
    sqSelected = () #No square is selected initially. Will keep track of the last click of the user (tuple: (row, col))
    playerClicks = [] #Keep track of player clicks 
    gameOver = False
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                if not gameOver:
                    location = p.mouse.get_pos() #(x, y) location of mouse
                    col = location[0]//SQ_SIZE
                    row = location[1]//SQ_SIZE
                    if sqSelected == (row, col): #User clicked the same square twice
                        sqSelected = () #Deselect
                        playerClicks= [] #Clear player clicks
                    else:
                        sqSelected = (row, col)
                        playerClicks.append(sqSelected) #Append for both 1st and 2nd clicks
                    if len(playerClicks) == 2: #After 2nd click
                        move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                        print(move.getChessNotation())
                        for i in range(len(validMoves)):

                            if move == validMoves[i]:
                                gs.makeMove(validMoves[i])
                                moveMade = True
                                animate = True
                                sqSelected = () 
                                playerClicks = []
                        if not moveMade:
                            playerClicks = [sqSelected]




            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undoMove()
                    moveMade = True
                    animate = False
                if e.key == p.K_r:   #Reset the board when 'r' is pressed
                    gs = ChessEngine.GameState()
                    validMoves = gs.getValidMoves()
                    sqSelected = ()
                    playerClicks = []
                    moveMade = False
                    animate = False

                    


        if moveMade:
            if animate:
                animateMove(gs.moveLog[-1], screen, gs.board, clock)
            validMoves = gs.getValidMoves()
            moveMade = False
            animate = False


        drawGameState(screen, gs, validMoves, sqSelected)

        if gs.checkmate:
            gameOver = True
            if gs.whiteToMove:
                drawText(screen, "Black wins by checkmate")
            else:
                drawText(screen, "White wins by checkmate")
        elif gs.stalemate:
            gameOver = True
            drawText(screen, "Stalemate")
        clock.tick(MAX_FPS)
        p.display.flip()

# Highlight square selected and moves for piece selected
#Add in a highlight of the last move made
def highlightSquares(screen, gs, validMoves, sqSelected):
    if sqSelected!= ():
        r, c = sqSelected
        if gs.board[r][c][0] == ('w' if gs.whiteToMove else 'b'):
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100)    #Transparency value. 0 = transparent, 255 = opaque
            s.fill(p.Color("blue"))
            screen.blit(s, (c*SQ_SIZE, r*SQ_SIZE))
            s.fill(p.Color('yellow'))
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s, (move.endCol*SQ_SIZE, move.endRow*SQ_SIZE))


"""
Responsible for all graphics within current game state
"""
def drawGameState(screen, gs, validMoves, sqSelected):
    drawBoard(screen) #Draw squares on the board
    highlightSquares(screen, gs, validMoves, sqSelected)
    drawPieces(screen, gs.board) #Draw pieces on top of the squares

"""
Draw the squares on the board. Top left square is always light
"""
def drawBoard(screen):
    global colors
    colors = [p.Color("white"), p.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c)%2)]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
    

"""
Draw the pieces on top of the board
"""
def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--": #Not empty square
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def animateMove(move, screen, board, clock):
    global colors
    coords = []
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    framesPerSquare = 10    #Frames to move one square
    frameCount = (abs(dR) + abs(dC)) * framesPerSquare
    for frame in range(frameCount + 1):
       r,c =  (move.startRow + dR* frame/frameCount, move.startCol + dC*frame/frameCount)
       drawBoard(screen)
       drawPieces(screen, board)
       color = colors[(move.endRow + move.endCol) % 2]
       endSquare = p.Rect(move.endCol * SQ_SIZE, move.endRow*SQ_SIZE, SQ_SIZE, SQ_SIZE)
       p.draw.rect(screen, color, endSquare)

       if move.pieceCaptured != "--":
           screen.blit(IMAGES[move.pieceCaptured], endSquare)
        
       screen.blit(IMAGES[move.pieceMoved], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
       p.display.flip()
       clock.tick(60)

def drawText(screen, text):
    font = p.font.SysFont("Helvitca", 32, True, False)
    textObject = font.render(text, 0, p.Color("Black"))
    textLocation = p.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH/2 - textObject.get_width()/2, HEIGHT/2 - textObject.get_height()/2)
    screen.blit(textObject, textLocation)
    textObject = font.render(text, 0, p.Color("Gray"))
    screen.blit(textObject, textLocation.move(2,2))

if __name__ == "__main":
    main()

main()



