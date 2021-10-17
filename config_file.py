import configparser


def create_config(init_pos_limit, sheep_move_dist, wolf_move_dist):
    config = configparser.ConfigParser()

    config['Terrain'] = {'InitPosLimit': init_pos_limit}
    config['Movement'] = {
        'SheepMoveDist': sheep_move_dist,
        'WolfMoveDist': wolf_move_dist
    }

    with open('config.ini', 'w') as f_config:
        config.write(f_config)


