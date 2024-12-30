from piece import Piece

class GameLogic:
    def __init__(self, board_size=19):
        print("Game Logic Object Created")
        self.board_size = board_size
        # Use Piece.NoPiece everywhere for empty cells
        self.board = [[Piece.NoPiece for _ in range(board_size)] for _ in range(board_size)]

    def reset_board(self):
        self.board = [[Piece.NoPiece for _ in range(self.board_size)]
                      for _ in range(self.board_size)]

    def is_valid_move(self, row, col, player):
        """Check if (row, col) is in range and empty."""
        if not (0 <= row < self.board_size and 0 <= col < self.board_size):
            return False
        if self.board[row][col] != Piece.NoPiece:
            return False
        return True

    def place_stone(self, row, col, player):
        """
        Places a stone if valid.
        Returns True if move was successful, False otherwise.
        Also calls capture logic if move placed.
        """
        if self.is_valid_move(row, col, player):
            self.board[row][col] = player
            # Check for captures (optional) if you want real Go capturing
            self.check_captures(row, col, player)
            return True
        return False

    # ----------------------------------------------------------------
    # CAPTURING LOGIC (Optional)
    # ----------------------------------------------------------------
    def check_captures(self, row, col, player):
        """
        After placing a stone at (row, col), look at neighboring positions.
        If an adjacent group is the opponent's color and has 0 liberties,
        remove that group from the board.
        """
        opponent = Piece.Black if (player == Piece.White) else Piece.White
        neighbors = self.get_neighbors(row, col)
        # For each adjacent cell, if it belongs to opponent, check if it’s captured
        for (nr, nc) in neighbors:
            if self.board[nr][nc] == opponent:
                group_stones, liberties = self.get_group_and_liberties(nr, nc)
                if liberties == 0:
                    # Remove them
                    for (r, c) in group_stones:
                        self.board[r][c] = Piece.NoPiece

    def get_neighbors(self, row, col):
        neighbors = []
        if row > 0:
            neighbors.append((row - 1, col))
        if row < self.board_size - 1:
            neighbors.append((row + 1, col))
        if col > 0:
            neighbors.append((row, col - 1))
        if col < self.board_size - 1:
            neighbors.append((row, col + 1))
        return neighbors

    def get_group_and_liberties(self, row, col):
        """
        Return (group_stones, liberty_count) for the group connected to (row, col).
        """
        color = self.board[row][col]
        if color == Piece.NoPiece:
            return set(), 0

        stack = [(row, col)]
        visited = set()
        liberties = 0

        while stack:
            r, c = stack.pop()
            if (r, c) in visited:
                continue
            visited.add((r, c))

            for (nr, nc) in self.get_neighbors(r, c):
                neighbor_color = self.board[nr][nc]
                if neighbor_color == color and (nr, nc) not in visited:
                    stack.append((nr, nc))
                elif neighbor_color == Piece.NoPiece:
                    liberties += 1

        return visited, liberties
    # ----------------------------------------------------------------

    def print_board(self):
        for row in self.board:
            print(' '.join(map(str, row)))
