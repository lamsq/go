from piece import Piece

class GameLogic:

    def __init__(self, board_size=19):
        print("Game Logic Object Created")
        self.board_size = board_size #board size
        self.board = [[Piece.NoPiece for _ in range(board_size)] for _ in range(board_size)] #board
        #initial prisoners
        self.captured_white= 0 
        self.captured_black= 0

    def reset_board(self):
        self.board = [[Piece.NoPiece for _ in range(self.board_size)] for _ in range(self.board_size)] #resets board
        #resets values for prisoners
        self.captured_black = 0
        self.captured_white = 0
        self.black_territory = 0
        self.white_territory = 0

    def is_valid_move(self, row, col, player):
        """checks if place is avaliable"""
        if not (0 <= row < self.board_size and 0 <= col < self.board_size): #checks if position is on board
            return False
        if self.board[row][col] != Piece.NoPiece: #checks if position is already occupied
            return False
        if self.is_suicidal(row, col, player): #check for self-capture
            return False        
        return True
    
    def is_suicidal(self, row, col, player):
        """checks if move is suicidal"""
        self.board[row][col] = player #temp stone
        group, liberties = self.get_group_and_liberties(row, col) #checks liberties
        self.board[row][col] = Piece.NoPiece #removes the temp stone
        return liberties == 0 #suicide of no liberties

    def place_stone(self, row, col, player):
        """
        Places a stone if valid.
        Returns True if move was successful, False otherwise.
        Also calls capture logic if move placed.
        """
        if self.is_valid_move(row, col, player): #checks if move is valid
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
        opponent = Piece.Black if (player == Piece.White) else Piece.White #opponent color
        neighbors = self.get_neighbors(row, col) #get neighbors
        # For each adjacent cell, if it belongs to opponent, check if it’s captured
        captured_stones = 0
        for (nr, nc) in neighbors: #for each neighbor
            if self.board[nr][nc] == opponent: #if neighbor is opponent stone
                group_stones, liberties = self.get_group_and_liberties(nr, nc) #get group and liberties
                if liberties == 0: 
                    # Remove them
                    for (r, c) in group_stones:
                        self.board[r][c] = Piece.NoPiece
                    captured_stones += len(group_stones) #count captured stones
        #update the prisoners count                
        if player == Piece.Black:
            self.captured_white += captured_stones
        else:
            self.captured_black += captured_stones
        # return the captured stones count
        return self.captured_black, self.captured_white

    def get_neighbors(self, row, col):
        neighbors = [] # neighbors around 
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
        if color == Piece.NoPiece: # no stone here
            return set(), 0
        
        stack = [(row, col)]
        visited = set()
        liberties = 0
        #find all stones in the group and count liberties
        while stack:
            r, c = stack.pop()
            if (r, c) in visited:
                continue
            visited.add((r, c)) # mark the stone as visited
            for (nr, nc) in self.get_neighbors(r, c):
                neighbor_color = self.board[nr][nc]
                if neighbor_color == color and (nr, nc) not in visited:
                    stack.append((nr, nc))
                elif neighbor_color == Piece.NoPiece:
                    liberties += 1
        return visited, liberties

    def print_board(self):
        for row in self.board: # print the board as a grid
            print(' '.join(map(str, row)))

    def count_territories(self):
        """counts the number of territories for both players and returns them as a tuple"""
        def flood_fill(row, col, visited): # fill the area with the same color
            if (row, col) in visited or row < 0 or row >= self.board_size or col < 0 or col >= self.board_size:
                return set(), set()            
            if self.board[row][col] != Piece.NoPiece: # no stone here
                return set(), {self.board[row][col]}
            
            visited.add((row, col))
            area = {(row, col)}
            bordering = set()
            
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]: # fill the area with the same color
                new_area, new_bordering = flood_fill(row + dr, col + dc, visited)
                area |= new_area
                bordering |= new_bordering            
            return area, bordering
        # check territories for both players
        black_territory = 0
        white_territory = 0
        visited = set()

        for row in range(self.board_size): # for each cell
            for col in range(self.board_size): # check each cell
                if (row, col) not in visited and self.board[row][col] == Piece.NoPiece: # no stone here
                    area, bordering = flood_fill(row, col, visited)
                    if len(bordering) == 1: 
                        if Piece.Black in bordering and all(self.is_enclosed(r, c, Piece.Black) for r, c in area):
                            black_territory += len(area)
                        elif Piece.White in bordering and all(self.is_enclosed(r, c, Piece.White) for r, c in area):
                            white_territory += len(area)
        return black_territory, white_territory

    def is_enclosed(self, row, col, player):
        """Check if a position is enclosed by a player's stones"""
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]: # check for each direction
            r, c = row + dr, col + dc
            if 0 <= r < self.board_size and 0 <= c < self.board_size:
                if self.board[r][c] == Piece.NoPiece or self.board[r][c] != player: # not player stone or empty cell
                    return False
        return True
    
    def is_game_over(self):
        return not (self.has_valid_moves(Piece.Black) and self.has_valid_moves(Piece.White)) # check if no moves left for both players

    def calculate_winner(self):
        # count territories and prisoners for both players and calculate the winner's score
        black_territory, white_territory = self.count_territories()
        black_score = black_territory + self.captured_white
        white_score = white_territory + self.captured_black
        if black_score > white_score:
            return "Black", black_score, white_score
        elif white_score > black_score:
            return "White", white_score, black_score
        else:
            return "Nobody", black_score, white_score
        
    def has_valid_moves(self, player): # check if there are any valid moves for a player
        for row in range(self.board_size): # for each cell
            for col in range(self.board_size): # check each cell
                if self.is_valid_move(row, col, player): # check if there is a valid move
                    return True
        return False

    