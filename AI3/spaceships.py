# Spaceship Starter File

# NOTE: You can run this file locally to test if your program is working.

# ===============================================================================

# INPUT FORMAT: ship, others

# ship: A list of length 4 consisting of [x, y, status, score], where

#   x, y is your current position

#   status = 1 if your goal is to travel counterclockwise
#   status = -1 if your goal is to travel clockwise
#   status = 0 if you have crashed

#   score = Number of times you have orbited the center in your target direction

# others: A list containing all other players' ships, in a fixed order. Each
#   ship is given in the same format as your ship, i.e. a list of length 4.

# Example input:

# ship: [3, 5, -1, 1.1]
# others: [[4, 4, 1, -1.3], [4, 6, 0, 0.1], [4, 6, 0, -0.3]]

# =============================================================================

# OUTPUT FORMAT: A list of two integers dx, dy satisfying dx^2 + dy^2 = 5.
# Your spaceship will move to the square x + dx, y + dy.

# Invalid outputs will result in the move you previously played being played
# again, with the exception of the first move, where a random move will be
# played instead.

### WARNING: COMMENT OUT YOUR DEBUG/PRINT STATEMENTS BEFORE SUBMITTING !!!
### (this file uses standard IO to communicate with the grader!)

# ===============================================================================

# Write your bot in the spaceship_bot class. Helper functions and standard
# library modules are allowed, and can be written before before/inside these
# classes.

# You can define as many different strategies as you like, but only the class
# currently named "spaceship_bot" will be run officially.


# Example bot that moves in a random direction every round:

import random
import math
import copy


class spaceship_bot:

    def __init__(self):
        # You can define global states (that last between moves) here
        self.moves = [(1, 2), (2, 1), (2, -1), (1, -2),
                      (-1, -2), (-2, -1), (-2, 1), (-1, 2)]
        self.safe_radii_x = 4
        self.safe_radii_y = 4
        self.last_moves = []
        self.counter_clockwise_path = [(-1, 2), (-2, 1), (-2, -1), (-1, -2), (-1, -2), (1, -2), (1, -2), (2, -1), (2, 1), (1, 2), (1, 2), (-1, 2)]
        self.clockwise_path = [(1, -2), (-1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2), (-1, 2), (1, 2), (1, 2), (2, 1), (2, -1), (1, -2)]
        self.repeats = 0
        self.greedy = False
        self.path = []
        self.wait = random.randint(3, 6)

    def move(self, ship, others):
        # print(others)
        # print(f"the ship status is {ship[2]}")
        loc = (ship[0], ship[1])
        if ship[3] > self.wait:
            self.safe_radii_x = 2
            self.safe_radii_y = 2
        if not self.greedy and ship[3] > self.wait and loc == (3, 2):
            self.greedy = True
        if self.greedy:
            if len(self.path) > 0:
                return self.path.pop(0)
            else:
                if ship[2] == 1:
                    for p in self.counter_clockwise_path:
                        self.path.append(p)
                    return self.path.pop(0)
                else:
                    for p in self.clockwise_path:
                        self.path.append(p)
                    return self.path.pop(0)
        # You should write your code that moves every turn here
        bad = []
        sun = []
        for i in range(-2, 3):
            for j in range(-2, 3):
                bad.append((i, j))
                sun.append((i, j))
        for o in others:
            if o[2] == 0:
                bad.append((o[0], o[1]))
                sun.append((o[0], o[1]))
            else:
                distance = math.sqrt(((o[0] - loc[0]) ** 2) + ((o[1] - loc[1]) ** 2))
                if distance < 7:
                    x = o[0]
                    y = o[1]
                    for x2, y2 in ((x + 2, y-1), (x + 2, y+1), (x - 2, y-1), (x - 2, y+1), (x+1, y + 2), (x-1, y + 2), (x+1, y - 2), (x-1, y - 2)):
                        bad.append((x2, y2))

        if len(self.last_moves) >= 2:
            last_last_loc = self.last_moves.pop(0)
            # print(f"{loc} and {last_last_loc}")
            if last_last_loc == loc:
                self.repeats += 1
                if self.repeats > 2:
                    self.repeats = 0
                    out = (-2, -1)
                    i = 0
                    random.shuffle(self.moves)
                    while (loc[0] + out[0], loc[1] + out[1]) in bad:
                        out = self.moves[i]
                        i += 1
                        if i == 8:
                            i = 0
                            out = self.moves[0]
                            while (loc[0] + out[0], loc[1] + out[1]) in sun:
                                out = self.moves[i]
                                i += 1
                            break
                    return out

        self.last_moves.append(loc)
        # print(f"the loc of the ship is {loc}")
        quadrant = 0
        out = random.choice(self.moves)
        if loc[0] < 0:
            if loc[1] < 0:
                quadrant = 3
            else:
                quadrant = 2
        else:
            if loc[1] < 0:
                quadrant = 4
            else:
                quadrant = 1

        # print(bad)
        # print(f"quadrant {quadrant}")
        # print(f"ship status: {ship[2]}")

        if ship[2] == 1:
            if quadrant == 1:
                # print("checking quad 1")
                if loc[1] > self.safe_radii_y:
                    out = (-2, -1)
                    i = 0
                    self.moves.sort(key=lambda x: x[0])
                    self.moves[2], self.moves[3] = self.moves[3], self.moves[2]
                    # print((loc[0] + out[0], loc[1] + out[1]) in bad)
                    while (loc[0] + out[0], loc[1] + out[1]) in bad:
                        # print(f"{(loc[0] + out[0], loc[1] + out[1])} in {bad}")
                        out = self.moves[i]
                        i += 1
                        if i == 8:
                            i = 0
                            out = self.moves[0]
                            while (loc[0] + out[0], loc[1] + out[1]) in sun:
                                out = self.moves[i]
                                i += 1
                            break
                else:
                    out = (-1, 2)
                    i = 0
                    self.moves.sort(key=lambda x: x[1])
                    self.moves.reverse()
                    self.moves[0], self.moves[1] = self.moves[1], self.moves[0]
                    self.moves[2], self.moves[3] = self.moves[3], self.moves[2]
                    # print((loc[0] + out[0], loc[1] + out[1]) in bad)
                    while (loc[0] + out[0], loc[1] + out[1]) in bad:
                        # print(f"{(loc[0] + out[0], loc[1] + out[1])} in {bad}")
                        out = self.moves[i]
                        i += 1
                        if i == 8:
                            i = 0
                            out = self.moves[0]
                            while (loc[0] + out[0], loc[1] + out[1]) in sun:
                                out = self.moves[i]
                                i += 1
                            break
            elif quadrant == 2:
                # print("checking quad 2")
                if loc[0] > -self.safe_radii_x:
                    out = (-2, -1)
                    i = 0
                    self.moves.sort(key=lambda x: x[0])
                    self.moves[0], self.moves[1] = self.moves[1], self.moves[0]
                    self.moves[2], self.moves[3] = self.moves[3], self.moves[2]
                    # print((loc[0] + out[0], loc[1] + out[1]) in bad)
                    while (loc[0] + out[0], loc[1] + out[1]) in bad:
                        # print(f"{(loc[0] + out[0], loc[1] + out[1])} in {bad}")
                        out = self.moves[i]
                        i += 1
                        if i == 8:
                            i = 0
                            out = self.moves[0]
                            while (loc[0] + out[0], loc[1] + out[1]) in sun:
                                out = self.moves[i]
                                i += 1
                            break
                else:
                    out = (1, -2)
                    i = 0
                    self.moves.sort(key=lambda x: x[1])
                    self.moves[0], self.moves[1] = self.moves[1], self.moves[0]
                    self.moves[2], self.moves[3] = self.moves[3], self.moves[2]
                    # print((loc[0] + out[0], loc[1] + out[1]) in bad)
                    while (loc[0] + out[0], loc[1] + out[1]) in bad:
                        # print(f"{(loc[0] + out[0], loc[1] + out[1])} in {bad}")
                        out = self.moves[i]
                        i += 1
                        if i == 8:
                            i = 0
                            out = self.moves[0]
                            while (loc[0] + out[0], loc[1] + out[1]) in sun:
                                out = self.moves[i]
                                i += 1
                            break
            elif quadrant == 3:
                # print("checking quad 3")
                if loc[1] > -self.safe_radii_y:
                    out = (1, -2)
                    i = 0
                    self.moves.sort(key=lambda x: x[1])
                    self.moves[0], self.moves[1] = self.moves[1], self.moves[0]
                    self.moves[2], self.moves[3] = self.moves[3], self.moves[2]
                    # print((loc[0] + out[0], loc[1] + out[1]) in bad)
                    while (loc[0] + out[0], loc[1] + out[1]) in bad:
                        # print(f"{(loc[0] + out[0], loc[1] + out[1])} in {bad}")
                        out = self.moves[i]
                        i += 1
                        if i == 8:
                            i = 0
                            out = self.moves[0]
                            while (loc[0] + out[0], loc[1] + out[1]) in sun:
                                out = self.moves[i]
                                i += 1
                            break
                else:
                    out = (2, 1)
                    i = 0
                    self.moves.sort(key=lambda x: x[0])
                    self.moves.reverse()
                    # print((loc[0] + out[0], loc[1] + out[1]) in bad)
                    while (loc[0] + out[0], loc[1] + out[1]) in bad:
                        # print(f"{(loc[0] + out[0], loc[1] + out[1])} in {bad}")
                        out = self.moves[i]
                        i += 1
                        if i == 8:
                            i = 0
                            out = self.moves[0]
                            while (loc[0] + out[0], loc[1] + out[1]) in sun:
                                out = self.moves[i]
                                i += 1
                            break
            elif quadrant == 4:
                # print("checking quad 4")
                if loc[0] < self.safe_radii_x:
                    out = (2, 1)
                    i = 0
                    self.moves.sort(key=lambda x: x[0])
                    self.moves.reverse()
                    self.moves[0], self.moves[1] = self.moves[1], self.moves[0]
                    self.moves[2], self.moves[3] = self.moves[3], self.moves[2]
                    # print((loc[0] + out[0], loc[1] + out[1]) in bad)
                    while (loc[0] + out[0], loc[1] + out[1]) in bad:
                        # print(f"{(loc[0] + out[0], loc[1] + out[1])} in {bad}")
                        out = self.moves[i]
                        i += 1
                        if i == 8:
                            i = 0
                            out = self.moves[0]
                            while (loc[0] + out[0], loc[1] + out[1]) in sun:
                                out = self.moves[i]
                                i += 1
                            break
                else:
                    out = (-1, 2)
                    i = 0
                    self.moves.sort(key=lambda x: x[1])
                    self.moves.reverse()
                    # print((loc[0] + out[0], loc[1] + out[1]) in bad)
                    while (loc[0] + out[0], loc[1] + out[1]) in bad:
                        # print(f"{(loc[0] + out[0], loc[1] + out[1])} in {bad}")
                        out = self.moves[i]
                        i += 1
                        if i == 8:
                            i = 0
                            out = self.moves[0]
                            while (loc[0] + out[0], loc[1] + out[1]) in sun:
                                out = self.moves[i]
                                i += 1
                            break

        elif ship[2] == -1:
            if quadrant == 1:
                # print("checking quad 1")
                if loc[0] < self.safe_radii_x:
                    out = (2, -1)
                    i = 0
                    self.moves.sort(key=lambda x: x[0])
                    self.moves.reverse()
                    # print((loc[0] + out[0], loc[1] + out[1]) in bad)
                    while (loc[0] + out[0], loc[1] + out[1]) in bad:
                        # print(f"{(loc[0] + out[0], loc[1] + out[1])} in {bad}")
                        out = self.moves[i]
                        i += 1
                        if i == 8:
                            i = 0
                            out = self.moves[0]
                            while (loc[0] + out[0], loc[1] + out[1]) in sun:
                                out = self.moves[i]
                                i += 1
                            break
                else:
                    out = (-1, -2)
                    i = 0
                    self.moves.sort(key=lambda x: x[1])
                    self.moves[0], self.moves[1] = self.moves[1], self.moves[0]
                    self.moves[2], self.moves[3] = self.moves[3], self.moves[2]
                    # print((loc[0] + out[0], loc[1] + out[1]) in bad)
                    while (loc[0] + out[0], loc[1] + out[1]) in bad:
                        # print(f"{(loc[0] + out[0], loc[1] + out[1])} in {bad}")
                        out = self.moves[i]
                        i += 1
                        if i == 8:
                            i = 0
                            out = self.moves[0]
                            while (loc[0] + out[0], loc[1] + out[1]) in sun:
                                out = self.moves[i]
                                i += 1
                            break
            elif quadrant == 2:
                # print("checking quad 2")
                if loc[1] < self.safe_radii_y:
                    out = (1, 2)
                    i = 0
                    self.moves.sort(key=lambda x: x[1])
                    self.moves.reverse()
                    self.moves[0], self.moves[1] = self.moves[1], self.moves[0]
                    self.moves[2], self.moves[3] = self.moves[3], self.moves[2]
                    # print((loc[0] + out[0], loc[1] + out[1]) in bad)
                    while (loc[0] + out[0], loc[1] + out[1]) in bad:
                        # print(f"{(loc[0] + out[0], loc[1] + out[1])} in {bad}")
                        out = self.moves[i]
                        i += 1
                        if i == 8:
                            i = 0
                            out = self.moves[0]
                            while (loc[0] + out[0], loc[1] + out[1]) in sun:
                                out = self.moves[i]
                                i += 1
                            break
                else:
                    out = (2, -1)
                    i = 0
                    self.moves.sort(key=lambda x: x[0])
                    self.moves.reverse()
                    # print((loc[0] + out[0], loc[1] + out[1]) in bad)
                    while (loc[0] + out[0], loc[1] + out[1]) in bad:
                        # print(f"{(loc[0] + out[0], loc[1] + out[1])} in {bad}")
                        out = self.moves[i]
                        i += 1
                        if i == 8:
                            i = 0
                            out = self.moves[0]
                            while (loc[0] + out[0], loc[1] + out[1]) in sun:
                                out = self.moves[i]
                                i += 1
                            break
            elif quadrant == 3:
                # print("checking quad 3")
                if loc[0] > -self.safe_radii_x:
                    out = (-2, 1)
                    i = 0
                    self.moves.sort(key=lambda x: x[0])
                    self.moves[0], self.moves[1] = self.moves[1], self.moves[0]
                    self.moves[2], self.moves[3] = self.moves[3], self.moves[2]
                    # print((loc[0] + out[0], loc[1] + out[1]) in bad)
                    while (loc[0] + out[0], loc[1] + out[1]) in bad:
                        # print(f"{(loc[0] + out[0], loc[1] + out[1])} in {bad}")
                        out = self.moves[i]
                        i += 1
                        if i == 8:
                            i = 0
                            out = self.moves[0]
                            while (loc[0] + out[0], loc[1] + out[1]) in sun:
                                out = self.moves[i]
                                i += 1
                            break
                else:
                    out = (1, 2)
                    i = 0
                    self.moves.sort(key=lambda x: x[1])
                    self.moves.reverse()
                    # print((loc[0] + out[0], loc[1] + out[1]) in bad)
                    while (loc[0] + out[0], loc[1] + out[1]) in bad:
                        # print(f"{(loc[0] + out[0], loc[1] + out[1])} in {bad}")
                        out = self.moves[i]
                        i += 1
                        if i == 8:
                            i = 0
                            out = self.moves[0]
                            while (loc[0] + out[0], loc[1] + out[1]) in sun:
                                out = self.moves[i]
                                i += 1
                            break
            elif quadrant == 4:
                # print("checking quad 4")
                if loc[1] > -self.safe_radii_y:
                    out = (-1, -2)
                    i = 0
                    self.moves.sort(key=lambda x: x[1])
                    # print((loc[0] + out[0], loc[1] + out[1]) in bad)
                    while (loc[0] + out[0], loc[1] + out[1]) in bad:
                        # print(f"{(loc[0] + out[0], loc[1] + out[1])} in {bad}")
                        out = self.moves[i]
                        i += 1
                        if i == 8:
                            i = 0
                            out = self.moves[0]
                            while (loc[0] + out[0], loc[1] + out[1]) in sun:
                                out = self.moves[i]
                                i += 1
                            break
                else:
                    out = (-2, 1)
                    i = 0
                    self.moves.sort(key=lambda x: x[0])
                    self.moves[0], self.moves[1] = self.moves[1], self.moves[0]
                    self.moves[2], self.moves[3] = self.moves[3], self.moves[2]
                    # print((loc[0] + out[0], loc[1] + out[1]) in bad)
                    while (loc[0] + out[0], loc[1] + out[1]) in bad:
                        # print(f"{(loc[0] + out[0], loc[1] + out[1])} in {bad}")
                        out = self.moves[i]
                        i += 1
                        if i == 8:
                            i = 0
                            out = self.moves[0]
                            while (loc[0] + out[0], loc[1] + out[1]) in sun:
                                out = self.moves[i]
                                i += 1
                            break

        # print(out)
        # print(f"loc: {(ship[0] + out[0], ship[1] + out[1])}")
        # if (ship[0] + out[0], ship[1] + out[1]) in bad:
        #     print('oh no theyre gonna die')
        return out

class spaceship_bot_2:

    def __init__(self):
        # You can define global states (that last between moves) here
        self.moves = [(1, 2), (2, 1), (2, -1), (1, -2),
                      (-1, -2), (-2, -1), (-2, 1), (-1, 2)]
        self.safe_radii = 3

    def move(self, ship, others):
        # print(f"the ship status is {ship[2]}")
        if ship[2] == 0:
            return
        # You should write your code that moves every turn here
        loca = [ship[0], ship[1]]
        # print(f"the loc of the ship is {loc}")
        quadrant = 0
        out = random.choice(self.moves)
        if loca[0] < 0:
            if loca[1] < 0:
                quadrant = 3
            else:
                quadrant = 2
        else:
            if loca[1] < 0:
                quadrant = 4
            else:
                quadrant = 1

        if ship[2] == 1:
            if quadrant == 1:
                if loca[1] > self.safe_radii:
                    out = (-2, -1)
                    if loca[0] + out[0] <= self.safe_radii and loca[1] + out[1] <= self.safe_radii:
                        out = (-2, 1)
                else:
                    out = (-1, 2)
                    if loca[0] + out[0] <= self.safe_radii and loca[1] + out[1] <= self.safe_radii:
                        out = (1, 2)
            elif quadrant == 2:
                if loca[0] > -self.safe_radii:
                    out = (-2, -1)
                    if loca[0] + out[0] <= self.safe_radii and loca[1] + out[1] <= self.safe_radii:
                        out = (-2, 1)
                else:
                    out = (1, -2)
                    if loca[0] + out[0] <= self.safe_radii and loca[1] + out[1] <= self.safe_radii:
                        out = (-1, -2)
            elif quadrant == 3:
                if loca[1] > -self.safe_radii:
                    out = (1, -2)
                    if loca[0] + out[0] <= self.safe_radii and loca[1] + out[1] <= self.safe_radii:
                        out = (-1, -2)
                else:
                    out = (2, 1)
                    if loca[0] + out[0] <= self.safe_radii and loca[1] + out[1] <= self.safe_radii:
                        out = (2, -1)
            elif quadrant == 4:
                if loca[0] < self.safe_radii:
                    out = (2, -1)
                    if loca[0] + out[0] <= self.safe_radii and loca[1] + out[1] <= self.safe_radii:
                        out = (2, 1)
                else:
                    out = (-1, 2)
                    if loca[0] + out[0] <= self.safe_radii and loca[1] + out[1] <= self.safe_radii:
                        out = (1, 2)

        elif ship[2] == -1:
            if quadrant == 1:
                if loca[0] < self.safe_radii:
                    out = (2, -1)
                    if loca[0] + out[0] <= self.safe_radii and loca[1] + out[1] <= self.safe_radii:
                        out = (2, 1)
                else:
                    out = (-1, -2)
                    if loca[0] + out[0] <= self.safe_radii and loca[1] + out[1] <= self.safe_radii:
                        out = (1, -2)
            elif quadrant == 2:
                if loca[1] < -self.safe_radii:
                    out = (1, 2)
                    if loca[0] + out[0] <= self.safe_radii and loca[1] + out[1] <= self.safe_radii:
                        out = (-1, 2)
                else:
                    out = (2, -1)
                    if loca[0] + out[0] <= self.safe_radii and loca[1] + out[1] <= self.safe_radii:
                        out = (2, 1)
            elif quadrant == 3:
                if loca[0] > -self.safe_radii:
                    out = (-2, 1)
                    if loca[0] + out[0] <= self.safe_radii and loca[1] + out[1] <= self.safe_radii:
                        out = (-2, 1)
                else:
                    out = (1, 2)
                    if loca[0] + out[0] <= self.safe_radii and loca[1] + out[1] <= self.safe_radii:
                        out = (-1, 2)
            elif quadrant == 4:
                if loca[1] > -self.safe_radii:
                    out = (-1, -2)
                    if loca[0] + out[0] <= self.safe_radii and loca[1] + out[1] <= self.safe_radii:
                        out = (1, -2)
                else:
                    out = (-2, 1)
                    if loca[0] + out[0] <= self.safe_radii and loca[1] + out[1] <= self.safe_radii:
                        out = (-2, -1)


        # print(out)
        return out



# =============================================================================

# Local testing parameters

# If you would like to view a turn by turn game display while testing locally,
# set this parameter to True

LOCAL_VIEW = True

# Set the size of the area (around the origin) you would like to display, as a
# square of side length 2 * SIDE + 1
# The first ship will be displayed as "1", other ships will be displayed as "0",
# crashed ships will be displayed as "X", and the sun will be displayed as "S".

SIDE = 10

# Set a list of (arbitrarily many) strategies you would like to test locally

LOCAL_STRATS = [
    spaceship_bot()
    # spaceship_bot(),
    # spaceship_bot(),
    # spaceship_bot(),
    # spaceship_bot()
]

# Set how many rounds you would like the game to run for (official is 500)

ROUNDS = 500

# =============================================================================


# You don't need to change any code below this point

import json
import sys
import random
import math
import copy


def WAIT():
    return json.loads(input())


def SEND(data):
    print(json.dumps(data), flush=True)


def dispboard_for_tester(board):
    print()
    print('\n'.join(' '.join(i) for i in board))
    print()


MASK = lambda a, i: a[:i] + a[i + 1:]
LEGAL = [(1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2)]
SIDES = 2 * SIDE + 1


def PLAY(playerlist):
    n = len(playerlist)
    players = [(playerlist[i], i) for i in range(n)]
    random.shuffle(players)
    r = max(8, n)
    ships = [[0] * 4 for i in range(n)]
    moves = [random.choice(LEGAL) for i in range(n)]
    history = []
    off = 2 * math.pi * random.random() / n
    for i in range(n):
        theta = i * 2 * math.pi / n + off
        x, y = int(r * math.sin(theta)), int(r * math.cos(theta))
        if (x + y) % 2:
            if random.choice((0, 1)):
                x += random.choice((-1, 1))
            else:
                y += random.choice((-1, 1))
        ships[i][0] = x
        ships[i][1] = y
        ships[i][2] = 2 * (i % 2) - 1
    board = [[' '] * SIDES for i in range(SIDES)]
    for i in range(SIDE - 2, SIDE + 3):
        for j in range(SIDE - 2, SIDE + 3):
            board[i][j] = 'S'
    for _ in range(ROUNDS):
        chips = copy.deepcopy(ships)
        history.append(chips)
        for i in range(SIDES):
            for j in range(SIDES):
                if board[i][j] in '01':
                    board[i][j] = '.'
        for i in range(n):
            if ships[i][2]:
                player = players[i][0]
                try:
                    move = player.move(chips[i], MASK(chips, i))
                    if move not in LEGAL:
                        raise Exception("invalid move")
                    moves[i] = move
                except Exception as e:
                    print(f"Player {players[i][1]} has an error: {e}! Defaulting to previous move.")
                    print(e)
                oldx, oldy = ships[i][0], ships[i][1]
                ships[i][0] += moves[i][0]
                ships[i][1] += moves[i][1]
                newx, newy = ships[i][0], ships[i][1]
                if -2 <= newx <= 2 and -2 <= newy <= 2:
                    ships[i][2] = 0
                else:
                    delta = math.atan2(newy, newx) - math.atan2(oldy, oldx)
                    if delta < -math.pi:
                        delta += 2 * math.pi
                    elif delta > math.pi:
                        delta -= 2 * math.pi
                    delta *= ships[i][2]
                    ships[i][3] += delta / (2 * math.pi)
                    if abs(ships[i][0]) <= SIDE and abs(ships[i][1]) <= SIDE:
                        board[SIDE - ships[i][1]][SIDE + ships[i][0]] = '1' if players[i][1] == 0 else '0'
            else:
                if abs(ships[i][0]) <= SIDE and abs(ships[i][1]) <= SIDE:
                    if not (-2 <= ships[i][0] <= 2 and -2 <= ships[i][1] <= 2):
                        board[SIDE - ships[i][1]][SIDE + ships[i][0]] = 'X'
        if LOCAL_VIEW:
            dispboard_for_tester(board)
            input("Enter to continue (change LOCAL_VIEW to toggle this)")
        for i in range(n):
            for j in range(i):
                if ships[i][0] == ships[j][0] and ships[i][1] == ships[j][1]:
                    ships[i][2] = 0
                    ships[j][2] = 0
    scores = sorted((players[i][1], ships[i][3]) for i in range(n))
    final = [x[1] for x in scores]
    print("Final scores:")
    print('\n'.join(map(str, final)))
    if not LOCAL_VIEW:
        print("Change LOCAL_VIEW to True to see a turn by turn replay")


if len(sys.argv) < 2 or sys.argv[1] != 'REAL':
    PLAY(LOCAL_STRATS)
    input()

else:
    player = spaceship_bot()
    while True:
        data = WAIT()
        play = player.move(data["ship"], data["others"])
        SEND(play)