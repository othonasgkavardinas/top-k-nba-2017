#import operator
from sys import argv
from time import time
import heapq

files = ["TRB", "AST", "STL", "BLK", "PTS"]

class Player:
    id1 = -1
    extra_files = []

    def __init__(self, id1, files_list):
        self.id1 = id1
        self.extra_files = files_list

class PriorityQueue(object):
    def __init__(self):
        self.queue = []
        self.dict = {}
        self.ids_dict = {}

    def insert(self, playerID, files_list, score, file):

        if not score in self.dict: self.dict[score] = []
        self.dict[score].append(Player(playerID, [ x for x in files_list ]))
        self.dict[score][len(self.dict[score])-1].extra_files.remove(file)
        self.ids_dict[playerID] = score

        heapq.heappush(self.queue, -score)

    def popMax(self):

        score = -(heapq.heappop(self.queue))
        player = self.dict[score].pop()
        
        if not self.dict[score]: del self.dict[score]
        del self.ids_dict[player.id1]

        return player, score

    def change_lb(self, id1, addition, file):

        score = self.ids_dict[id1]
        new_score = score + addition
 
        self.queue.remove(-score)
        self.queue.append(-(new_score))
        heapq.heapify(self.queue)

        if not new_score in self.dict: self.dict[new_score] = []
        for player in self.dict[score]:
            if player.id1 == id1:
                self.dict[new_score].append(player)
                self.dict[score].remove(player)
                break
        if not self.dict[score]: del self.dict[score]
        self.dict[new_score][len(self.dict[new_score])-1].extra_files.remove(file)
        self.ids_dict[id1] = new_score


def get_input(argv):
    if len(argv) != 3:
        print("Error: Wrong number of arguments!")
        print("Arguments: [1,..,5] k")
        exit()
    
    return [ int(x)-1 for x in argv[1][1:-1].split(",") ], int(argv[2])

def open_files(statistics):
    global files

    files_list = []

    for stat in statistics:
        files_list.append(open("2017_"+files[stat]+".csv", "r"))
    return files_list

def find_top_k(files_list, k, q):

    count_lines = 0
    result = []
    max_values = get_max_values(files_list)
    has_lines = True
    my_k = k

    while my_k != 0:
        all_values = []
        
        if has_lines:
            count_lines += 1
            for file in files_list:
                line = file.readline()
                if line:
                    playerID, value = [ int(x) for x in line.split(",") ]
                    score = func(max_values, value, file)
                    if not add_player(playerID, files_list, score, q, file):
                        set_value(playerID, score, q, file)
                    all_values.append(score)
                else:
                    has_lines = False
                    count_lines -= 1
                    break
        if not q.ids_dict: break
        t = calculate_t(q)
        T = calculate_T(all_values)
        if t >= T:
            upper_bound = max_upper_bound(all_values, files_list, q)
            if check_for_top(upper_bound, q):
                player, score = q.popMax()
                result.append((player, score))
                my_k -= 1
        
    return result, count_lines, my_k

        
def get_max_values(files_list):
    max_values = {}
    for file in files_list:
        line = file.readline()
        max_values[file] = int(line.split(",")[1][:-1])
        file.seek(0)

    return max_values


def add_player(playerID, files_list, score, q, file):

    if playerID not in q.ids_dict:
        q.insert(playerID, files_list, score, file)
        return 1
    return 0

def func(max_values, value, file):
    return value/max_values[file]


def set_value(playerID, value, q, file):
    q.change_lb(playerID, value, file)

def calculate_t(q):
    return -q.queue[0]

def calculate_T(all_values):
    return sum(all_values)


def max_upper_bound(all_values, files_list, q):

    max1 = 0
    counts = 0

    for key, value in q.dict.items():
        for elem in value:
            counts+=1
            temp = 0
            c_vals = 0
            for file in files_list:
                if file in elem.extra_files:
                    temp += all_values[c_vals]
                c_vals += 1
            temp += key
            if max1 < temp:
                max1 = temp
    return max1


def check_for_top(upper_bound, q):
    return -q.queue[0] >= upper_bound

def print_results(top_k, count_lines, k, my_k):
    print("Top ", k - my_k, " players:")
    for player in top_k:
        print(player[0].id1, " with score: ", player[1])
    print("Lines read:")
    print(count_lines)

def close_files(files_list):
    for file in files_list:
        file.close()

def main(argv):

    q = PriorityQueue()
    statistics, k = get_input(argv)
    files_list = open_files(statistics)
    top_k, count_lines, my_k = find_top_k(files_list, k, q)
    print_results(top_k, count_lines, k, my_k)
    close_files(files_list)

'''
def dummy_main(argv):

    max_vals = [None, None, None, 1116, 906, 157, 214, 2558]
    dict1 = {}

    if len(argv) != 3:
        print("Error: Wrong number of arguments!")
        print("Arguments: [1,..,5], k")
        exit()

    statistics, _ = [ int(x) for x in argv[1][1:-1].split(",") ], int(argv[2])
    statistics = [ x+2 for x in statistics ]
    f = open("2017_ALL.csv", "r")

    f.readline()

    for line in f:
        result = 0
        tokens = line[:-1].split(",")

        for elem in statistics:
            result += int(tokens[elem])/max_vals[elem]
        dict1[int(tokens[0])] = result

    sorted_dict1 = sorted(dict1.items(), key=operator.itemgetter(1), reverse=True)
    
    print()
    print("TEST CALC")
    for elem in sorted_dict1[]:#insert size of q
        print(elem[0], "with ", elem[1])
    print()

    f.close()
'''

start_time = time()
main(argv)
#dummy_main(argv)
print("total time: %s" %(time() - start_time))
