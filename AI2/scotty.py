# Scotty Dog Starter File

# NOTE: You can run this file locally to test if your program is working.

# =============================================================================

# INPUT FORMAT: board

# board: A 15 x 15 2D array, where each element is:
#   0 - an empty square
#   1 - the current position of Scotty
#   2 - a naturally generated barrier
#   3 - a player placed barrier

# Example Input:

# board: See "SAMPLE_BOARD" below.

# =============================================================================

# OUTPUT FORMAT when scotty_bot is called:

# A list of two integers [dx, dy], designating in which
# direction you would like to move. Your output must satisfy

# -1 <= dx, dy <= 1

# and one of the following, where board[y][x] is Scotty's current position:

# max(x + dx, y + dy) >= 15 OR min(x + dx, y + dy) < 0 (move off the board)
# OR
# board[y + dy][x + dx] < 2 (move to an empty square or stay still)

# Invalid outputs will result in Scotty not moving.

# =============================================================================

# OUTPUT FORMAT when trapper_bot is called:

# A list of two integers [x, y], designating where you would
# like to place a barrier. The square must be currently empty, i.e.
# board[y][x] = 0

# Invalid outputs will result in no barrier being placed.

### WARNING: COMMENT OUT YOUR DEBUG/PRINT STATEMENTS BEFORE SUBMITTING !!!
### (this file uses standard IO to communicate with the grader!)

# =============================================================================

# Write your bots in the scotty_bot and trapper_bot classes. Helper functions
# and standard library modules are allowed, and can be written before/inside
# these classes.

# You can define as many different strategies as you like, but only the classes
# currently named "scotty_bot" and "trapper_bot" will be run officially.


# Example Scotty bot that makes a random move:

import random
import collections


class scotty_bot:

    def __init__(self):
        # You can define global states (that last between moves) here
        pass

    def find_scotty(self, board):
        # Helper function that finds Scotty's location on the board
        for y in range(15):
            for x in range(15):
                if board[y][x] == 1:
                    return (x, y)

    def move(self, board):
        # You should write your code that moves every turn here q
        moves = [(-1, -1), (-1, 0), (-1, 1), (0, 1),
                 (1, 1), (1, 0), (1, -1), (0, -1)]
        b = board.copy()
        b.reverse()
        loc = self.find_scotty(b)
        if loc[0] == 14:
            return (1, 0)
        elif loc[0] == 0:
            return (-1, 0)
        elif loc[1] == 14:
            return (0, -1)
        elif loc[1] == 0:
            return (0, 1)
        # print("-----scotty-----")
        # print("loc = " + str(loc))
        move = self.bfs(b, loc)
        # print("-----------")
        return (move[0], move[1])

    def bfs(self, grid, start):
        best_path = []
        path_len = 1000
        path_dist = 1000
        to_go = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0), (9, 0), (10, 0), (11, 0),
                 (12, 0), (13, 0), (14, 0), (0, 1), (14, 1), (0, 2), (14, 2), (0, 3), (14, 3), (0, 4), (14, 4), (0, 5),
                 (14, 5), (0, 6), (14, 6), (0, 7), (14, 7), (0, 8), (14, 8), (0, 9), (14, 9), (0, 10), (14, 10),
                 (0, 11), (14, 11), (0, 12), (14, 12), (0, 13), (14, 13), (0, 14), (1, 14), (2, 14), (3, 14), (4, 14),
                 (5, 14), (6, 14), (7, 14), (8, 14), (9, 14), (10, 14), (11, 14), (12, 14), (13, 14), (14, 14)]
        for goal in to_go:
            distance_new = ((start[0] - goal[1]) ** 2) + ((start[1] - goal[0]) ** 2)
            if distance_new < 100:
                if grid[goal[0]][goal[1]] == 0:
                    queue = collections.deque([[start]])
                    seen = [[False] * 15 for _ in range(15)]
                    seen[start[0]][start[1]] = True
                    while queue:
                        path = queue.popleft()
                        x, y = path[-1]
                        if (y, x) == goal:
                            if len(path) < path_len:
                                best_path = path.copy()
                                path_len = len(path)
                                path_dist = distance_new
                            elif len(path) == path_len and distance_new > path_dist:
                                best_path = path.copy()
                                path_len = len(path)
                                path_dist = distance_new
                            break
                        for x2, y2 in ((x - 1, y - 1), (x - 1, y), (x - 1, y + 1), (x, y + 1),
                                       (x + 1, y + 1), (x + 1, y), (x + 1, y - 1), (x, y - 1)):
                            if 0 <= x2 < 15 and 0 <= y2 < 15 and grid[y2][x2] == 0 and not seen[x2][y2]:
                                queue.append(path + [(x2, y2)])
                                seen[x2][y2] = True
        moves = []
        for i in range(len(best_path) - 1):
            cur = best_path[i]
            next = best_path[i + 1]
            xDif = cur[0] - next[0]
            yDif = cur[1] - next[1]
            moves.append((-1 * xDif, yDif))

        if len(moves) > 0:
            # print("move = " + str(moves[0]))
            return moves[0]

        if len(moves) > 0:
            return moves[0]
        return (1, 1)


# Example trapper bot that places a barrier randomly:

class trapper_bot:

    def __init__(self):
        # You can define global states (that last between moves) here
        self.open_points = []
        self.closed = False
        self.pop_locs = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0), (9, 0), (10, 0), (11, 0),
                 (12, 0), (13, 0), (14, 0), (0, 1), (14, 1), (0, 2), (14, 2), (0, 3), (14, 3), (0, 4), (14, 4), (0, 5),
                 (14, 5), (0, 6), (14, 6), (0, 7), (14, 7), (0, 8), (14, 8), (0, 9), (14, 9), (0, 10), (14, 10),
                 (0, 11), (14, 11), (0, 12), (14, 12), (0, 13), (14, 13), (0, 14), (1, 14), (2, 14), (3, 14), (4, 14),
                 (5, 14), (6, 14), (7, 14), (8, 14), (9, 14), (10, 14), (11, 14), (12, 14), (13, 14), (14, 14)]
        self.first = True
        self.to_go = [[(0, 0), 0], [(1, 0), 0], [(2, 0), 0], [(3, 0), 0], [(4, 0), 0], [(5, 0), 0], [(6, 0), 0], [(7, 0), 0], [(8, 0), 0], [(9, 0), 0], [(10, 0), 0], [(11, 0), 0], [(12, 0), 0], [(13, 0), 0], [(14, 0), 0], [(0, 1), 0], [(14, 1), 0], [(0, 2), 0], [(14, 2), 0], [(0, 3), 0], [(14, 3), 0], [(0, 4), 0], [(14, 4), 0], [(0, 5), 0], [(14, 5), 0], [(0, 6), 0], [(14, 6), 0], [(0, 7), 0], [(14, 7), 0], [(0, 8), 0], [(14, 8), 0], [(0, 9), 0], [(14, 9), 0], [(0, 10), 0], [(14, 10), 0], [(0, 11), 0], [(14, 11), 0], [(0, 12), 0], [(14, 12), 0], [(0, 13), 0], [(14, 13), 0], [(0, 14), 0], [(1, 14), 0], [(2, 14), 0], [(3, 14), 0], [(4, 14), 0], [(5, 14), 0], [(6, 14), 0], [(7, 14), 0], [(8, 14), 0], [(9, 14), 0], [(10, 14), 0], [(11, 14), 0], [(12, 14), 0], [(13, 14), 0], [(14, 14), 0]]
        pass

    def find_scotty(self, board):
        # Helper function that finds Scotty's location on the board
        for y in range(15):
            for x in range(15):
                if board[y][x] == 1:
                    return (x, y)

    def move(self, board):
        # You should write your code that moves every turn here
        b = board.copy()
        b.reverse()
        loc = self.find_scotty(b)
        if loc == (7, 7) and not self.first and len(self.pop_locs) > 0:
            return self.pop_locs.pop(0)
        if self.closed:
            out = random.choice(self.open_points)
            while out == loc:
                out = random.choice(self.open_points)
            self.open_points.remove(out)
            if len(self.open_points) == 0:
                self.closed = False
            return out

        # print("-----trapper-----")
        # print("loc = " + str(loc))
        move = self.bfs(b, loc)
        # print("-----------")
        if self.first:
            self.first = False
        return (move[0], 14 - move[1])

    def bfs(self, grid, start):
        best_path = []
        path_len = 1000

        for goal in range(len(self.to_go)):
            distance = ((start[0] - self.to_go[goal][0][1]) ** 2) + ((start[1] - self.to_go[goal][0][0]) ** 2)
            self.to_go[goal][1] = distance
        self.to_go.sort(key=lambda x: x[1])

        for g in self.to_go:
            goal = g[0]
            if grid[goal[0]][goal[1]] == 0:
                queue = collections.deque([[start]])
                seen = [[False] * 15 for _ in range(15)]
                seen[start[0]][start[1]] = True
                while queue:
                    path = queue.popleft()
                    x, y = path[-1]
                    if (y, x) == goal:
                        if len(path) < path_len:
                            best_path = path.copy()
                            path_len = len(path)
                        elif len(path) == path_len:
                            best_path = path.copy()
                            path_len = len(path)
                        break
                    for x2, y2 in ((x - 1, y - 1), (x - 1, y), (x - 1, y + 1), (x, y + 1),
                                   (x + 1, y + 1), (x + 1, y), (x + 1, y - 1), (x, y - 1)):
                        if 0 <= x2 < 15 and 0 <= y2 < 15 and grid[y2][x2] == 0 and not seen[x2][y2]:
                            queue.append(path + [(x2, y2)])
                            seen[x2][y2] = True
            if len(best_path) > 0:
                break

        if len(best_path) == 0:
            self.closed = True
            for i in range(0, 15):
                for j in range(14, -1, -1):
                    if grid[j][i] == 0 or grid[j][i] == 1:
                        self.open_points.append((i, 14 - j))
            # queue = collections.deque([[start]])
            # seen = [[False] * 15 for _ in range(15)]
            # seen[start[0]][start[1]] = True
            # while queue:
            #     path = queue.popleft()
            #     backup_path = path.copy()
            #     if len(path) > 5:
            #         break
            #     x, y = path[-1]
            #     for x2, y2 in ((x - 1, y - 1), (x - 1, y), (x - 1, y + 1), (x, y + 1),
            #                    (x + 1, y + 1), (x + 1, y), (x + 1, y - 1), (x, y - 1)):
            #         self.i += 5
            #         if 0 <= x2 < 15 and 0 <= y2 < 15 and grid[y2][x2] == 0 and not seen[x2][y2]:
            #             queue.append(path + [(x2, y2)])
            #             seen[x2][y2] = True

        if len(best_path) > 0:
            # print("scotty is at " + str(start))
            # print("move = " + str(best_path))
            # print(path_dist)
            return best_path[-1]
        return [-1, -1]


# =============================================================================

# Local testing parameters

# If you would like to view a turn by turn game display while testing locally,
# set this parameter to True

LOCAL_VIEW = True

# Sample board your game will be run on (flipped vertically)
# This file will display 0 as ' ', 1 as '*', 2 as 'X', and 3 as 'O'

SAMPLE_BOARD = [
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0],
    [2, 0, 0, 0, 2, 0, 2, 0, 2, 2, 0, 0, 2, 2, 2],
    [2, 0, 2, 0, 2, 2, 0, 0, 0, 0, 0, 2, 0, 0, 0],
    [2, 2, 0, 0, 2, 0, 2, 2, 0, 0, 2, 0, 2, 0, 2],
    [2, 0, 2, 2, 0, 0, 2, 0, 0, 0, 2, 0, 2, 0, 2],
    [2, 2, 0, 2, 0, 2, 0, 2, 0, 0, 2, 0, 0, 0, 0],
    [2, 0, 0, 2, 2, 0, 2, 0, 2, 2, 2, 0, 2, 0, 0],
    [2, 2, 0, 2, 2, 2, 0, 1, 0, 2, 2, 0, 0, 2, 0],
    [2, 2, 0, 2, 2, 2, 0, 0, 0, 2, 0, 2, 2, 2, 0],
    [0, 0, 0, 0, 2, 0, 2, 2, 0, 2, 0, 2, 2, 0, 0],
    [2, 2, 0, 0, 0, 0, 0, 0, 2, 2, 0, 2, 2, 0, 2],
    [2, 2, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0],
    [2, 0, 0, 2, 2, 0, 0, 0, 2, 2, 0, 0, 0, 0, 2],
    [2, 0, 0, 0, 0, 0, 2, 0, 2, 0, 0, 0, 0, 0, 0],
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0]]

for i in range(len(SAMPLE_BOARD)):
    for j in range(len(SAMPLE_BOARD[0])):
        rand = random.randint(1, 10)
        if i == 7 and j == 7:
            SAMPLE_BOARD[i][j] = 1
        elif rand <= 3:
            SAMPLE_BOARD[i][j] = 2
        else:
            SAMPLE_BOARD[i][j] = 0

# =============================================================================


# You don't need to change any code below this point

import json
import sys


def WAIT():
    return json.loads(input())


def SEND(data):
    print(json.dumps(data), flush=True)


def dispboard_for_tester(board):
    print()
    print('\n'.join(''.join(map(lambda x: ' *XO'[x], i)) for i in reversed(board)))
    print()


def find_scotty_for_tester(board):
    for y in range(15):
        for x in range(15):
            if board[y][x] == 1:
                return (x, y)


def trapped_for_tester(board):
    pos = find_scotty_for_tester(board)
    moves = [*zip([0, 1, 1, 1, 0, -1, -1, -1], [1, 1, 0, -1, -1, -1, 0, 1])]
    trap = True
    for i in moves:
        if 0 <= pos[0] + i[0] < 15 and 0 <= pos[1] + i[1] < 15:
            if board[pos[1] + i[1]][pos[0] + i[0]] == 0:
                trap = False
                break
        else:
            trap = False
            break
    return trap


def PLAY(scotty, trapper, board):
    result = -1
    while True:
        try:
            val = trapper.move(board)
            if not (val[0] == int(val[0]) and 0 <= val[0] < 15
                    and val[1] == int(val[1]) and 0 <= val[1] < 15
                    and board[val[1]][val[0]] == 0):
                raise Exception('invalid move')
            board[val[1]][val[0]] = 3
        except Exception as e:
            print(f'Your trapper has an error: {e}! Doing nothing instead.')
            val = -1
        if trapped_for_tester(board):
            result = 1
            break
        if LOCAL_VIEW:
            dispboard_for_tester(board)
            input("Enter to continue (change LOCAL_VIEW to toggle this)")
        try:
            val = scotty.move(board)
            if not (val[0] == int(val[0]) and -1 <= val[0] <= 1
                    and val[1] == int(val[1]) and -1 <= val[1] <= 1):
                raise Exception('invalid move')
        except Exception as e:
            print(f'Your Scotty has an error: {e}! Doing nothing instead.')
            val = (0, 0)
        pos = find_scotty_for_tester(board)
        if 0 <= pos[0] + val[0] < 15 and 0 <= pos[1] + val[1] < 15:
            if board[pos[1] + val[1]][pos[0] + val[0]] == 0:
                board[pos[1] + val[1]][pos[0] + val[0]] = 1
                board[pos[1]][pos[0]] = 0
        else:
            board[pos[1]][pos[0]] = 0
            result = 0
            break
        if LOCAL_VIEW:
            dispboard_for_tester(board)
            input("Enter to continue (change LOCAL_VIEW to toggle this)")
    print(["Scotty", "Trapper"][result], "won!")
    if not LOCAL_VIEW:
        print("Change LOCAL_VIEW to True to see a turn by turn replay")

if len(sys.argv) < 2 or sys.argv[1] != 'REAL':
    PLAY(scotty_bot(), trapper_bot(), SAMPLE_BOARD)
    input()

else:
    scotty = scotty_bot()
    trapper = trapper_bot()
    while True:
        data = WAIT()
        board = data["board"]
        role = data["role"]
        if role == "trapper":
            SEND(trapper.move(board))
        else:
            SEND(scotty.move(board))