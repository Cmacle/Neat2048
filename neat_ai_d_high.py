
from __future__ import print_function
from genericpath import isdir
import math
import pickle
import os
import neat
import visualize
import TwentyFortyEight_Deterministic
import statistics

outputs = ["u", "d", "l", "r"]
os.environ["PATH"] += os.pathsep + 'C:/Program Files/Graphviz/bin'
NUM_GAMES = 1
GENERATIONS = 10000
SEEDS = [10, 1322, 3425, 9876, 2345, 1234, 11, 15, 895, 3472, 17, 28, 48, 65]

def eval_genomes(genomes, config):
    for genome_id, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        genome.fitness = play_game(net, config, games=NUM_GAMES)[0]

def play_game(net, config, genome=None, games=1):
    scores = []
    moves = []
    for i in range(games):
        
        game = TwentyFortyEight_Deterministic.TwentyFortyEight(seed=SEEDS[i])
        num_moves = 0
        board = []

        while not game.game_over:
            board = []
            for y in range(len(game.board)):
                for x in range(len(game.board[0])):
                    board.append(int(game.board[y][x]))
                
            num_moves += 1
            output_ = net.activate(board)
            outputs_sorted = [[output_[i],i] for i in range(len(output_))]
            outputs_sorted.sort(key=lambda x: x[0], reverse=True)
            for output in outputs_sorted:
                if game.can_move(outputs[output[1]]):
                    game.move(outputs[output[1]])
                    if genome:
                        tup = (game.board.copy(), outputs[outputs_sorted[0][1]], outputs[output[1]], output_)
                        genome.moves.append(tup)
        scores.append(max(board)-num_moves)
        moves.append(num_moves)
    return float(statistics.mean(scores)), float(statistics.mean(moves)), game.score
    
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

    # Run for up to GENERATIONS generations.
    winner = p.run(eval_genomes, GENERATIONS)
    final_fitness = int(winner.fitness)
    
    #Save the winner to a file
    print("Saving Winner")
    base_path = f'nets/{final_fitness}-Deterministic'
    if not isdir('nets/'):
        os.mkdir('nets/')
    os.mkdir(base_path)
    path = os.path.join(base_path, f'{final_fitness}-Deterministic.pkl')
    
    with open(path, "wb") as f:
        pickle.dump(winner, f)
        pickle.dump(config, f)
    
    # Display the winning genome.
    print('\nBest genome:\n{!s}'.format(winner))

    # Show output of the most fit genome against training data.
    print('\nOutput:')
    winner_net = neat.nn.FeedForwardNetwork.create(winner, config)
    winner.moves=[]
    fitness, num_moves, score = play_game(winner_net, config, genome=winner, games=NUM_GAMES)
    print('\nMoves:')
    for move in winner.moves:
        print(f'First Choice: {move[1]} Taken: {move[2]}')
        print(move[0])
        print(move[3])
    print(f'Score: {score} Num Moves: {num_moves}')

    visualize.draw_net(config, winner, True,
                    filename=os.path.join(base_path, f'net-{int(winner.fitness)}.gv'))
    visualize.plot_stats(stats, ylog=False, view=True,
                    filename=os.path.join(base_path, f'avg_fitness-{int(winner.fitness)}.svg'))
    visualize.plot_species(stats, view=True,
                    filename=os.path.join(base_path, f'speciation-{int(winner.fitness)}.svg'))

    #p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-4')
    #p.run(eval_genomes, 10)


if __name__ == '__main__':
    # Determine path to configuration file. This path manipulation is
    # here so that the script will run successfully regardless of the
    # current working directory.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'neat_config_ff')
    run(config_path)