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
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],
        ]
        self.whiteToMove = True
        self.moveLog = []
