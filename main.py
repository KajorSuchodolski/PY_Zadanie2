import random
import json
import csv
import argparse
import configparser
import logging
import os
from chase.Sheep import Sheep
from chase.Wolf import Wolf

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
print(args.config)


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


def save_to_json(data, path_json):
    with open(path_json + 'pos.json', 'w') as f_json:
        json.dump(data, f_json, indent=2)


def random_direction():
    return random.randint(0, 3)


def random_position():
    return random.uniform(-init_pos_limit, init_pos_limit)


def simulation():

    rand_x = random_position()
    rand_y = random_position()

    sheep = []
    for i in range(num_of_sheep):
        sheep.append(Sheep(rand_x, rand_y, i + 1))
        logging.debug("Constructor Sheep(" + str(rand_x) + ", " + str(rand_y) + ", " + str(i + 1) + ") was called")

    wolf = Wolf(0.0, 0.0, wolf_move_dist, sheep)
    logging.debug("Constructor Wolf( 0.0, 0.0, " + str(wolf_move_dist) + ", " + str(sheep) + " was called")

    pos_data = []

    for simulation_round in range(1, rounds + 1):

        alive = []

        for s in sheep:
            if s.is_dead is False:
                alive.append(s)
                rand_direction = random_direction()
                s.move_sheep(rand_direction, sheep_move_dist)
                logging.debug("Function move_sheep(" + str(rand_direction) + ", "
                          + str(sheep_move_dist) + ") was called on a Sheep class object: " + str(s))
                logging.debug("Function alive.append(" + str(s) + ") was called.")

        logging.info("Alive: " + str(alive))

        if not alive:
            print("Wolf has eaten all the sheep!")
            return

        wolf.move_wolf()
        logging.debug("Function move_wolf() was called on a Wolf class object: " + str(wolf))


        # for i in sheep:
        #     if i.is_dead is False:
        #         alive.append(i)
        #         logging.debug("Function alive.append(" + str(i) + ") was called")

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
                logging.debug("Function append(" + str(sheep[j].x) + ", " + str(sheep[j].y)
                              + ") was called on a sheep_pos list: " + str(sheep_pos))
            else:
                sheep_pos.append('null')
                logging.debug("Function append('null') was called on a sheep_pos list: " + str(sheep_pos))

        pos_data.append({
            'round_no': simulation_round,
            'wolf_pos': [wolf.x, wolf.y],
            'sheep_pos': sheep_pos
        })

        # with open('pos.json', 'a') as f_json:
        #     json.dump(pos_data, f_json, indent=2)

        row_alive = [simulation_round, len(alive)]
        with open(absolute_dir + 'alive.csv', 'a', newline='') as f_csv:
            writer = csv.writer(f_csv)
            logging.debug("Function writer(" + str(f_csv) + ") was called on a csv class object: " + str(csv))

            if simulation_round == 1:
                writer.writerow(['round', 'alive'])
                logging.debug("Function writerow(" + str(['round', 'alive'])
                              + ") was called on a writer class object: " + str(writer))
            writer.writerow(row_alive)
            logging.debug("Function writerow(" + str(row_alive)
                          + ") was called on a writer class object: " + str(writer))

        if wait_for_key:
            input("Press any key to continue...")

        logging.info('Round number: ' + str(simulation_round) + ' Wolf position: ' + str(wolf.x) + ', ' + str(wolf.y)
                     + 'Chased sheep number: ' + str(wolf.victim.id_sheep) + 'Chased sheep position'
                     + str(wolf.victim.x) + ', ' + str(wolf.victim.y) + 'Number of sheep alive: '
                     + str(len(alive)) + 'Number of dead sheep: ' + str(alive - len(sheep)))

    save_to_json(pos_data, absolute_dir)
    logging.debug("Function save_to_json(" + str(pos_data) + ", " + str(absolute_dir) + ") was called")


simulation()
logging.debug("Function simulation() was called")





