import random
from enum import Enum


class GameResult(Enum):
    WINNER_EXIST = 1
    DRAW = 2
    UNTERMINATED = 3


class Player(Enum):
    X = 1
    O = 2

    def other(self):
        return Player.X if self == Player.O else Player.O

    def __str__(self):
        return "X" if self == Player.X else "O"

    def __repr__(self):
        return str(self)


class TicTacToeBoard:
    def __init__(self, start_player: Player):
        self.grid = None
        self.current_player = None
        self.is_terminal = False
        self.result = None
        self.winner = None

        self.reset(start_player)

    def reset(self, start_player: Player):
        self.grid = [None for _ in range(9)]
        self.current_player = start_player
        self.is_terminal = False
        self.result = None
        self.winner = None

    def make_move(self, move, player: Player):
        if self.grid[move] is not None:
            raise ValueError("Invalid move")
        self.grid[move] = player

        if (result := self.get_result()) != GameResult.UNTERMINATED:
            self.is_terminal = True
            self.result = result
            self.winner = self.get_winner()

        self.current_player = player.other()

    def make_random_move(self, player: Player = None):
        if player is None:
            player = self.current_player
        possible_moves = self.get_possible_moves()
        move = random.choice(possible_moves)
        self.make_move(move, player)

    def get_possible_moves(self):
        return [i for i, player in enumerate(self.grid) if player is None]

    def get_winner(self) -> Player | None:
        if self.grid[0] == self.grid[1] == self.grid[2] != None:
            return self.grid[0]
        if self.grid[3] == self.grid[4] == self.grid[5] != None:
            return self.grid[3]
        if self.grid[6] == self.grid[7] == self.grid[8] != None:
            return self.grid[6]

        if self.grid[0] == self.grid[3] == self.grid[6] != None:
            return self.grid[0]
        if self.grid[1] == self.grid[4] == self.grid[7] != None:
            return self.grid[1]
        if self.grid[2] == self.grid[5] == self.grid[8] != None:
            return self.grid[2]

        if self.grid[0] == self.grid[4] == self.grid[8] != None:
            return self.grid[0]
        if self.grid[2] == self.grid[4] == self.grid[6] != None:
            return self.grid[2]

        return None

    def get_result(self) -> GameResult:
        if self.get_winner():
            return GameResult.WINNER_EXIST
        if not self.get_possible_moves():
            return GameResult.DRAW
        return GameResult.UNTERMINATED

    def draw_board(self):
        print("_" * 5)
        for i in range(3):
            print(
                "|"
                + "".join(
                    str(cell if cell else "*")
                    for j, cell in enumerate(self.grid[i * 3 : i * 3 + 3])
                )
                + "|"
            )
        print("‾" * 5)
