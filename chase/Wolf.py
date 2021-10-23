import logging
import math


class Wolf:
    def __init__(self, x, y, wolf_move_dist, sheep):
        self.victim = None
        self.sheep_number = 0
        self.x = x
        self.y = y
        self.wolf_move_dist = wolf_move_dist
        self.is_chasing = False
        self.sheep = sheep

    def move_wolf(self):

        if self.is_chasing is False:
            self.is_chasing = True
            sheep_distances = []

            for shp in self.sheep:
                if shp.is_dead is False:
                    sheep_distances.append(self.check_distance(shp.x, shp.y))

            sheep_number = self.sheep[sheep_distances.index(min(sheep_distances))].id_sheep
            self.sheep_number = sheep_number
            self.victim = next((s for s in self.sheep if s.id_sheep == self.sheep_number), None)

            self.chase()
            logging.debug("Function chase(" + str(self) + ") was called")

        else:
            self.chase()

    def chase(self):
        distance_wolf = self.check_distance(self.victim.x, self.victim.y)
        logging.debug("Function check_distance(" + str(self.victim.x) + " " + str(self.victim.y)
                      + ") was called on a Wolf object: " + str(self)
                      + ", returning the value of " + str(distance_wolf))

        if self.wolf_move_dist > distance_wolf:
            logging.info('Wolf has caught sheep number ' + str(self.victim.id_sheep) + ' at position'
                         + str(self.victim.x) + ' ' + str(self.victim.y) + ' from position '
                         + str(self.x) + ' ' + str(self.y))
            self.x = self.victim.x
            self.y = self.victim.y
            self.victim.is_dead = True
            self.is_chasing = False

            if not self.sheep:
                print('Wolf has consumed all of the sheep')

        else:
            move_to_x = self.wolf_move_dist \
                        * (self.victim.x - self.x) / self.check_distance(self.victim.x, self.victim.y)
            move_to_y = self.wolf_move_dist \
                        * (self.victim.y - self.y) / self.check_distance(self.victim.x, self.victim.y)
            logging.info('Wolf headed ' + str(move_to_x) + ' ' + str(move_to_y) + ' from position'
                         + str(self.x) + ' ' + str(self.y))
            self.x += move_to_x
            self.y += move_to_y

    def check_distance(self, x, y):
        return math.sqrt(((x - self.x) ** 2) + ((y - self.y) ** 2))
