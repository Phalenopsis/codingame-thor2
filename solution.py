# this solution doesn't pass the 10th test case but pass 100% of the submit tests cases 
import sys
import math

MAX_X = 40
MIN_X = 0
MAX_Y = 18
MIN_Y = 0

class Pos:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __add__(self, other_pos):
        return Pos(self.x + other_pos.x, self.y + other_pos.y)

    def __str__(self):
        return f"({self.x}, {self.y})"
    
    def __repr__(self):
        return f"({self.x}, {self.y})"

    def dist(self, other_pos):
        dist_x = abs(other_pos.x - self.x)
        dist_y = abs(other_pos.y - self.y)
        return math.floor(math.sqrt(dist_x**2 + dist_y**2))
    
    def next_move(self, obj):
        x = self.x
        y = self.y
        if obj.x > self.x :
            x += 1
        if obj.x > self.x :
            x -= 1
        if obj.y > self.y :
            y += 1
        if obj.y > self.y :
            y -= 1
        return Pos(x, y)

def giant_next_move(giant_pos, thor):
    next_giants_pos = []
    for i in giant_pos :
        next_giants_pos.append(i.next_move(thor))
    return  next_giants_pos

MOVES = {   "WAIT" : Pos(0, 0),
            "E" : Pos(1, 0), 
            "SE" : Pos(1, 1),
            "S" : Pos(0, 1), 
            "SW" : Pos(-1, 1), 
            "W" : Pos(-1, 0), 
            "NW" : Pos(-1, -1), 
            "N" : Pos(0, -1), 
            "NE" : Pos(1, -1)         
        }

def barycentre(list_pos):
    x = 0
    y = 0
    for i in list_pos :
        x += i.x
        y += i.y
    x /= len(list_pos)
    y /= len(list_pos)
    return Pos(x, y)

def find_possibilities(giants_pos, thor) :
    """
    >>> return dict where :
    >>> dict[direction] = (pos_possible, nb_giants_near_possibilities)
    >>> 
    """
    possibilities = {}
    nb_giants_near_possibilitie = 0
    for direction, move in MOVES.items() :
        nb_giants_near_possibilitie = 0
        pos_possible = thor + move
        if (pos_possible.x < MIN_X or
            pos_possible.y < MIN_Y or
            pos_possible.x >= MAX_X or
            pos_possible.y >= MAX_Y):
            break
        for i in giants_pos :
            if pos_possible.dist(i) <= 1 :
                nb_giants_near_possibilitie += 1
        if nb_giants_near_possibilitie == 0 :
            possibilities[direction] = (pos_possible, nb_giants_near_possibilitie)
    return possibilities

def thor_next_move(giants_pos, thor) :
    action = ""
    n = len(giants_pos)
    nb_giants_near_thor = 0
    if n > 1 :
        for i in giants_pos :
            if thor.dist(i) <= 1 :
                nb_giants_near_thor += 1
    else :
        for i in giants_pos :
            if thor.dist(i) <= 3 :
                nb_giants_near_thor += 1
    
    if nb_giants_near_thor == n :
        action = "STRIKE"
    elif nb_giants_near_thor > 0 :
        possibilities= find_possibilities(giants_pos, thor)

        if possibilities == {}:
            action = "STRIKE"
            
        else :
            sum_square_distance = math.inf
            choice2 = []
            choice1 = []
            for direction, (pos, nb_giant) in possibilities.items() :
                print(direction, file=sys.stderr, flush = True)
                sum_square = 0
                for i in giants_pos :
                    sum_square += pos.dist(i)**2
                if sum_square < sum_square_distance :
                    sum_square_distance = sum_square
                    action = direction              
    return action


tx, ty = [int(i) for i in input().split()]

giants_pos = []

turn = 0
giants_rectangle_max_x = 0
giants_rectangle_min_x = MAX_X
giants_rectangle_max_y = 0
giants_rectangle_min_y = MAX_Y
queueing = 0
min_min_dist = math.inf

# game loop
while True:
    giants_rectangle_max_x = 0
    giants_rectangle_min_x = MAX_X
    giants_rectangle_max_y = 0
    giants_rectangle_min_y = MAX_Y

    thor = Pos(tx, ty)
    action = ""
    # h: the remaining number of hammer strikes.
    # n: the number of giants which are still present on the map.
    h, n = [int(i) for i in input().split()]
    for i in range(n):
        x, y = [int(j) for j in input().split()]
        giants_pos.append((Pos(x, y)))
        if x > giants_rectangle_max_x :
            giants_rectangle_max_x = x
        if x < giants_rectangle_min_x :
            giants_rectangle_min_x = x
        if y > giants_rectangle_max_y :
            giants_rectangle_max_y = y
        if y < giants_rectangle_min_y :
            giants_rectangle_min_y = y
    
    if giants_rectangle_max_x == giants_rectangle_min_x or giants_rectangle_max_y == giants_rectangle_min_y :
        queueing = 1

    print("thor", thor, file=sys.stderr, flush=True)
    giants_dist = []
    dist_pos = []
    for i in giants_pos :
        giants_dist.append(thor.dist(i))
    for i in range(len(giants_pos)) :
        dist_pos.append(giants_pos[i])
        dist_pos.append(giants_dist[i])
    print("giants", *dist_pos, file=sys.stderr, flush=True)


    center_rectangle = barycentre([Pos(giants_rectangle_max_x, giants_rectangle_max_y), Pos(giants_rectangle_min_x,giants_rectangle_min_y)])
    pos_barycentre = center_rectangle
    
    action = thor_next_move(giants_pos, thor)

    if queueing == 1 :
        min_dist = math.inf
        for i in giants_pos :
            if thor.dist(i) < min_dist :
                min_dist = thor.dist(i)
                if min_dist < min_min_dist :
                    min_min_dist = min_dist
        if min_dist > 13:
            if thor.y > 0 :
                action += "S"
                if pos_barycentre.x > thor.x :
                    action += "E"
                elif pos_barycentre.x < thor.x :
                    action += "W"             
        else : pos_barycentre.y = 7

    if action == "" :
        if pos_barycentre.y > thor.y :
            action += "S"
        elif pos_barycentre.y < thor.y :
            action += "N"

        if pos_barycentre.x > thor.x :
            action += "E"
        elif pos_barycentre.x < thor.x :
            action += "W"

    if action == "" : action = "WAIT"

    print(action)
    giants_pos.clear()
    if action != "STRIKE" and "S" in action :
        ty += 1
    if "N" in action :
        ty -= 1
    if action != "WAIT" and "W" in action :
        tx -= 1
    if action != "STRIKE" and "E" in action :
        tx += 1
    turn += 1
