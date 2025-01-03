from PyQt6.QtWidgets import QFrame
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QPoint
from PyQt6.QtGui import QPainter, QColor, QBrush, QPen
from piece import Piece
from game_logic import GameLogic

class Board(QFrame):  
    updateTimerSignal = pyqtSignal(int)  #signal sent for the timer 
    clickLocationSignal = pyqtSignal(str)  #signal sent when there is a new click
    currentPlayerSignal = pyqtSignal(int) #signal for changing player
    prisonersCapturedSignal = pyqtSignal(int, int) #updates prisoners
    territoriesUpdatedSignal = pyqtSignal(int, int) #updates territories
    gameOverSignal = pyqtSignal(str, int, int) #signal for game over    
    currentPlayer = 2 #initial player is black
    cellSize = 40  #size of each cell 
    timerSpeed = 1000  #the timer updates every 1 second
    
    def __init__(self, parent, board_size, timer_value):
        super().__init__(parent)
        # set board size and initialize game logic
        self.boardWidth = board_size
        self.boardHeight = board_size
        # set timer value
        self.game_logic = GameLogic(board_size)
        self.current_player = Piece.Black
        self.current_player = 2
        self.counter = timer_value
        self.initBoard()

        #animation state
        self.stone_animations = [[0 for _ in range(self.boardWidth)] for _ in range(self.boardHeight)]
        
        #animation timer
        self.animation_timer = QTimer(self)
        self.animation_timer.timeout.connect(self.updateAnimations)
        self.animation_timer.start(10)  # updates every 7ms for smooth animation


    def initBoard(self):
        '''initiates board'''
        # initialize timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.timerEvent)
        self.isStarted = False
        self.start()
        # initialize board array
        self.boardArray = [[0 for _ in range(self.boardWidth)] for _ in range(self.boardHeight)]
        self.printBoardArray()
        # sets fixed size
        totalWidth = (self.boardWidth - 1) * self.cellSize + 40  
        totalHeight = (self.boardHeight - 1) * self.cellSize + 40
        self.setFixedSize(totalWidth, totalHeight)

    def printBoardArray(self): # prints the current state of the board array
        print("boardArray:")
        print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in self.boardArray]))

    def mousePosToColRow(self, event):        
        '''converts the mouse click event to a row and column'''
        # gets the position of the mouse click event
        pos = event.position()
        padding = 20
        col = round((pos.x() - padding) / self.cellSize)
        row = round((pos.y() - padding) / self.cellSize)
        return row, col

    def squareWidth(self):
        '''returns the width of one square in the board'''
        return self.cellSize

    def squareHeight(self):
        '''returns the height of one square of the board'''
        return self.cellSize

    def start(self):
        '''starts game'''        
        self.isStarted = True  #sets the start flag to true
        self.resetGame()  #resets the game
        self.timer.start(self.timerSpeed)  #starts the timer with the correct speed
        print("start () - timer is started")

    def timerEvent(self):
        '''automatically called when the timer is updated. based on the timerSpeed variable '''
        if self.counter > 0: # update the timer
            self.counter -= 1
            print('timerEvent()', self.counter)
            self.updateTimerSignal.emit(self.counter)
        else: # game over
            self.timer.stop()
            self.end_game()

    def end_game(self):
        '''Ends the game and calculates the winner'''
        winner, winner_score, loser_score = self.game_logic.calculate_winner() # calculates the winner
        self.gameOverSignal.emit(winner, winner_score, loser_score) # sends game over signal with winner and scores
        #print(f"Game over! Winner: {winner}, Score: {winner_score} to {loser_score}")

    def paintEvent(self, event):
        '''paints the board and the pieces of the game'''
        # creates a painter object and draws the board and pieces
        painter = QPainter(self)
        self.drawBoardSquares(painter)
        self.drawPieces(painter)

    def mousePressEvent(self, event):
        
        # gets the position of the mouse click event
        row, col = self.mousePosToColRow(event)
        if 0 <= row < self.boardHeight and 0 <= col < self.boardWidth: # checks if the click is within the board
            
            # sends click loc signal with the row and col to the game logic
            clickLoc = f"[row: {row}, col: {col}]"
            print("mousePressEvent() - " + clickLoc)
            self.clickLocationSignal.emit(clickLoc)

            #attempts to place
            placed = self.game_logic.place_stone(row,col,self.current_player)

            if placed: # if move was successful

                self.stone_animations[row][col] = 0.1 #start animation
                # sends prisoners captured signal to the game logic
                black_prisoners, white_prisoners = self.game_logic.check_captures(row, col, self.current_player)
                self.prisonersCapturedSignal.emit(black_prisoners, white_prisoners)
                #switches players
                if self.current_player == Piece.Black: #switch players
                    self.current_player = Piece.White
                    currentPlayer = 2
                else:
                    self.current_player = Piece.Black
                    currentPlayer = 1
                # sends territories updated signal to the game logic
                black_territory, white_territory = self.game_logic.count_territories()
                self.territoriesUpdatedSignal.emit(black_territory, white_territory)
                # sends current player signal to the game logic
                if self.game_logic.is_game_over():
                    winner, winner_score, loser_score = self.game_logic.calculate_winner()
                    self.gameOverSignal.emit(winner, winner_score, loser_score)
                elif not self.game_logic.has_valid_moves(self.current_player):
                    #game is over
                    self.switch_player()  #switch to other player if there's np moves
                    if not self.game_logic.has_valid_moves(self.current_player):
                        #game is over
                        winner, winner_score, loser_score = self.game_logic.calculate_winner()
                        self.gameOverSignal.emit(winner, winner_score, loser_score)
                
            else: # invalid move
                #print("Invalid move")
                if self.current_player == Piece.Black:
                    currentPlayer = 1
                else:
                    currentPlayer = 2

            #prints currentPlayer
            self.currentPlayerSignal.emit(currentPlayer)
            self.update()  #triggers repaint

    def tryMove(self, newX, newY):
        '''tries to move a piece'''
        pass  #implement this method according to your logic
        #moved to go file

    def switch_player(self):
        # switches the current player
        self.current_player = Piece.White if self.current_player == Piece.Black else Piece.Black
        self.currentPlayerSignal.emit(self.current_player)

    def drawBoardSquares(self, painter):
        '''draw all the squares on the board with padding around the edges'''
        # sets the color and draws the board squares
        padding = 20
        boardPixelWidth = (self.boardWidth - 1) * self.cellSize
        boardPixelHeight = (self.boardHeight - 1) * self.cellSize
        
        painter.setPen(QPen(Qt.GlobalColor.black, 1))
        for i in range(self.boardWidth): # draw vertical lines
            painter.drawLine(padding + i * self.cellSize, padding,
                            padding + i * self.cellSize, padding + boardPixelHeight)
        for i in range(self.boardHeight): # draw horizontal lines
            painter.drawLine(padding, padding + i * self.cellSize,
                            padding + boardPixelWidth, padding + i * self.cellSize)

    def drawPieces(self, painter):
        '''draw the pieces on the board'''
        padding = 20
        full_radius = self.cellSize // 2 - 2
        # draws the pieces in the board array
        for row in range(self.boardHeight):
            for col in range(self.boardWidth): # draws the piece at the current position
                piece = self.game_logic.board[row][col]
                if piece != Piece.NoPiece: # draws the piece if it exists
                    painter.save()
                    painter.translate(padding + col * self.cellSize, padding + row * self.cellSize)
                    if piece == Piece.Black:  # sets the color of the piece
                        painter.setBrush(QBrush(Qt.GlobalColor.black))
                    elif piece == Piece.White:
                        painter.setBrush(QBrush(Qt.GlobalColor.white))
                    
                    #animation
                    animation_progress = self.stone_animations[row][col]
                    radius = int(full_radius * animation_progress)
                    painter.drawEllipse(-radius, -radius, 2*radius, 2*radius)
                    painter.restore()

    def updateAnimations(self):
        '''Update stone animations'''
        updated = False
        for row in range(self.boardHeight): # update the animation progress for each stone
            for col in range(self.boardWidth): # update the animation till its drawn
                if 0 < self.stone_animations[row][col] < 1:
                    self.stone_animations[row][col] = min(1, self.stone_animations[row][col] + 0.1)
                    updated = True
        if updated: 
            self.update()  #repaint if animation is updated

    def resetGame(self): # resets the game to its initial state
        '''clears pieces from the board'''
        self.boardArray = [[0 for _ in range(self.boardWidth)] for _ in range(self.boardHeight)] # clears the board
        self.clicked_points = []  # clears all placed dots
        self.game_logic.reset_board() # resets game logic
        self.currentPlayerSignal.emit(1) # sets current player black
        self.current_player = Piece.Black 
        self.stone_animations = [[0 for _ in range(self.boardWidth)] for _ in range(self.boardHeight)] # clears animations
        self.counter = self.parent().timer_value  #reset the counter 
        #self.updateTimerSignal.emit(self.counter)
        self.update()  # triggers repaint

        