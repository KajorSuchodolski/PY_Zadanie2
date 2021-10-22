import argparse
import configparser
import logging
import os
from chase.functions import simulation


def main():
    rounds = 50
    init_pos_limit = 10.0
    sheep_move_dist = 0.5
    wolf_move_dist = 1.0
    num_of_sheep = 15
    wait_for_key = False
    absolute_dir = ""

    parser = argparse.ArgumentParser()

    parser.add_argument('-c', '--config', type=str,
                        help='add configuration file')
    parser.add_argument('-d', '--dir', type=str,
                        help='directory to which pos.json, alive.csv and optionally chase.log files shall be saved')
    parser.add_argument('-r', '--rounds', type=int,
                        help='define the number of rounds')
    parser.add_argument('-s', '--sheep', type=int,
                        help='define the number of sheep')
    parser.add_argument('-w', '--wait', action='store_true',
                        help='wait for key press after every round')
    parser.add_argument('-l', '--log', type=int,
                        help='save the events of the chosen type to the log')

    args = parser.parse_args()
    logging.debug("Function parse_args() was called")

    if args.config:
        config_file = configparser.ConfigParser()
        config_file.read(args.config)
        logging.debug("Function read(" + str(args.config) + ") was called on object" + str(config_file))

        if float(config_file.get('Movement', 'WolfMoveDist')) <= 0:
            raise Exception('Wolf cannot be moving at velocity 0 or less')
        if float(config_file.get('Movement', 'SheepMoveDist')) <= 0:
            raise Exception('Sheep cannot be moving at velocity 0 or less')
        if float(config_file.get('Terrain', 'InitPosLimit')) == 0:
            raise Exception('Sheep cannot be placed at 0.0')

        init_pos_limit = float(config_file.get('Terrain', 'InitPosLimit'))
        wolf_move_dist = float(config_file.get('Movement', 'WolfMoveDist'))
        sheep_move_dist = float(config_file.get('Movement', 'SheepMoveDist'))

    if args.dir:
        if not os.path.isdir(args.dir):
            os.mkdir(args.dir)
        directory = args.dir
        absolute_dir = directory + "\\"

    if args.rounds:
        if args.rounds <= 0:
            raise Exception('The number of rounds should be more than 0')

        rounds = args.rounds

    if args.sheep:
        if args.sheep <= 0:
            raise Exception('The number of sheep should be more than 0')

        num_of_sheep = args.sheep

    if args.wait:
        wait_for_key = True

    if args.log:
        if args.log not in (10, 20, 30, 40, 50):
            raise Exception('Wrong argument')
        logging.basicConfig(filename=absolute_dir + 'chase.log', level=args.log,
                            format='%(levelname)s:%(asctime)s:%(name)s:%(message)s', force=True, filemode='w')

    simulation(rounds, init_pos_limit, sheep_move_dist, wolf_move_dist, num_of_sheep, wait_for_key, absolute_dir)
    logging.debug("Function simulation() was called")


if __name__ == "__main__":
    main()
