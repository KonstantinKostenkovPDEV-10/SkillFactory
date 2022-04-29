from random import randint


class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"({self.x}, {self.y})"


class BoardException(Exception):
    pass


class BoardOutException(BoardException):
    def __str__(self):
        return "Вы пытаетесь выстрелить за доску!"


class BoardUsedException(BoardException):
    def __str__(self):
        return "Вы уже стреляли в эту клетку"


class BWShipException(BoardException):
    pass


class Ship:
    def __init__(self, bow, l, o):
        self.bow = bow
        self.l = l
        self.o = o
        self.lives = l
     

    @property
    def dots(self):
        ship_dots = []
        for i in range(self.l):
            koord_x = self.bow.x
            koord_y = self.bow.y
            if self.o == 0:
                koord_x += i
            else:
                koord_y += i
            ship_dots.append(Dot(koord_x, koord_y))
        return ship_dots

    def shooten(self, shoot):
        return shoot in self.dots

    pass


class Board:
    def __init__(self, hiden=False, size=9):
        self.size = size
        self.hiden = hiden
        self.count = 0
        self.fields = [["0"] * size for i in range(size)]
        self.busy = []
        self.ships = []

    def add_ship(self, ship_current):

        for d in ship_current.dots:
            if self.out(d) or d in self.busy:
                raise BWShipException()
        for d in ship_current.dots:
            self.fields[d.x][d.y] = "■"
            self.busy.append(d)

        self.ships.append(ship_current)
        self.contour(ship_current)

    def contour(self, ship_current, verb= False):
        near = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        for d in ship_current.dots:
            for dx, dy in near:
                cur = Dot(d.x + dx, d.y + dy)
                if (not (self.out(cur))) and (cur not in self.busy):
                    if verb:
                        self.fields[cur.x][cur.y] = "Х"
                    self.busy.append(cur)

    def __str__(self):
        res = ""
        res += "  | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |"
        for i, j in enumerate(self.fields):
            res += f"\n{i + 1} | " + " | ".join(j) + " |"
            if self.hiden:
                res = res.replace("■", "O")
        return res

    def out(self, d):
        return not ((0 <= d.x < self.size) and (0 <= d.y < self.size))

    def shot(self, d):
        if self.out(d):
            raise BoardOutException()

        if d in self.busy:
            raise BoardUsedException()

        self.busy.append(d)

        for ship in self.ships:
            if d in ship.dots:
                ship.lives -= 1
                self.fields[d.x][d.y] = "X"
                if ship.lives == 0:
                    self.count += 1
                    self.contour(ship, verb=True)
                    print("Корабль уничтожен!")
                    return False
                else:
                    print("Корабль ранен!")
                    return True

        self.fields[d.x][d.y] = "."
        print("Мимо!")
        return False

    def begin(self):
        self.busy = []

    pass


class Player:
    def __init__(self, board, enemy):
        self.board = board
        self.enemy = enemy

    def ask(self):
        raise NotImplementedError()

    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy.shot(target)
                return repeat
            except BoardException as e:
                print(e)


class AI(Player):
    def ask(self):
        d = Dot(randint(0, 5), randint(0, 5))
        print(f"Ход компьютера: {d.x + 1} {d.y + 1}")
        return d


class User(Player):
    def ask(self):
        while True:
            cords = input("Ваш ход: ").split()

            if len(cords) != 2:
                print(" Введите 2 координаты! ")
                continue

            x, y = cords

            if not (x.isdigit()) or not (y.isdigit()):
                print(" Введите числа! ")
                continue

            x, y = int(x), int(y)

            return Dot(x - 1, y - 1)


class Game:
    def __init__(self, size=9):
        self.size = size
        pl = self.random_board()
        co = self.random_board()
        co.hid = True

        self.ai = AI(co, pl)
        self.us = User(pl, co)

    def random_board(self):
        board = None
        while board is None:
            board = self.random_place
            return board

    @property
    def random_place(self):
        lens = [1,1,1,1,2,2,3]
        board=Board(size=self.size)
        attempts = 0
        for l in lens:
            while True:
                attempts += 1

                ship = Ship(Dot(randint(1, self.size), randint(1, self.size)), l, randint(0, 1))
                try:
                    board.add_ship(ship)
                    break
                except BWShipException:
                    pass
                board.begin()
                return board

    def greet(self):
        print("------------------------------------------")
        print("---------------ИГРА МОРСКОЙ БОЙ-----------")
        print("------------------------------------------")
        print(" формат ввода координат: x y ")
        print(" x - номер строки  ")
        print(" y - номер столбца ")
    
    def loop(self):
        num = 0
        while True:
            print("-" * 20)
            print("Доска пользователя:")
            print(self.us.board)
            print("-" * 20)
            print("Доска компьютера:")
            print(self.ai.board)
            if num % 2 == 0:
                print("-" * 20)
                print("Ходит пользователь!")
                repeat = self.us.move()
            else:
                print("-" * 20)
                print("Ходит компьютер!")
                repeat = self.ai.move()
            if repeat:
                num -= 1
            if self.ai.board.count == 7:
                print("-" * 20)
                print("Пользователь выиграл!")
                break
            if self.us.board.count == 7:
                print("-" * 20)
                print("Компьютер выиграл!")
                break
            num += 1

    def start(self):
        self.greet()
        self.loop()


g = Game()
g.start()
