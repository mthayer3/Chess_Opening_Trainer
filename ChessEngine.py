"""
This class is responsible for storing all information about the current state of the chess game. It will also be responsible for
determining valid moves. It will also keep a move log.
"""

class GameState():
    def __init__(self):
        """
        Board is an 8x8 2d list, each element of the list has two characters.
        The first character represents the color of the piece, "b" or "w". 
        The second character represents the type of piece "R", "N", "B", "Q", "K", "b".
        "--" represents an empty square with no piece.
        """
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"], 
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "wN", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],
        ]

        self.moveFunctions = {'p': self.getPawnMoves, 'R': self.getRookMoves, 'N': self.getKnightMoves, 'B': self.getBishopMoves,
        'Q': self.getQueenMoves, 'K': self.getKingMoves}


        self.whiteToMove = True
        self.moveLog = []
    #Takes a move as a parameter and executes it (this will not work for castling, pawn promotion, and en passant)
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move) #Log the move for the possibility of undoing
        self.whiteToMove = not self.whiteToMove #Swap whose turn it is

    def undoMove(self):
        if len(self.moveLog) != 0: #Make sure there is a move to undo
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove #Switch turns back


    
    # All moves considering checks
    # Get all possible moves
    # For each possible move, check to see if it is a valid move by doing the following:
    #     -make the move
    #     -generate all possible moves for opposing player
    #     -see if any of the moves attack your king
    #     -if king is safe, it is a valid move and add to list
    def getValidMoves(self):
        return self.getAllPossibleMoves()

    # All moves without considering checks
    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r,c, moves)
        return moves

    def getPawnMoves(self, r,c, moves):
        if self.whiteToMove:    #White pawn moves
            if self.board[r-1][c] == "--": #1 square pawn advance
                moves.append(Move((r,c), (r-1, c), self.board))
                if r == 6 and self.board[r-2][c] == "--": #2 square pawn advance
                    moves.append(Move((r,c), (r-2, c), self.board))
            if c-1 >= 0: #Captures to the left
                if self.board[r-1][c-1][0] == 'b':
                    moves.append(Move((r, c), (r-1, c-1), self.board))
            if c+1 <= 7:    #Captures to the right
                if self.board[r-1][c+1][0] == 'b':
                    moves.append(Move((r, c), (r-1, c+1), self.board))
        else:   #Black pawn moves
            if self.board[r+1][c] == "--": #1 square pawn advance
                moves.append(Move((r,c), (r+1, c), self.board))
                if r == 1 and self.board[r+2][c] == "--": #2 square pawn advance
                    moves.append(Move((r,c), (r+2, c), self.board))
            if c+1<= 7: #Captures to the left
               if self.board[r+1][c+1][0] == 'w':
                   moves.append(Move((r,c), (r+1, c+1), self.board))
            if c-1 >= 0: #Captures to the right
                if self.board[r+1][c-1][0] == 'w':
                    moves.append(Move((r,c), (r+1, c-1), self.board))


    def getQueenMoves(self, r, c, moves):
        if self.whiteToMove:
            for i in range(1,r+1):  #Queen move forward
                if self.board[r-i][c] == "--":
                    moves.append(Move((r,c), (r-i, c), self.board))
                else:
                    if self.board[r-i][c][0] == 'b':
                        moves.append(Move((r,c), (r-i, c), self.board))
                        break
                    if self.board[r-i][c][0] == 'w':
                        break
            
            for i in range(1,8-r):  #Queen move backward
                    if self.board[r+i][c] == "--":
                        moves.append(Move((r,c), (r+i, c), self.board))
                    else:
                        if self.board[r+i][c][0] == 'b':
                            moves.append(Move((r,c), (r+i, c), self.board))
                            break
                        if self.board[r+i][c][0] == 'w':
                            break

            for i in range(1,8-c):    #Queen move right
                if self.board[r][c+i] == "--":
                    moves.append(Move((r,c), (r, c+i), self.board))
                else:
                    if self.board[r][c+i][0] == 'b':
                        moves.append(Move((r,c), (r, c+i), self.board))
                        break
                    if self.board[r][c+i][0] == 'w':
                        break
            for i in range(1,c+1):    #Queen move left
                if self.board[r][c-i] == "--":
                    moves.append(Move((r,c), (r, c-i), self.board))
                else:
                    if self.board[r][c-i][0] == 'b':
                        moves.append(Move((r,c), (r, c-i), self.board))
                        break
                    if self.board[r][c-i][0] == 'w':
                        break
                    



    def getKnightMoves(self, r, c, moves):
        if self.whiteToMove:
            if r >= 2 and c >= 1:
                if self.board[r-2][c-1] == "--":
                    moves.append(Move((r,c), (r-2, c-1), self.board))
                else:
                    if self.board[r-2][c-1][0] == "b":
                        moves.append(Move((r,c), (r-2, c-1), self.board))
            if r >=2 and c <=6:
                if self.board[r-2][c+1] == "--":
                    moves.append(Move((r,c), (r-2, c+1), self.board))
                else:
                    if self.board[r-2][c+1][0] == "b":
                        moves.append(Move((r,c), (r-2, c+1), self.board))
            if r>=1 and c >=2:
                if self.board[r-1][c-2] == "--":
                    moves.append(Move((r,c), (r-1, c-2), self.board))
                else:
                    if self.board[r-1][c-2][0] == "b":
                        moves.append(Move((r,c), (r-1, c-2), self.board))

            if r <=6 and c >=2:
                if self.board[r+1][c-2] == "--":
                    moves.append(Move((r,c), (r+1, c-2), self.board))
                else:
                    if self.board[r+1][c-2][0] == "b":
                        moves.append(Move((r,c), (r+1, c-2), self.board))
            if r<=6 and c<= 5:
                if self.board[r+1][c+2] == "--":
                    moves.append(Move((r,c), (r+1, c+2), self.board))
                else:
                    if self.board[r+1][c+2][0] == "b":
                        moves.append(Move((r,c), (r+1, c+2), self.board))
            if r>=1 and c <=5:
                if self.board[r-1][c+2] == "--":
                    moves.append(Move((r,c), (r-1, c+2), self.board))
                else:
                    if self.board[r-1][c+2][0] == "b":
                        moves.append(Move((r,c), (r-1, c+2), self.board))
            if r<=5 and c>=1:
                if self.board[r+2][c-1] == "--":
                    moves.append(Move((r,c), (r+2, c-1), self.board))
                else:
                    if self.board[r+2][c-1][0] == "b":
                        moves.append(Move((r,c), (r+2, c-1), self.board))
            if r<= 5 and c<= 6:
                if self.board[r+2][c+1] == "--":
                    moves.append(Move((r,c), (r+2, c+1), self.board))
                else:
                    if self.board[r-2][c+1][0] == "b":
                        moves.append(Move((r,c), (r+2, c+1), self.board))
                

                    
     
           
                            



    def getRookMoves(self, r, c, moves):
        if self.whiteToMove:
            for i in range(1,r+1):  #Rook move forward
                if self.board[r-i][c] == "--":
                    moves.append(Move((r,c), (r-i, c), self.board))
                else:
                    if self.board[r-i][c][0] == 'b':
                        moves.append(Move((r,c), (r-i, c), self.board))
                        break
                    if self.board[r-i][c][0] == 'w':
                        break
            
            for i in range(1,8-r):  #Rook move backward
                    if self.board[r+i][c] == "--":
                        moves.append(Move((r,c), (r+i, c), self.board))
                    else:
                        if self.board[r+i][c][0] == 'b':
                            moves.append(Move((r,c), (r+i, c), self.board))
                            break
                        if self.board[r+i][c][0] == 'w':
                            break

            for i in range(1,8-c):    #Rook move right
                if self.board[r][c+i] == "--":
                    moves.append(Move((r,c), (r, c+i), self.board))
                else:
                    if self.board[r][c+i][0] == 'b':
                        moves.append(Move((r,c), (r, c+i), self.board))
                        break
                    if self.board[r][c+i][0] == 'w':
                        break
            for i in range(1,c+1):    #Rook move left
                if self.board[r][c-i] == "--":
                    moves.append(Move((r,c), (r, c-i), self.board))
                else:
                    if self.board[r][c-i][0] == 'b':
                        moves.append(Move((r,c), (r, c-i), self.board))
                        break
                    if self.board[r][c-i][0] == 'w':
                        break
            


    def getKingMoves(self, r, c, moves):
        if self.whiteToMove:
            if r>= 1:
                if self.board[r-1][c] == "--": #King move forward
                    moves.append(Move((r,c), (r-1, c), self.board))
                else:
                    if self.board[r-1][c][0] == "b":
                        moves.append(Move((r,c), (r-1, c), self.board))
            if c>=1:
                if self.board[r][c-1] == "--":  #King move left
                    moves.append(Move((r,c), (r, c-1), self.board))
                else:
                    if self.board[r][c-1][0] == "b":
                        moves.append(Move((r,c), (r, c-1), self.board))
            if r<= 6:
                if self.board[r+1][c] == "--":  #King move down
                    moves.append(Move((r,c), (r+1, c), self.board))
                else:
                    if self.board[r][c+1][0] == "b":
                        moves.append(Move((r,c), (r, c+1), self.board))
            if c<=6:
                if self.board[r-1][c] == "--":  #King move right
                    moves.append(Move((r,c), (r, c+1), self.board))
                else:
                    if self.board[r-1][c][0] == "b":
                        moves.append(Move((r,c), (r, c+1), self.board))
            if r>=1 and c>=1:
                if self.board[r-1][c-1] == "--":    #King move front left
                    moves.append(Move((r,c), (r-1, c-1), self.board))
                else:
                    if self.board[r-1][c-1][0] == "b":
                        moves.append(Move((r,c), (r-1, c-1), self.board))
            if r>=1 and c<=6:
                if self.board[r-1][c+1] == "--":    #King move front right
                    moves.append(Move((r,c), (r-1, c+1), self.board))
                else:
                    if self.board[r-1][c+1][0] == "b":
                        moves.append(Move((r,c), (r-1, c+1), self.board))
            if r<=6 and c>=1:
                if self.board[r+1][c-1] == "--":    #King move back left
                    moves.append(Move((r,c), (r+1, c-1), self.board))
                else:
                    if self.board[r-1][c-1][0] == "b":
                        moves.append(Move((r,c), (r+1, c-1), self.board))
            if r<=6 and c<=6:
                if self.board[r+1][c+1] == "--":    #King move back right
                    moves.append(Move((r,c), (r+1, c+1), self.board))
                else:
                    if self.board[r-1][c-1][0] == "b":
                        moves.append(Move((r,c), (r+1, c+1), self.board))






    def getBishopMoves(self, r, c, moves):
        pass



class Move():
    #Maps keys to values
    ranksToRows = {"1":7, "2":6, "3":5, "4":4, "5":3, "6": 2, "7":1, "8":0}
    rowsToRanks = {v:k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b":1, "c":2, "d":3, "e":4, "f":5, "g":6, "h":7}
    colsToFiles = {v:k for k, v in filesToCols.items()}

   
    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol

    # Overiding the equals method
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID


    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) +self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r,c):
        return self.colsToFiles[c] +self.rowsToRanks[r]
