import pyxel


COL_BACKGROUND = 0
TILE_SIZE = 8
SCREEN_WIDTH = 160
SCREEN_HEIGHT = 120


def draw_tile(x, y, image_num, color):
    i = image_num // 10
    j = image_num % 10
    pyxel.pal(7, color)
    pyxel.blt(x*TILE_SIZE, y*TILE_SIZE, 0, j*TILE_SIZE, i*TILE_SIZE, TILE_SIZE, TILE_SIZE)
    pyxel.pal()


class Object:
    last_id = 0

    def __init__(self, x, y, color, sprite, solid=True):
        self.id = Object.last_id
        Object.last_id += 1
        self.color = color
        self.sprite = sprite
        self.x = x
        self.y = y
        self.solid = solid

        self.image_x = (sprite % 10)*TILE_SIZE
        self.image_y = (sprite // 10)*TILE_SIZE

    def move(self):
        return []

    def draw(self):
        draw_tile(self.x, self.y, self.sprite, self.color)


class Creature(Object):
    def __init__(self, x, y, color, sprite, solid=True):
        super().__init__(x, y, color, sprite, solid)


class Player(Creature):
    def __init__(self, x, y, color, sprite, solid=True):
        super().__init__(x, y, color, sprite, solid)

    def move(self):
        action_list = []
        if pyxel.btnp(pyxel.KEY_W):
            action_list.append({'object_id': self.id, 'action': 'mvUp'})
        elif pyxel.btnp(pyxel.KEY_A):
            action_list.append({'object_id': self.id, 'action': 'mvLt'})
        elif pyxel.btnp(pyxel.KEY_S):
            action_list.append({'object_id': self.id, 'action': 'mvDn'})
        elif pyxel.btnp(pyxel.KEY_D):
            action_list.append({'object_id': self.id, 'action': 'mvRt'})
        return action_list


def make_a_move():
    in_game_keys = [pyxel.KEY_W, pyxel.KEY_A, pyxel.KEY_S, pyxel.KEY_D]

    if any(pyxel.btnp(key) for key in in_game_keys):
        return True
    else:
        return False


class ObjectHandler:
    def __init__(self):
        self.objects = []
        self.objects.append(Player(13, 5, 8, 82))
        for i in range(SCREEN_WIDTH // TILE_SIZE):
            self.objects.append(Object(i, 0, 2, 1))
        for i in range(SCREEN_WIDTH // TILE_SIZE):
            self.objects.append(Object(i, SCREEN_HEIGHT // TILE_SIZE - 1, 2, 1))
        for i in range(1, SCREEN_HEIGHT // TILE_SIZE-1):
            self.objects.append(Object(0, i, 2, 1))
        for i in range(1, SCREEN_HEIGHT // TILE_SIZE-1):
            self.objects.append(Object(SCREEN_WIDTH // TILE_SIZE - 1, i, 2, 1))

    def passable(self, x, y):
        for obj in self.objects:
            if obj.x == x and obj.y == y and obj.solid is True:
                return False
        return True

    def perform_moves(self):

        for obj in self.objects:
            for move in [mv for mv in obj.move() if mv]:
                subj = self.objects[move['object_id']]
                action = move['action']
                if action == 'mvUp' and self.passable(subj.x, subj.y - 1):
                    subj.y = (subj.y - 1) % SCREEN_HEIGHT
                if action == 'mvLt' and self.passable(subj.x - 1, subj.y):
                    subj.x = (subj.x - 1) % SCREEN_WIDTH
                if action == 'mvDn' and self.passable(subj.x, subj.y + 1):
                    subj.y = (subj.y + 1) % SCREEN_WIDTH
                if action == 'mvRt' and self.passable(subj.x + 1, subj.y):
                    subj.x = (subj.x + 1) % SCREEN_WIDTH


class App:
    def __init__(self):
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT)

        pyxel.image(0).load(0, 0, 'minirogue-c64-all.png')
        self.objectHandler = ObjectHandler()

        pyxel.run(self.update, self.draw)

    def update(self):
        if make_a_move():
            self.objectHandler.perform_moves()

    def draw(self):
        pyxel.cls(COL_BACKGROUND)
        for i in range(SCREEN_HEIGHT // TILE_SIZE):
            for j in range(SCREEN_WIDTH // TILE_SIZE):
                pyxel.rectb(j * TILE_SIZE, i * TILE_SIZE, (j + 1) * TILE_SIZE - 1, (i + 1) * TILE_SIZE - 1, 5)

        for obj in self.objectHandler.objects:
            obj.draw()

        if pyxel.btn(pyxel.KEY_T):
            for i in range(128):
                draw_tile(i % 10 + 1, i // 10 + 1, i, 1 + i % 14)


App()
