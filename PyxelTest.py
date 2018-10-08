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

    def __init__(self, x, y, color=0, sprite=0, solid=True, behavior=None):
        self.id = Object.last_id
        Object.last_id += 1
        self.color = color
        self.sprite = sprite
        self.x = x
        self.y = y
        self.solid = solid

        self.image_x = (sprite % 10)*TILE_SIZE
        self.image_y = (sprite // 10)*TILE_SIZE

        self.solid = solid
        self.behavior = behavior

    @classmethod
    def from_name(cls, x, y, name, color=0, sprite=1, solid=True, behavior=None):

        if name == 'player':
            color = 8
            sprite = 82
            behavior = 'player'
        elif name == 'wall':
            color = 2
            sprite = 1
        elif name == 'stairs_down':
            color = 2
            sprite = 12
            solid = False

        return Object(x, y, color=color, sprite=sprite, solid=solid, behavior=behavior)

    def draw(self):
        draw_tile(self.x, self.y, self.sprite, self.color)


def make_a_move():
    in_game_keys = [pyxel.KEY_W, pyxel.KEY_A, pyxel.KEY_S, pyxel.KEY_D]

    if any(pyxel.btnp(key) for key in in_game_keys):
        return True
    else:
        return False


class ObjectHandler:
    def __init__(self):
        self.objects = []
        self.generate_location()

    def generate_location(self):
        self.objects.append(Object.from_name(13, 5, 'player'))

        self.objects.append(Object.from_name(4, 4, 'stairs_down'))
        for i in range(SCREEN_WIDTH // TILE_SIZE):
            self.objects.append(Object.from_name(i, 0, 'wall'))
        for i in range(SCREEN_WIDTH // TILE_SIZE):
            self.objects.append(Object.from_name(i, SCREEN_HEIGHT // TILE_SIZE - 1, 'wall'))
        for i in range(1, SCREEN_HEIGHT // TILE_SIZE-1):
            self.objects.append(Object.from_name(0, i, 'wall'))
        for i in range(1, SCREEN_HEIGHT // TILE_SIZE-1):
            self.objects.append(Object.from_name(SCREEN_WIDTH // TILE_SIZE - 1, i, 'wall'))

    def passable(self, x, y):
        for obj in self.objects:
            if obj.x == x and obj.y == y and obj.solid is True:
                return False
        return True

    def perform_moves(self):

        for obj in self.objects:
            if obj.behavior == 'player':
                if pyxel.btnp(pyxel.KEY_W) and self.passable(obj.x, obj.y - 1):
                    obj.y = (obj.y - 1) % SCREEN_HEIGHT
                elif pyxel.btnp(pyxel.KEY_A) and self.passable(obj.x - 1, obj.y):
                    obj.x = (obj.x - 1) % SCREEN_WIDTH
                elif pyxel.btnp(pyxel.KEY_S) and self.passable(obj.x, obj.y + 1):
                    obj.y = (obj.y + 1) % SCREEN_WIDTH
                elif pyxel.btnp(pyxel.KEY_D) and self.passable(obj.x + 1, obj.y):
                    obj.x = (obj.x + 1) % SCREEN_WIDTH


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
