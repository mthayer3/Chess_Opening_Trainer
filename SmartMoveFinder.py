from Pirc import my_dict
import random
import ChessEngine


def findRandomMove(validMoves, currBoard):
    
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
                if chance <= key[0][4]:
                    return ChessEngine.Move((key[0][0],key[0][1]), (key[0][2], key[0][3]), currBoard)
                
                        

                # return ChessEngine.Move()
        # return ChessEngine.Move((1,4), (3,4), currBoard)
        
    else:
        print("That is the end of CPU theory knowledge")
        return validMoves[random.randint(0, len(validMoves)-1)]
        
        

def findBestMove():
    pass

