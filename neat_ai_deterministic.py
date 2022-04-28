"""
2-input XOR example -- this is most likely the simplest possible example.
"""

from __future__ import print_function
import math
import os
import neat
import visualize
import TwentyFortyEight_Deterministic
import statistics

outputs = ["u", "d", "l", "r"]
os.environ["PATH"] += os.pathsep + 'C:/Program Files/Graphviz/bin'
NUM_GAMES = 1
GENERATIONS = 300

def eval_genomes(genomes, config):
    for genome_id, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        genome.fitness = play_game(net, config, games=NUM_GAMES)[0]

def play_game(net, config, genome=None, games=1):
    scores = []
    moves = []
    for i in range(games):
        
        game = TwentyFortyEight_Deterministic.TwentyFortyEight()
        num_moves = 0

        board = []

        while not game.game_over:
            board = []
            for y in range(len(game.board)):
                for x in range(len(game.board[0])):
                    board.append(int(game.board[y][x]))
                
            num_moves += 1
            output = net.activate(board)
            outputs_sorted = [(output[i],i) for i in range(len(output))]
            outputs_sorted.sort()
            for output in outputs_sorted:
                if game.can_move(outputs[output[1]]):
                    game.move(outputs[output[1]])
                    if genome:
                        tup = (game.board.copy(), outputs[outputs_sorted[0][1]], outputs[output[1]])
                        genome.moves.append(tup)
        scores.append(game.score)
        moves.append(num_moves)
    return float(statistics.median(scores)), float(statistics.median(moves))
    
def run(config_file):
    # Load configuration.
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(5))

    # Run for up to 300 generations.
    winner = p.run(eval_genomes, GENERATIONS)

    # Display the winning genome.
    print('\nBest genome:\n{!s}'.format(winner))

    # Show output of the most fit genome against training data.
    print('\nOutput:')
    winner_net = neat.nn.FeedForwardNetwork.create(winner, config)
    winner.moves=[]
    high_score, num_moves = play_game(winner_net, config, genome=winner, games=NUM_GAMES)
    print('\nMoves:')
    for move in winner.moves:
        print(f'First Choice: {move[1]} Taken: {move[2]}')
        print(move[0])
    print(f'Score: {high_score} Num Moves: {num_moves}')

    visualize.draw_net(config, winner, True)
    visualize.plot_stats(stats, ylog=False, view=True)
    visualize.plot_species(stats, view=True)

    p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-4')
    p.run(eval_genomes, 10)


if __name__ == '__main__':
    # Determine path to configuration file. This path manipulation is
    # here so that the script will run successfully regardless of the
    # current working directory.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'neat_config')
    run(config_path)