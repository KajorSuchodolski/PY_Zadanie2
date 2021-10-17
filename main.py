import random
import json
import csv
import argparse
import configparser
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

# if args.dir:
#     if not os.path.isdir(dir):
#         os.mkdir(dir)

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


def save_to_json(data):
    with open('pos.json', 'w') as f_json:
        json.dump(data, f_json, indent=2)


def random_direction():
    return random.randint(0, 3)


def random_position():
    return random.uniform(-init_pos_limit, init_pos_limit)


def simulation():
    sheep = [Sheep(random_position(), random_position(), i + 1) for i in range(num_of_sheep)]
    wolf = Wolf(0.0, 0.0, wolf_move_dist, sheep)

    pos_data = []

    for simulation_round in range(1, rounds + 1):
        for s in sheep:
            s.move_sheep(random_direction(), sheep_move_dist)

        wolf.move_wolf()

        alive = []

        for i in sheep:
            if i.is_dead is False:
                alive.append(i)

        print('\nRound number: ', simulation_round)
        print('Wolf position: ', wolf.x, ', ', wolf.y)
        print('Number of sheep alive: ', len(alive))
        if wolf.is_chasing is not True:
            print('Wolf has eaten sheep number: ', wolf.sheep_number)
        else:
            print('Wolf is uwu chasing :3 sheep number: ', wolf.sheep_number)
        umu_sheep = wolf.victim
        print('Sheep umu: ', umu_sheep.x, umu_sheep.y)

        sheep_pos = []

        for j in range(0, len(sheep)):
            if sheep[j].is_dead is not True:
                sheep_pos.append([sheep[j].x, sheep[j].y])
            else:
                sheep_pos.append('null')

        pos_data.append({
            'round_no': simulation_round,
            'wolf_pos': [wolf.x, wolf.y],
            'sheep_pos': sheep_pos
        })

        # with open('pos.json', 'a') as f_json:
        #     json.dump(pos_data, f_json, indent=2)

        row_alive = [simulation_round, len(alive)]
        with open('alive.csv', 'a', newline='') as f_csv:
            writer = csv.writer(f_csv)
            if simulation_round == 1:
                writer.writerow(['round', 'alive'])
            writer.writerow(row_alive)

        if wait_for_key:
            input("Press any key to continue...")

    save_to_json(pos_data)


simulation()
