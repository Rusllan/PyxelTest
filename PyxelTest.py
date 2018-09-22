import pyxel


class object:
    def __init__(self, id, x, y, color, sprite, tile_size):
        self.id = id
        self.color = color
        self.sprite = sprite
        self.x = x
        self.y = y
        self.tile_size = tile_size
        self.image_x = (sprite % 10)*self.tile_size
        self.image_y = (sprite // 10)*self.tile_size

    def draw(self):
        pyxel.pal(7, self.color)
        pyxel.blt(self.x, self.y, 0, self.image_x, self.image_y, 8, 8)


class App:
    def __init__(self):
        pyxel.init(160, 120)
        self.tile_size = 8

        pyxel.image(0).load(0, 0, 'minirogue-c64-all.png')
        self.player = object(1, 0, 0, 8, 82, 8)
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_W):
            self.player.y = (self.player.y - self.tile_size) % pyxel.height
        if pyxel.btnp(pyxel.KEY_A):
            self.player.x = (self.player.x - self.tile_size) % pyxel.width
        if pyxel.btnp(pyxel.KEY_S):
            self.player.y = (self.player.y + self.tile_size) % pyxel.height
        if pyxel.btnp(pyxel.KEY_D):
            self.player.x = (self.player.x + self.tile_size) % pyxel.width

    def draw_tile(self, x, y, image_num, color):
        i = image_num // 10
        j = image_num % 10
        pyxel.pal(7, color)
        pyxel.blt(x, y, 0, j*self.tile_size, i*self.tile_size, self.tile_size, self.tile_size)
        pyxel.pal()

    def draw(self):
        pyxel.cls(0)
        for i in range(pyxel.height // self.tile_size):
            for j in range(pyxel.width // self.tile_size):
                pyxel.rectb(j * self.tile_size, i * self.tile_size,
                            (j + 1) * self.tile_size - 1, (i + 1) * self.tile_size - 1, 5)

        for i in range(128):
            self.draw_tile((i % 10)*self.tile_size , (i//10)*self.tile_size, i, 1 + i%14)
        self.player.draw()


App()
