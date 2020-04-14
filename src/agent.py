from copy import deepcopy
from time import time

MAX_LEVEL = 5  # 4 for faster action
MAX_TIME = 10  # None


class Node:
    def __init__(self, board, parent=None):
        self.board = board
        self.parent = parent
        self.extreme_utility = None
        self.best_move = None

    def __lt__(self, other):
        return self.extreme_utility < other.extreme_utility

    def __str__(self):
        return '\n'.join([' '.join(row) for row in self.board.board]) + '\n'


class Tree:

    def __init__(self, board, color, opponentColor, start_time, time):
        self.root = Node(board)
        self.max_level = None
        self.color = color
        self.opponentColor = opponentColor
        self.start_row, self.end_row = (0, 5) if self.color == 'W' else (5, 0)
        self.dir = 1 if self.start_row < self.end_row else -1
        self.start_time = start_time
        self.time = time

    def minimax_alpha_beta_search(self, parent, level):
        enough_search = level >= self.max_level or self.time_is_over()

        whose_turn = self.color if level % 2 == 0 else self.opponentColor
        from_cells, to_sets_of_cells = parent.board.getPiecesPossibleLocations(whose_turn)
        for i, from_cell in enumerate(from_cells):
            to_set_of_cells = to_sets_of_cells[i]
            for to_cell in to_set_of_cells:
                new_board = deepcopy(parent.board)
                new_board.changePieceLocation(whose_turn, from_cell, to_cell)
                child = Node(new_board, parent=parent)
                print(from_cell, to_cell)
                print(child)
                # todo:   return extreme_utility  and assign best move

    def time_is_over(self):
        return self.time is not None and time() >= self.start_time + self.time

    # return best move (from cell, to cell), for example: ((4, 0), (3, 1))
    def move(self):
        self.max_level = 0
        while self.max_level <= MAX_LEVEL and not self.time_is_over():
            self.minimax_alpha_beta_search(self.root, 0)
            self.max_level += 1
        return self.root.best_move


class Agent:
    def __init__(self, color, opponentColor, time=MAX_TIME):
        self.color = color
        self.opponentColor = opponentColor
        self.time = time

    def move(self, board):
        start_time = time()
        tree = Tree(board, self.color, self.opponentColor, start_time, self.time)
        return tree.move()
