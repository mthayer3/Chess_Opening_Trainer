from ScotchGambit import my_dict
import random
import ChessEngine


def findRandomMove(validMoves, currBoard):
    if currBoard in my_dict.values():
        print("YOOOOOOOOOOOUUUUUUU")
        for key, value in my_dict.items():
            if value == currBoard:
                print(key)
        return ChessEngine.Move((1,4), (3,4), currBoard)
        
    else:
        return validMoves[random.randint(0, len(validMoves)-1)]

def findBestMove():
    pass

