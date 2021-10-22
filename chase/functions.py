import csv
import json
import random
import logging
from chase.Sheep import Sheep
from chase.Wolf import Wolf


def save_to_json(data, path_json):
    with open(path_json + 'pos.json', 'w') as f_json:
        json.dump(data, f_json, indent=2)


def random_direction():
    return random.randint(0, 3)


def random_position(init_pos_limit):
    return random.uniform(-init_pos_limit, init_pos_limit)


def simulation(rounds, init_pos_limit, sheep_move_dist, wolf_move_dist, num_of_sheep, wait_for_key, absolute_dir):

    rand_x = random_position(init_pos_limit)
    rand_y = random_position(init_pos_limit)

    sheep = []
    for i in range(num_of_sheep):
        sheep.append(Sheep(rand_x, rand_y, i + 1))
        logging.debug("Constructor Sheep(" + str(rand_x) + ", " + str(rand_y) + ", " + str(i + 1) + ") was called")

    wolf = Wolf(0.0, 0.0, wolf_move_dist, sheep)
    logging.debug("Constructor Wolf( 0.0, 0.0, " + str(wolf_move_dist) + ", " + str(sheep) + " was called")

    pos_data = []

    for simulation_round in range(1, rounds + 1):

        for s in sheep:
            rand_direction = random_direction()
            s.move_sheep(rand_direction, sheep_move_dist)
            logging.debug("Function move_sheep(" + str(rand_direction) + ", "
                          + str(sheep_move_dist) + ") was called on a Sheep class object: " + str(s))

        wolf.move_wolf()
        logging.debug("Function move_wolf() was called on a Wolf class object: " + str(wolf))

        alive = []

        for i in sheep:
            if i.is_dead is False:
                alive.append(i)
                logging.debug("Function alive.append(" + str(i) + ") was called")

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
                     + str(len(sheep)) + 'Number of dead sheep: ' + str(num_of_sheep - len(sheep)))

    save_to_json(pos_data, absolute_dir)
    logging.debug("Function save_to_json(" + str(pos_data) + ", " + str(absolute_dir) + ") was called")
