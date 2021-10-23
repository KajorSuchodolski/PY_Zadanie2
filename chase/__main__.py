import argparse
import configparser
import csv
import json
import logging
import os
import random
from chase.Sheep import Sheep
from chase.Wolf import Wolf


def save_to_json(data, path_json):
    with open(path_json + 'pos.json', 'w') as f_json:
        json.dump(data, f_json, indent=2)


def save_to_csv(data, path_csv):
    with open(path_csv + 'alive.csv', 'w', newline='') as f_csv:
        writer = csv.writer(f_csv)
        logging.debug("Function writer(" + str(f_csv) + ") was called on a csv class object: " + str(csv))

        for i in data:
            writer.writerow(i)
            logging.debug("Function writerow(" + str(i)
                          + ") was called on a writer class object: " + str(writer))


def random_direction():
    return random.randint(0, 3)


def random_position(init_pos_limit):
    return random.uniform(-init_pos_limit, init_pos_limit)


def simulation(rounds, init_pos_limit, sheep_move_dist, wolf_move_dist, num_of_sheep, wait_for_key, absolute_dir):

    sheep = []

    for i in range(num_of_sheep):
        rand_x = random_position(init_pos_limit)
        rand_y = random_position(init_pos_limit)

        sheep_obj = Sheep(rand_x, rand_y, i + 1)
        sheep.append(sheep_obj)
        logging.debug("Constructor Sheep(" + str(rand_x) + ", " + str(rand_y) + ", " + str(i + 1)
                      + ") was called, creating a Sheep object: " + str(sheep_obj))

    wolf = Wolf(0.0, 0.0, wolf_move_dist, sheep)
    logging.debug("Constructor Wolf( 0.0, 0.0, " + str(wolf_move_dist) + ", " + str(sheep)
                  + " was called, creating a Wolf object: " + str(wolf))

    pos_data = []
    row_alive = []

    for simulation_round in range(1, rounds + 1):

        alive = []

        for s in sheep:
            if s.is_dead is False:
                rand_direction = random_direction()
                s.move_sheep(rand_direction, sheep_move_dist)
                logging.debug("Function move_sheep(" + str(rand_direction) + ", "
                              + str(sheep_move_dist) + ") was called on a Sheep class object: " + str(s))
                alive.append(s)
                logging.debug("Function alive.append(" + str(s) + ") was called.")

        logging.info("Alive: " + str(alive))

        if not alive:
            print("Wolf has eaten all the sheep!")
            return

        wolf.move_wolf()
        logging.debug("Function move_wolf() was called on a Wolf class object: " + str(wolf))

        # alive = []
        #
        # for i in sheep:
        #     if i.is_dead is False:
        #         alive.append(i)
        #         logging.debug("Function alive.append(" + str(i) + ") was called")

        print('\nRound number: ', simulation_round)
        print('Wolf position: ', format(wolf.x, '.3f'), ', ', format(wolf.y, '.3f'))
        print('Number of sheep alive: ', len(alive))
        if wolf.is_chasing is False:
            print('Wolf has eaten sheep number: ', wolf.sheep_number)
            if not alive:
                print('lel')
                return
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

        row_alive.append([simulation_round, len(alive)])

        if wait_for_key:
            input("Press any key to continue...")

        logging.info('Round number: ' + str(simulation_round) + ' Wolf position: ' + str(wolf.x) + ', ' + str(wolf.y)
                     + 'Chased sheep number: ' + str(wolf.victim.id_sheep) + 'Chased sheep position'
                     + str(wolf.victim.x) + ', ' + str(wolf.victim.y) + 'Number of sheep alive: '
                     + str(len(alive)) + 'Number of dead sheep: ' + str(num_of_sheep - len(alive)))

    save_to_json(pos_data, absolute_dir)
    save_to_csv(row_alive, absolute_dir)
    logging.debug("Function save_to_json(" + str(pos_data) + ", " + str(absolute_dir) + ") was called")


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
