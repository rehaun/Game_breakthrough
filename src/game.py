from src.RandomMinimaxAgent import RandomMinimaxAgent
from src.board import Board
from src.graphicalBoard import GraphicalBoard


def switchTurn(turn):
    if turn == 'W':
        return 'B'
    return 'W'


def play(white, black, board):
    graphicalBoard = GraphicalBoard(board)
    turn = 'W'
    while not board.finishedGame():
        if turn == 'W':
            from_cell, to_cell = white.move(board)
        elif turn == 'B':
            from_cell, to_cell = black.move(board)
        else:
            raise Exception
        board.changePieceLocation(turn, from_cell, to_cell)
        turn = switchTurn(turn)
        graphicalBoard.showBoard()


if __name__ == '__main__':
    board = Board(6, 6, 2)
    white = RandomMinimaxAgent('W', 'B')
    you = RandomMinimaxAgent('B', 'W')     # use your agent
    play(white, you, board)
