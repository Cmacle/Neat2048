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
        pass
    
    def can_move(self, direction):
        # Check if a move will cause any changes
        pass
    
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