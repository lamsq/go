class GameLogic:
    def __init__(self):
        print("Game Logic Object Created")
        self.board_size = 19
        self.board = [[0 for _ in range(self.board_size)] for _ in range(self.board_size)]

    def reset_board(self):
        self.board = [[0 for _ in range(self.board_size)] for _ in range(self.board_size)]

    def is_valid_move(self, row, col, player):
        if 0 <= row < self.board_size and 0 <= col < self.board_size and self.board[row][col] == 0:
            self.board[row][col] = player
            return True
        return False

    def print_board(self):
        for row in self.board:
            print(' '.join(map(str, row)))