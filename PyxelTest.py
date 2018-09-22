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


class Event:
    def __init__(self, object_id, action):
        self.object_id = object_id
        self.action = action


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

    def action(self):
        return Event(self.id, 'none')

    def draw(self):
        draw_tile(self.x, self.y, self.sprite, self.color)


class Creature(Object):
    def __init__(self, x, y, color, sprite, solid=True):
        super().__init__(x, y, color, sprite, solid)


class Player(Creature):
    def __init__(self, x, y, color, sprite, solid=True):
        super().__init__(x, y, color, sprite, solid)

    def action(self):
        if pyxel.btnp(pyxel.KEY_W):
            return Event(self.id, 'mvUp')
        elif pyxel.btnp(pyxel.KEY_A):
            return Event(self.id, 'mvLt')
        elif pyxel.btnp(pyxel.KEY_S):
            return Event(self.id, 'mvDn')
        elif pyxel.btnp(pyxel.KEY_D):
            return Event(self.id, 'mvRt')
        else:
            return super().action()


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
            if obj.x == x and obj.y == y and obj.solid == True:
                return False
        return True

    def get_events(self):
        events = []
        for obj in self.objects:
            event = obj.action()
            if event.action != 'none':
                events.append(event)
        return events


class App:
    def __init__(self):
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT)

        pyxel.image(0).load(0, 0, 'minirogue-c64-all.png')
        self.objectHandler = ObjectHandler()

        pyxel.run(self.update, self.draw)

    def update(self):
        self.perform_events(self.objectHandler.get_events())

    def perform_events(self, events):

        for event in events:
            obj = self.objectHandler.objects[event.object_id]

            if event.action == 'mvUp' and self.objectHandler.passable(obj.x, obj.y - 1):
                obj.y = (obj.y - 1) % SCREEN_HEIGHT
            if event.action == 'mvLt' and self.objectHandler.passable(obj.x - 1, obj.y):
                obj.x = (obj.x - 1) % SCREEN_WIDTH
            if event.action == 'mvDn' and self.objectHandler.passable(obj.x, obj.y + 1):
                obj.y = (obj.y + 1) % SCREEN_WIDTH
            if event.action == 'mvRt' and self.objectHandler.passable(obj.x + 1, obj.y):
                obj.x = (obj.x + 1) % SCREEN_WIDTH

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
