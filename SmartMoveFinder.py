from ScotchGambit import my_dict
import random
import ChessEngine


def findRandomMove(validMoves, currBoard):
    # if currBoard in my_dict.values():
    #     print("YOOOOOOOOOOOUUUUUUU")
    for key, value in my_dict.items():
        if value == currBoard:
            
            chance = random.randint(1,100)
            print(chance)
            print(key)
            if len(key)>=2:

                for i in key:
                    if chance <= i[-1]:
                            return ChessEngine.Move((i[0],i[1]), (i[2], i[3]), currBoard)
                    

            else:
                if chance < key[-1]:
                        return ChessEngine.Move((key[0],key[1]), (key[2], key[3]), currBoard)
                
                        

                # return ChessEngine.Move()
        # return ChessEngine.Move((1,4), (3,4), currBoard)
        
    else:
        print("That is the end of CPU theory knowledge")
        return validMoves[random.randint(0, len(validMoves)-1)]
        
        

def findBestMove():
    pass

