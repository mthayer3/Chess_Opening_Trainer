from ScotchGambit import my_dict
import random


def findRandomMove(validMoves, currBoard):
    if currBoard in my_dict:
        print("YOOOOOOOOOOOUUUUUUU")
        # return validMoves[random.randint(0, len(validMoves)-1)]
        return validMoves[0]
    else:
        return validMoves[random.randint(0, len(validMoves)-1)]

def findBestMove():
    pass

