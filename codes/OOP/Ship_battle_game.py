from random import randint, choice, shuffle


class Ship:
    def __init__(self, length=1, tp=1, x=None, y=None):
        self._x = x  # start coordinates
        self._y = y  # nose is allways turned left or upwards
        self._tp = tp  # ship orientation: 1 - horiz, 2 - vert
        self._length = length  # ship length
        self._is_move = True  # unable to move after hit (any of _cells is 2)
        self._cells = [1 for _ in range(self._length)]  # 1 - no damage, 2 - hit one or more decks

    def set_start_coords(self, x, y):
        self._x = x
        self._y = y

    def get_start_coords(self):
        return self._x, self._y

    def get_tp_length(self):
        return self._tp, self._length

    def move(self, step):
        if self._is_move == False:
            return
        if self._tp == 1:
            self._x += step
        elif self._tp == 2:
            self._y += step

    # no needs of checking whether the cell is inside the field or not
    def ship_surr_cells(self):  # cells, that surrounds the ship on field
        if self._tp == 1:
            res = [(x, y) for x in range(self._x - 1, self._x + self._length + 1) \
                   for y in range(self._y - 1, self._y + 2)]
        else:
            res = [(x, y) for x in range(self._x - 1, self._x + 2) \
                   for y in range(self._y - 1, self._y + self._length + 1)]
        return set(res)

    def ship_cells(self):  # cells of the ship on field
        if self._tp == 1:
            res = [(x, self._y) for x in range(self._x, self._x + self._length)]
        if self._tp == 2:
            res = [(self._x, y) for y in range(self._y, self._y + self._length)]
        return set(res)

    def is_collide(self, ship):
        return bool(self.ship_surr_cells().intersection(ship.ship_cells()))

    def is_out_pole(self, size):
        if self._tp == 1:
            if self._x < 0 or self._x + self._length > size or self._y < 0 or self._y > size - 1:
                return True
        if self._tp == 2:
            if self._y < 0 or self._y + self._length > size or self._x < 0 or self._x > size - 1:
                return True
        return False

    def __getitem__(self, index):
        return self._cells[index]

    def __setitem__(self, index, value):
        self._cells[index] = value


class GamePole:
    def __init__(self, size=10):
        self._size = size
        self._ships = []

    def init(self):
        self._ships = []
        tries = 0
        success_flag = True
        for i in range(4, 0, -1):
            for l in range(5 - i):  # number of ship with i decks
                s = Ship(length=i, tp=randint(1, 2), x=randint(0, self._size - 1), y=randint(0, self._size - 1))
                while s.is_out_pole(self._size) or any(map(lambda x: s.is_collide(x), self._ships)):
                    s.set_start_coords(randint(0, self._size - 1), randint(0, self._size - 1))
                    tries += 1
                    if tries > 200:
                        break
                self._ships.append(s)
        if tries > 200:
            self.init()

    def get_ships(self):
        return self._ships

    def move_ships(self):
        shuffle(self._ships)
        for ship in self._ships:
            step = choice([-1, 1])
            ship.move(step)
            if ship.is_out_pole(self._size) or \
                    any(map(lambda x: ship.is_collide(x) if x != ship else False, self._ships)):
                ship.move(-2 * step)
            if ship.is_out_pole(self._size) or \
                    any(map(lambda x: ship.is_collide(x) if x != ship else False, self._ships)):
                ship.move(step)

    def get_pole(self):
        res = [['.'] * self._size for _ in range(self._size)]
        for s in self._ships:
            x, y = s.get_start_coords()
            tp, l = s.get_tp_length()
            if tp == 1:
                for _ in range(l):
                    res[y][x] = '0'
                    x += 1
            if tp == 2:
                for _ in range(l):
                    res[y][x] = '0'
                    y += 1
            # unnesessary 2 strings
            x, y = s.get_start_coords()
            if tp == 2:
                res[y][x] = 'V'
            if tp == 1:
                res[y][x] = 'H'
        return tuple(tuple(i) for i in res)

    def show(self):
        for i in self.get_pole():
            print(*i)


#  Tests
ship = Ship(2)
ship = Ship(2, 1)
ship = Ship(3, 2, 0, 0)

assert ship._length == 3 and ship._tp == 2 and ship._x == 0 and ship._y == 0, "неверные значения атрибутов объекта класса Ship"
assert ship._cells == [1, 1, 1], "неверный список _cells"
assert ship._is_move, "неверное значение атрибута _is_move"

ship.set_start_coords(1, 2)
assert ship._x == 1 and ship._y == 2, "неверно отработал метод set_start_coords()"
assert ship.get_start_coords() == (1, 2), "неверно отработал метод get_start_coords()"

ship.move(1)
s1 = Ship(4, 1, 0, 0)
s2 = Ship(3, 2, 0, 0)
s3 = Ship(3, 2, 0, 2)

assert s1.is_collide(s2), "неверно работает метод is_collide() для кораблей Ship(4, 1, 0, 0) и Ship(3, 2, 0, 0)"
assert s1.is_collide(
    s3) == False, "неверно работает метод is_collide() для кораблей Ship(4, 1, 0, 0) и Ship(3, 2, 0, 2)"

s2 = Ship(3, 2, 1, 1)
assert s1.is_collide(s2), "неверно работает метод is_collide() для кораблей Ship(4, 1, 0, 0) и Ship(3, 2, 1, 1)"

s2 = Ship(3, 1, 8, 1)
assert s2.is_out_pole(10), "неверно работает метод is_out_pole() для корабля Ship(3, 1, 8, 1)"

s2 = Ship(3, 2, 1, 5)
assert s2.is_out_pole(10) == False, "неверно работает метод is_out_pole(10) для корабля Ship(3, 2, 1, 5)"

s2[0] = 2
assert s2[0] == 2, "неверно работает обращение ship[indx]"

p = GamePole(10)
p.init()
for nn in range(5):
    for s in p._ships:
        assert s.is_out_pole(10) == False, "корабли выходят за пределы игрового поля"

        for ship in p.get_ships():
            if s != ship:
                assert s.is_collide(ship) == False, "корабли на игровом поле соприкасаются"
    p.move_ships()

gp = p.get_pole()
assert type(gp) == tuple and type(gp[0]) == tuple, "метод get_pole должен возвращать двумерный кортеж"
assert len(gp) == 10 and len(gp[0]) == 10, "неверные размеры игрового поля, которое вернул метод get_pole"

pole_size_8 = GamePole(8)
pole_size_8.init()
pole_size_8.show()
