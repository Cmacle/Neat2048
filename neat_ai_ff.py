
from __future__ import print_function
from genericpath import isdir
import math
import pickle
import os
import neat
import visualize
import TwentyFortyEight_Deterministic
import statistics

OUTPUTS = ["u", "d", "l", "r"]
os.environ["PATH"] += os.pathsep + 'C:/Program Files/Graphviz/bin'
NUM_GAMES = 25
GENERATIONS = 10000
# 'score' for highest game score, 'max' for highest tile - num moves
SCORING_METHOD = 'score'

def eval_genomes(genomes, config, scoring_method=SCORING_METHOD):
    for genome_id, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        genome.fitness = play_game(net, config, games=NUM_GAMES, scoring_method=scoring_method)[0]

def play_game(net, config, genome=None, games=1, scoring_method="score"):
    scores = []
    moves = []
    for i in range(games):
        
        game = TwentyFortyEight_Deterministic.TwentyFortyEight(seed=i)
        num_moves = 0
        board = []

        while not game.game_over:
            board = game.board.flatten()
            #for y in range(len(game.board)):
            #    for x in range(len(game.board[0])):
            #        board.append(int(game.board[y][x]))
                
            num_moves += 1
            net_output = net.activate(board)
            outputs_sorted = [[net_output[i],i] for i in range(len(net_output))]
            outputs_sorted.sort(key=lambda x: x[0], reverse=True)
            for output in outputs_sorted:
                if game.can_move(OUTPUTS[output[1]]):
                    game.move(OUTPUTS[output[1]])
                    if genome:
                        tup = (game.board.copy(), OUTPUTS[outputs_sorted[0][1]], OUTPUTS[output[1]], net_output)
                        genome.moves.append(tup)
                    break
        if scoring_method == 'max':
            scores.append(max(board) - num_moves)
        else:
            scores.append(game.score - num_moves)
        moves.append(num_moves)
    return float(min(scores)), float(statistics.mean(moves)), game.score
    
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
    base_path = f'nets/{final_fitness}-{SCORING_METHOD.upper()}-LOWEST-FF'
    if not isdir('nets/'):
        os.mkdir('nets/')
    os.mkdir(base_path)
    path = os.path.join(base_path, f'{final_fitness}-FF.pkl')
    
    with open(path, "wb") as f:
        data = (winner,config)
        pickle.dump(data, f)
    
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