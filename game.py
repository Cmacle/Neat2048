import numpy as np

class TwentyFortyEight():
    score = 0
    game_over = False
    
    def __init__(self, width=4, height=4):
        self.width = width
        self.height = height
        self.board = np.zeros(shape=(height,width), dtype=np.uint16)
        self.add_num()
        self.add_num()
        
    def __str__(self):
        string = ""
        for y in range(self.height):
            string += "\n" + "|"
            for x in range(self.width):
                string += str(self.board[y][x]).center(8) + "|"
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
            self.board[y][x] = np.random.randint(low=1,high=3)*2
            return (y,x)
    
    def move(self, direction):
        # Move in a direction
        if direction == "Up" or direction == "u":
            self._move_up
        elif direction == "Down" or direction == "d":
            self._move_down
        elif direction == "Left" or direction == "":
            self._move_left
        elif direction == "Right" or direction == "r":
            self._move_up
    
    def _move_up(self):
        pass
    
    def _move_down(self):
        pass
    
    def _move_left(self):
        pass
    
    def _move_right(self):
        pass
    
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
        avaiable_moves = 0
        return avaiable_moves


if __name__ == '__main__':
    game = TwentyFortyEight()
    print(game)
    print(f'Up: {game.can_move("u")}')
    print(f'Down: {game.can_move("d")}')
    print(f'Left: {game.can_move("l")}')
    print(f'Right: {game.can_move("r")}')