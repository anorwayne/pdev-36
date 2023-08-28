import random


class BoardOutException(Exception):
    pass


class Board:
    def __int__(self, size):
        self.size = size
        self.board = [["О" for _ in range(size)] for _ in range(size)]

    def display(self, show_ships=False):
        print(" " + " ".join([str(i + 1) for i in range(self.size)]))
        for i in range(self.size):
            row = []
        for j in range(self.size):
            if self.board[i][j] == "X" or (show_ships and self.board[i][j] == "■"):
                row.append(self.board[i][j])
            elif self.board[i][j] == '-':
             row.append("T")
        else:
            row.append("О")
            print(chr(65 + i) + " " + " ".join(row))


def is_valid_position(self, x, y):
    return 0 <= x < self.size and 0 <= y < self.size


def is_hit(self, x, y):
    return self.board[y][x] == "O"


def place_ship(self, ship):
    for x, y in ship.positions:
        self.board[y][x] = "O"


def is_overlap(self, positions):
    for x, y in positions:
        if self.board[y][x] == "O":
            return True
        return False


class Ship:
    def __init__(self, positions):
        self.positions = positions
        self.is_sunk = False

    def get_ship_size(self):
        return len(self.positions)


class Game:
    def __init__(self, size):
        self.size = size
        self.player_board = Board(size)
        self.ai_board = Board(size)
        self.player_ships = []
        self.ai_ships = []
        self.moves = []

    def setup(self):
        print("Добро пожаловать в Морской бой!")
        print("Расставьте свои корабли на поле:")
        self.place_ships(self.player_board, self.player_ships)
        self.place_ships(self.ai_board, self.ai_ships, ai=True)

    def place_ships(self, board, ships, ai=False):
        num_ships = [1, 2, 4]  # Кол-во кораблей разных размеров
        ship_size = [3, 2, 1]  # Размеры кораблей соответственно
        for i, count in enumerate(num_ships):
            for _ in range(count):
                while True:
                    x, y = random.randint(0, self.size - 1), random.randint(0, self.size - 1)
                    if ai:
                        direction = random.choice(["h", "v"])
                    else:
                        position = input(
                            f"Введите начальную координату корабля размером {ship_size[i]} (например, A1: ")
                        direction = input("Введите направление корабля (h - горизонтальное, v - вертикальное): ")
                        x, y = self.parse_coordinates(position)

                        position = self.get_ship_positions(x, y, ship_size[i], direction)
                        if not board.is_valid_positions(x, y):
                            continue

                        if board.is_overlap(position):
                            continue
                            break
                            ship = Ship(positions)
                            ships.append(ship)
                            board.place_ship(ship)

    def parse_coordinates(self, positions):
        x = ord(positions[0].upper()) - 65
        y = int(positions[1:]) - 1
        return x, y

    def get_ship_positions(self, x, y, size, direction):
        positions = []
        for i in range(size):
            if direction == "h":
                positions.append((x + i, y))
            elif direction == "v":
                positions.append((x, y + i))
                return positions

    def make_move(self, board):
        while True:
            move = input("ведите координаты выстрела (например, A1): ")
            x, y = self.parse_coordinates(move)
            if not board.is_valid_positions(x, y):
                raise BoardOutException("Ошибка! Недопустимые координаты! ( Вы стреляете за пределы поля.")
            if (x, y) in self.moves:
                raise Exception("Ошибка! В эту клетку уже стреляли.")
            self.moves.append((x, y))
            if board.is_hit(x, y):
                board.board[y][x] = "X"
                print("Попадание!")
                return True
            else:
                board.board[y][x] = "-"
                print("Мимо!")
                return False

    def ai_move(self):
        while True:
            x, y = random.randint(0, self.size - 1), random.randint(0, self.size - 1)
            if (x, y) not in self.moves:
                break

            self.moves.append((x, y))
            if self.player_board.is_hit(x, y):
                self.player_board.board[y][x] = "X"
                print("\nХод компьютера: " + chr(65 + y) + str(x + 1))
                print("Попадание!")
                return True
            else:
                self.player_board.board[y][x] = "-"
                print("\nХод компьютера: " + chr(65 + y) + str(x + 1))
                print("Мимо!")
                return False

    def play(self):
        print("Игра началась!\n")
        self.setup()
        player_turn = True
        ai_turn = False
        player_moves = 0
        ai_moves = 0
        while True:
            self.player_board.display(show_ships=True)
            print("\n")
            self.ai_board.display()
            try:
                if player_turn:
                    print("\nВаш ход:")
                    player_hit = self.make_move(self.ai_board)
                if player_hit:
                    player_moves += 1
                else:
                    print("\nХод компьютера:")
                    ai_hit = self.ai_move()
                    if ai_hit:
                        ai_moves += 1
                        if self.check_game_over(self.ai_ships):
                            print("\nКомпьютер победил!")
                            break

                if player_turn and not player_hit:
                    player_turn = False
                    ai_turn = True
                elif ai_turn and not ai_hit:
                    player_turn = True
                    ai_turn = False
            except Exception as e:
                print(e)
                print("Количество ходов игрока:", player_moves)
                print("Количество ходов компьютера:", ai_moves)
