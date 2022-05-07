import numpy as np




class TwentyFortyEight():
    score = 0
    game_over = False
    
    def __init__(self, width=4, height=4, seed=10):
        self.width = width
        self.height = height
        self.board = np.zeros(shape=(height,width), dtype=np.uint16)
        np.random.seed(seed)
        self.add_num()
        self.add_num()
        
    def __str__(self):
        string = ""
        for y in range(self.height):
            string += "\n\n" + "|"
            for x in range(self.width):
                if self.board[y][x]:
                    string += str(self.board[y][x]).center(8) + "|"
                else:
                    string += "        " + "|"
        return string
    
    def add_num(self):
        # Generate a new number in an empty space
        # with value 2 or 4
        empty_spaces = self.empty_spaces
        if not empty_spaces:
            self.game_over = True
            return "GAME OVER"
        else:
            loc = np.random.randint(len(empty_spaces))
            y = empty_spaces[loc][0]
            x = empty_spaces[loc][1]
            self.board[y][x] = np.random.randint(low=1, high=3)*2
            return (y,x)
    
    def move(self, direction):
        # Move in a direction
        if direction == "Up" or direction == "u":
            if self.can_move('u'):
                self._move_up()
                self.add_num()
        elif direction == "Down" or direction == "d":
            if self.can_move('d'):
                self._move_down()
                self.add_num()
        elif direction == "Left" or direction == "l":
            if self.can_move('l'):
                self._move_left()
                self.add_num()
        elif direction == "Right" or direction == "r":
            if self.can_move('r'):
                self._move_right()
                self.add_num()
        # Check for game over
        if not self.available_moves:
            self.game_over=True
    
    def _move_up(self):
        for y in range(1,self.height):
            for x in range(self.width):
                if self.board[y][x]:
                    holdy = y
                    at_zero = False
                    while True:

                        if self.board[holdy-1][x] == 0:
                            self.board[holdy-1][x] = self.board[holdy][x]
                            self.board[holdy][x] = 0
                            holdy-=1
                        else:
                            break
                        if holdy < 1:
                            at_zero = True
                            break
                    if not at_zero:
                        if self.board[holdy][x] == self.board[holdy-1][x]:
                            loc1 = (holdy-1,x)
                            loc2 = (holdy,x)
                            self._combine(loc1,loc2)
                else:
                    continue
    
    def _move_down(self):
        for y in range(self.height-2,-1,-1):
            for x in range(self.width):
                if self.board[y][x]:
                    holdy = y
                    at_max = False
                    while True:
                        if self.board[holdy+1][x] == 0:
                            self.board[holdy+1][x] = self.board[holdy][x]
                            self.board[holdy][x] = 0
                            holdy+=1
                        else:
                            break
                        if holdy >= self.height-1:
                            at_max = True
                            break
                    if not at_max:
                        if self.board[holdy][x] == self.board[holdy+1][x]:
                            loc1 = (holdy+1,x)
                            loc2 = (holdy,x)
                            self._combine(loc1,loc2)
                else:
                    continue
                
    def _move_left(self):
        for x in range(1,self.width):
            for y in range(self.height):
                if self.board[y][x]:
                    holdx = x
                    at_zero = False
                    while True:
                        if self.board[y][holdx-1] == 0:
                            self.board[y][holdx-1] = self.board[y][holdx]
                            self.board[y][holdx] = 0
                            holdx-=1
                        else:
                            break
                        if holdx < 1:
                            at_zero = True
                            break
                    if not at_zero:
                        if self.board[y][holdx] == self.board[y][holdx-1]:
                            loc1 = (y,holdx-1)
                            loc2 = (y,holdx)
                            self._combine(loc1,loc2)
                else:
                    continue
    
    def _move_right(self):
        for x in range(self.width-2,-1,-1):
            for y in range(self.height):
                if self.board[y][x]:
                    holdx = x
                    at_max = False
                    while True:
                        if self.board[y][holdx+1] == 0:
                            self.board[y][holdx+1] = self.board[y][holdx]
                            self.board[y][holdx] = 0
                            holdx+=1
                        else:
                            break
                        if holdx >= self.width-1:
                            at_max = True
                            break
                    if not at_max:
                        if self.board[y][holdx] == self.board[y][holdx+1]:
                            loc1 = (y,holdx+1)
                            loc2 = (y,holdx)
                            self._combine(loc1,loc2)
                else:
                    continue
    
    def _combine(self, loc1, loc2):
        # Combine the two locations, increment the score and
        # set loc2 to 0
        self.board[loc1[0]][loc1[1]] *= 2
        self.board[loc2[0]][loc2[1]] = 0
        self.score += self.board[loc1[0]][loc1[1]]
    
    def can_move(self, direction):
        # Check if a move will cause any changes
        if direction == "Up" or direction == "u":
            for y in range(1,self.height):
                for x in range(self.width):
                    if self.board[y][x]:
                        if ((not self.board[y-1][x]) or 
                            self.board[y][x] == self.board[y-1][x]):
                            return True
                    else:
                        continue
            return False
        elif direction == "Down" or direction == "d":
            for y in range(self.height-2,-1,-1):
                for x in range(self.width):
                    if self.board[y][x]:
                        if ((not self.board[y+1][x]) or 
                            self.board[y][x] == self.board[y+1][x]):
                            return True
                    else:
                        continue
            return False
        elif direction == "Left" or direction == "l":
            for x in range(1,self.width):
                for y in range(self.height):
                    if self.board[y][x]:
                        if ((not self.board[y][x-1]) or 
                            self.board[y][x] == self.board[y][x-1]):
                            return True
                    else:
                        continue
            return False
        elif direction == "Right" or direction == "r":
            for x in range(self.width-2,-1,-1):
                for y in range(self.height):
                    if self.board[y][x]:
                        if ((not self.board[y][x+1]) or 
                            self.board[y][x] == self.board[y][x+1]):
                            return True
                    else:
                        continue
            return False
    
    @property
    def empty_spaces(self):
        # Return a list of empty spaces (value = 0)
        empty_spaces = []
        for y in range(self.height):
            for x in range(self.width):
                if not self.board[y][x]:
                    space = (y,x)
                    empty_spaces.append(space)
        return empty_spaces
                     
    @property
    def available_moves(self):
        # Return the number of available moves
        available_moves = 0
        for dir in ('u','d','l','r'):
            if self.can_move(dir):
                available_moves += 1
        return available_moves


if __name__ == '__main__':
    game = TwentyFortyEight()
    while not game.game_over:
        print(game)
        print(f'Score: {game.score}')
        game.move(input())
    print("GAME OVER")