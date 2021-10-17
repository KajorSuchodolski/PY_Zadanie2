import math


# KOD DO POPRAWY BTW

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

            for pp in self.sheep:
                if pp.is_dead is False:
                    sheep_distances.append(self.check_distance(pp.x, pp.y))

            sheep_number = self.sheep[sheep_distances.index(min(sheep_distances))].id_sheep
            self.sheep_number = sheep_number
            self.victim = next((s for s in self.sheep if s.id_sheep == self.sheep_number), None)

            self.chase()

        else:
            self.chase()

    def chase(self):
        if self.wolf_move_dist > self.check_distance(self.victim.x, self.victim.y):
            self.x = self.victim.x
            self.y = self.victim.y
            self.victim.is_dead = True
            # self.sheep.remove(self.victim)
            self.is_chasing = False

        # TODO
        else:
            move_to_x = self.wolf_move_dist * (self.victim.x - self.x) / self.check_distance(self.victim.x, self.victim.y)
            move_to_y = self.wolf_move_dist * (self.victim.y - self.y) / self.check_distance(self.victim.x, self.victim.y)
            self.x += move_to_x
            self.y += move_to_y

    def check_distance(self, x, y):
        return math.sqrt(((x - self.x) ** 2) + ((y - self.y) ** 2))
