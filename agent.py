from copy import deepcopy
from time import time
import math

MAX_LEVEL = 4  # 4 for faster action
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
        self.children = []




    def minimax_alpha_beta_search(self, parent, level):
        enough_search = level >= self.max_level or self.time_is_over()

        whose_turn = self.color if level % 2 == 0 else self.opponentColor
        from_cells, to_sets_of_cells = parent.board.getPiecesPossibleLocations(whose_turn)
        for i, from_cell in enumerate(from_cells):
            to_set_of_cells = to_sets_of_cells[i]
            for to_cell in to_set_of_cells:
                new_board = deepcopy(parent.board)
                util=0;
                if whose_turn == 'B':
                    pass



                new_board.changePieceLocation(whose_turn, from_cell, to_cell)
                child = Node(new_board, parent=parent)



                print(from_cell, to_cell)
                print(child)

                self.children.apend(child)
                self.max_value(enough_search,child,alpha= -math.inf,beta= math.inf)

                # todo:   return extreme_utility  and assign best move





    def max_value(self,enough_search ,parent, alpha, beta):
        if enough_search:
            return parent.Evaluation
        ex_util= -math.inf
        for s in self.children:
            ex_util= max(ex_util,self.min_value(enough_search,s,alpha,beta))
            if ex_util >= beta :
                return ex_util
            alpha = max(alpha, ex_util)
            return ex_util


    def min_value(self,enough_search ,parent, alpha, beta):
        if enough_search:
            return parent.Evaluation
        ex_util= math.inf
        for s in self.children:
            ex_util= min(ex_util,self.max_value(enough_search,s,alpha,beta))
            if ex_util <= alpha :
                return ex_util
            beta = min(beta, ex_util)
            return ex_util

    #Evaluation function
    def Evaluation(self, state):

        #distance from end
        mybeadDistanceFromEnd= self.CalcuteDistance(state.board)

        #backup
        backup= self.backUp(state.board)
        #is in danger
        danger= self.isinDanger(self.board)

        return danger+ mybeadDistanceFromEnd + backup


    #  CalcuteDistance
    def CalcuteDistance(self, board):
        first_line = 0
        second_line = 0
        rest_line = 0
        for k in range(board.n_rows):
            for c in range(board.n_cols):
                if (k == 0):
                    if (board.board[k][c] == self.color):
                        first_line += 1
                elif (k == 1):
                    if (board.board[k][c] == self.color):
                        second_line += 1
                else:
                    if (board.board[k][c] == self.color):
                        rest_line += 1

        return ((first_line * 5) + (second_line * 3) + rest_line )
    # # isClose
    # def isClose(self, board):
    #     chance=0
    #     for k in range(board.n_rows):
    #         for c in range(board.n_cols):
    #             if(board.board[k][c]== self.color):
    #                 if(board.board[k+1][c] == 'E'):
    #                     chance+=1
    #     return chance*2

    #backup
    def backUp(self, board):
        backup=0
        for k in range(board.n_rows):
            for c in range(board.n_cols):
                if(board.board[k][c]== self.color):
                    if(board.board[k-1][c-1]==self.color or board.board[k-1][c+1]==self.color):
                        backup+=1
        return backup*3
    #danger
    def isinDanger(self, board):
        danger=0
        for k in range(board.n_rows):
            for c in range(board.n_cols):
                if(board.board[k][c]== self.color):
                    if(board.board[k+1][c-1]!=self.color or board.board[k-1][c+1]!=self.color):
                        danger+=1
        return danger*5

    #evalFunctions_End

    def time_is_over(self):
        return self.time is not None and time() >= self.start_time + self.time

    # return best move (from cell, to cell), for example: ((4, 0), (3, 1))
    def move(self):
        self.max_level = 0
        while self.max_level <= MAX_LEVEL and not self.time_is_over():
            self.max_value(self.root, 0)
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
