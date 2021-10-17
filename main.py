import random
import json
import csv
from Sheep import Sheep
from Wolf import Wolf

# Liczba tur: 50;
# Liczba owiec: 15;
# init_pos_limit: 10.0;
# sheep_move_dist: 0.5;
# wolf_move_dist: 1.0.


rounds = 50
init_pos_limit = 10.0
sheep_move_dist = 1.0


def random_direction():
    return random.randint(0, 3)


def random_position():
    return random.uniform(-init_pos_limit, init_pos_limit)


def simulation():
    sheep = [Sheep(random_position(), random_position(), i) for i in range(15)]
    wolf = Wolf(0.0, 0.0, 1.0, sheep)

    for simulation_round in range(1, rounds + 1):
        for s in sheep:
            s.move_sheep(random_direction(), 0.5)

        wolf.move_wolf()

        print('\nRound number: ', simulation_round)
        print('Wolf position: ', wolf.x, ', ', wolf.y)
        print('Number of sheep alive: ', len(sheep))
        if wolf.is_chasing is not True:
            print('Wolf has eaten sheep number: ', wolf.sheep_number)
        else:
            print('Wolf is uwu chasing :3 sheep number: ', wolf.sheep_number)
        umu_sheep = wolf.victim
        print('Sheep umu: ', umu_sheep.x, umu_sheep.y)

        sheep_pos = []

        for j in range(0, len(sheep)):
            if sheep[j].is_dead is False:
                sheep_pos.append([sheep[j].x, sheep[j].y])
            else:
                sheep_pos.append('null')

        pos_data = {
            'round_no': simulation_round,
            'wolf_pos': [wolf.x, wolf.y],
            'sheep_pos': sheep_pos
        }

        with open('pos.json', 'a') as f_json:
            json.dump(pos_data, f_json, indent=2)

        row_alive = [simulation_round, len(sheep)]
        with open('alive.csv', 'a', newline='') as f_csv:
            writer = csv.writer(f_csv)
            if simulation_round == 1:
                writer.writerow(['round', 'alive'])
            writer.writerow(row_alive)


simulation()
