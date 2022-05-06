from os import getcwd
import pickle
import neat
from tkinter import filedialog
import TwentyFortyEight
import tkinter as tk

OUTPUTS = ["u", "d", "l", "r"]

def create_network(netpath):
    with open(netpath, 'rb') as f:
        data = pickle.load(f)
    return neat.nn.RecurrentNetwork.create(data[0], data[1])


def play_game(net, games=1):
    scores = []
    all_moves = []
    for i in range(games):
        moves = []
        score = 0 
        game = TwentyFortyEight.TwentyFortyEight()
        num_moves = 0
        board = []

        while not game.game_over:
            board = []
            for y in range(len(game.board)):
                for x in range(len(game.board[0])):
                    board.append(int(game.board[y][x]))
                
            num_moves += 1
            net_output = net.activate(board)
            outputs_sorted = [[net_output[i],i] for i in range(len(net_output))]
            outputs_sorted.sort(key=lambda x: x[0], reverse=True)
            for output in outputs_sorted:
                if game.can_move(OUTPUTS[output[1]]):
                    game.move(OUTPUTS[output[1]])
                    tup = (str(game), OUTPUTS[outputs_sorted[0][1]], OUTPUTS[output[1]], net_output)
                    moves.append(tup)
                break
        scores.append(game.score)
        all_moves.append(moves)
    return scores, all_moves


if __name__ == '__main__':
    print("Choose the file.")
    root = tk.Tk()
    root.withdraw()
    netpath = filedialog.askopenfilename(filetypes=[('Pickle','.pkl')], initialdir=getcwd())
    net = create_network(netpath)
    games = int(input("How many games to be played?:  "))
    scores, moves = play_game(net, games=games)
    print(f'Max Score = {max(scores)} \nAvg Score = {sum(scores)/len(scores)}')

    for i, game in enumerate(moves):
        print(f'Game: {i}\nScore: {scores[i]}')
        answer = input("Display this game? y if yes").lower()

        if answer == 'y':
            for n, move in enumerate(game):
                print(move[0])
                print(f'Move #{n}')
                print(f'First Move Choice: {move[1]}')
                print(f'Move Taken: {move[2]}')
                print(f'Network Output: {move[3]}')
                input("")
            print(f'FINAL SCORE: {scores[i]} MOVES: {len(game)}')

            


