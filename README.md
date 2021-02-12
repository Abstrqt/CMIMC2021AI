# CCA5: CMIMC AI Round

Source code available at [Abstrqt/CMIMC2021AI](https://github.com/Abstrqt/CMIMC2021AI)

Overview:

- Bet: Matches dealer card in the first round. Keeps a log of the threshold to win/tie a card, then adapt in the following rounds assuming that opponents make the same move pattern (dealer card + x).
- Scotty: Scotty would go for corners and the trapper would start by going for the middle edges on an empty board. 
- Spaceships: Greedy algorithm where we would play somewhat safe orbiting the sun but assume that other players would avoid possible collisions. 

## Bet: 

### Introduction

This is a 3-player game. Initially, each of the 3 players holds 13 bidding cards worth 2 through 14 (i.e. a suit of cards with ace-high). There is also a face-down pile that contains 13 shuffled cards with point values from 2 to 14.

On each turn, one card from the face-down pile is revealed. All three players simultaneously bid on the revealed card by using one of their remaining bidding cards. If there is a unique highest bidder, that player receives points equal to the value of the card. If there is a tie for first, no player receives points. This repeats 13 times until all cards are used.

### Scoring

In each game, you will receive 5 points for coming 1st, 2 points for 2nd, and 1 point for 3rd. If there are ties, all tied players will be treated as having the lower scoring rank, i.e. if 1st and 2nd tie, both will be treated as 2nd. Additionally, 1% of the numerical sum of the cards you won during the game will be added to your score. For example, if you came 1st in a game with a total of 49 points won from bids, you would receive 5.49 points for that game.

In each match, your bot will play against the same 2 opponents for a total of 5 games, and your match score will be the average over these 5 games. You are allowed (and encouraged) to store any information you want about previous games in the match.

### Strategy

At first, we started with the simple strategy of just playing the same value of the card to bid on, so if the dealer plays a 3, we would just return the card. 

```python
card = 3
return card
```

This worked well, but many other people also did this strategy, so we then changed our strategy to playing the dealer card + 1, and if it was 14, we would just play 1. Later, more people started catching on to this, so we did dealer card + 2 and if it was greater than 14, we would just play the lowest card in the hand. 

```python
return hand[lowest] if card >= 14 else card+2
```

Then we realized that we could just detect what strategy the other players were using (if they were using a simple one like this) and counter it, so if we were P1 and P2 played dealer card + 1 and P3 played dealer card + 3, we would play dealer card + 4, which would win most of the time. The bot would track this for three rounds to detect that a predictable pattern was being played by our opponents. If the bot did not detect any of these strategies, we would just play the same value as the dealer card. Many people did not use the simple strategy of dealer card + _, but our code still worked pretty well, as playing the same value as the dealer card is a pretty strong strategy.

### Results

Third place overall out of 235 teams with a rating of 51.58. 

## Trap the Scotty Dog:

### Introduction

This is a 2-player asymmetric game. The two players are Scotty and the Trapper.

Initially, Scotty is at the center cell of a  grid, called the game board. On each turn, the Trapper can place a barrier on any empty cell of the board, then Scotty can either move to one of the 8 cells adjacent to it's current cell (like a chess king), or stay in it's current cell. Scotty's goal is to move off the edge of the board, while the Trapper's goal is to stop this from happenning.

The game ends when Scotty moves off the board (and Scotty wins), or Scotty is unable to make any legal move besides staying still (and the Trapper wins). If no player has won after 200 moves, the game is considered a draw.

To help out the Trapper, some cells will start with barriers. In particular, the board will be randomly initialized with barriers in 20-40% of its cells. It is guaranteed that the center cell never contains a barrier, and Scotty will always have a path to escape.

### Scoring

In each game, the winner receives 1 point and the loser receives 0 points. In the case of a draw, both players receive 0.5 points.

### Strategy

For Scotty, our strategy for escaping was to sort all edges by euclidean distance and use BFS to pathfind to the edges that were the furthest euclidean distance way while still equal to the shortest number of moves. 

```python
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
```


For trapping, it was pretty similar to escaping, but instead, we placed a barrier at the edge that had the least euclidean distance while still tied for shortest number of moves. Once all the edges were blocked, the bot would just randomly place traps until Scotty was trapped. This was done so that the trapper did not run out of time. 

```python
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
```

### Results

Second place overall out of 235 teams with a rating of 61.39. 

## Spaceships: 

### Introduction

This is an n-player game. Each player controls a spaceship that starts at some integer coordinates (x,y). On each turn, all spaceships move simultaneously to a new position. Spaceships move in the same L-shaped pattern of a chess knight, so there are 8 possible moves to choose from.

If two or more spaceships move to the same position at the same turn, they will crash. This is bad for all spaceships involved, and should be avoided at all costs. Additionally, the sun occupies a 5x5 square of cells centered at (0,0), and any spaceships moving into this region will also crash.

Each player is given a direction to move their spaceship: either clockwise or counterclockwise. The goal is to make the maximum number of orbits around the sun, in the given direction.

The starting positions (x,y) are such that x + y (mod 2) is the same for all players. Moreover, (x,y) is chosen to be a distance of approximately n away from the sun, i.e x^2 + y^2 ≈ n^2, where n is the number of players.

The game will last for 500 turns, but any crashed spaceships will immediately stop moving.

### Scoring

At the end of the game, your score will be calculated as your winding number - the total number of times your spaceship has orbited around the origin. If you are going in the wrong direction (e.g. moving counterclockwise when you are supposed to move clockwise), your score will be 0 (despite the starter file's local tester showing a negative winding number)

### Strategy

Our strategy was a greedy algorithm that had our spaceship orbit close to the sun and assumed that other players had a collision detection algorithm. This, in theory, allowed us to basically "play chicken" and go where other bots would avoid, allowing us to have a shorter orbit distance around the sun. In retrospect, this wasn't that good because many other bots didn't really have a detection algorithm and our ship would suffer numerous collisions, which hurt our performance. 

### Results

10th place overall out of 235 teams with a rating of 67.37.

## Final Thoughts

Overall, our team ended up with 5th in the AI round and 10th place overall on the combined leaderboard! It was an amazing and fun two weeks full of ups and downs for both the organizers and the competitors. Thank you to CMIMC for hosting and we are definitely looking forward to competing again next year!
