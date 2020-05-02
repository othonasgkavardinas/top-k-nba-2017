#Othonas Gkavardinas
#AM 2620

from sys import argv
from time import time

def get_input(argv):
    if len(argv) != 2:
        print("Error: Wrong number of arguments!")
        print("Arguments: [1,..,5]")
        exit()
    
    return [ int(x)+2 for x in argv[1][1:-1].split(",") ]

def get_first_player(dominant_players, f):
    tokens = f.readline()[:-1].split(",")
    dominant_players[tokens[0]] = tuple([ int(x) for x in tokens[3:] ])

def print_results(dominant_players):
    print("Dominant players:")
    for key, value in dominant_players.items():
        print(key, " with ", value)



def main(argv):

    dominant_players = {}

    statistics = get_input(argv)

    f = open("2017_ALL.csv", "r")
    f.readline()

    get_first_player(dominant_players, f)

    for line in f:
        tokens = line[:-1].split(",")


        dominatedPlayers = []

        for key, value in dominant_players.items():
            domination = 0
            same = 0
            insertPlayer = False

            for i in statistics:
                if int(tokens[i]) > value[i-3]:
                    domination += 1
                elif int(tokens[i]) < value[i-3]:
                    domination -= 1
                else:
                    same +=1

            if domination + same == len(statistics):
                insertPlayer = True
                dominatedPlayers.append(key)
            elif domination - same == -(len(statistics)):
                insertPlayer = False
                break
            else:
                insertPlayer = True

        if insertPlayer:
            dominant_players[tokens[0]] = tuple([ int(x) for x in tokens[3:] ])

            for player in dominatedPlayers:
                dominant_players.pop(player)
                
    f.close()
    
    print_results(dominant_players)

start_time = time()
main(argv)
#dummy_main(argv)
print("total time: %s" %(time() - start_time))
