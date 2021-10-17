class Sheep:
    def __init__(self, x, y, id_sheep):
        self.x = x
        self.y = y
        self.id_sheep = id_sheep
        self.is_dead = False

    # up - 0, right - 1, down - 2, left - 3

    def move_sheep(self, direction, sheep_move_dist):
        if direction == 0:
            self.y += sheep_move_dist
        elif direction == 1:
            self.x += sheep_move_dist
        elif direction == 2:
            self.y -= sheep_move_dist
        elif direction == 3:
            self.x -= sheep_move_dist
