import random
import json
import csv
import argparse
import configparser
import logging
import os
from Sheep import Sheep
from Wolf import Wolf

# Liczba tur: 50;
# Liczba owiec: 15;
# init_pos_limit: 10.0;
# sheep_move_dist: 0.5;
# wolf_move_dist: 1.0.


rounds = 50
init_pos_limit = 10.0
sheep_move_dist = 0.5
wolf_move_dist = 1.0
num_of_sheep = 15
wait_for_key = False
directory = None
path = ""

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
print(args.config)

if args.config:
    config_file = configparser.ConfigParser()
    config_file.read(args.config)

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

    logging.basicConfig(filename=path + 'chase.log', level=args.log,
                        format='%(asctime)s:%(name)s:%(message)s')


def save_to_json(data, path):
    with open(path + 'pos.json', 'w') as f_json:
        json.dump(data, f_json, indent=2)


def random_direction():
    return random.randint(0, 3)


def random_position():
    return random.uniform(-init_pos_limit, init_pos_limit)


def simulation():
    global path
    if directory is not None:
        path = directory + "\\"
        if not os.path.isdir(directory):
            os.mkdir(directory)

    rand_x = random_position()
    rand_y = random_position()

    sheep = [Sheep(rand_x, rand_y, i + 1) for i in range(num_of_sheep)]
    logging.debug("Function Sheep(", rand_x, rand_y, "i + 1 was called in a loop: for i in range(", num_of_sheep,
                  " returning a Sheep object with every loop transition and adding it to a list: ", sheep)

    wolf = Wolf(0.0, 0.0, wolf_move_dist, sheep)
    logging.debug("Function Wolf(", 0.0, 0.0, wolf_move_dist, sheep, ") was called, returning a Wolf object:", wolf)

    pos_data = []

    for simulation_round in range(1, rounds + 1):
        for s in sheep:
            rand_direction = random_direction()
            s.move_sheep(rand_direction, sheep_move_dist)
            logging.debug("Function s.move_sheep(", rand_direction, sheep_move_dist, ") was called")

        wolf.move_wolf()
        logging.debug("Function wolf.move_wolf() was called")

        alive = []

        for i in sheep:
            if i.is_dead is False:
                alive.append(i)
                logging.debug("Function alive.append(", i, ") was called")

        print('\nRound number: ', simulation_round)
        print('Wolf position: ', format(wolf.x, '.3f'), ', ', format(wolf.y, '.3f'))
        print('Number of sheep alive: ', len(alive))
        if wolf.is_chasing is not True:
            print('Wolf has eaten sheep number: ', wolf.sheep_number)
        else:
            print('Wolf is chasing sheep number: ', wolf.sheep_number)

        sheep_pos = []

        for j in range(0, len(sheep)):
            if sheep[j].is_dead is not True:
                sheep_pos.append([sheep[j].x, sheep[j].y])
                logging.debug("Function sheep_pos.append(", [sheep[j].x, sheep[j].y], ") was called")
            else:
                sheep_pos.append('null')
                logging.debug("Function sheep_pos.append('null') was called")

        pos_data.append({
            'round_no': simulation_round,
            'wolf_pos': [wolf.x, wolf.y],
            'sheep_pos': sheep_pos
        })

        # with open('pos.json', 'a') as f_json:
        #     json.dump(pos_data, f_json, indent=2)

        row_alive = [simulation_round, len(alive)]
        with open(path + 'alive.csv', 'a', newline='') as f_csv:
            writer = csv.writer(f_csv)
            if simulation_round == 1:
                writer.writerow(['round', 'alive'])
            writer.writerow(row_alive)
            logging.debug("Function writer.writerow(", row_alive, ") was called")

        if wait_for_key:
            input("Press any key to continue...")

        logging.info('Round number: ' + str(simulation_round) + ' Wolf position: ' + str(wolf.x) + ', ' + str(wolf.y)
                     + 'Chased sheep number: ' + str(wolf.victim.id_sheep) + 'Chased sheep position'
                     + str(wolf.victim.x) + ', ' + str(wolf.victim.y) + 'Number of sheep alive: '
                     + str(len(sheep)) + 'Number of dead sheep: ' + str(num_of_sheep - len(sheep)))

    save_to_json(pos_data, path)


simulation()
