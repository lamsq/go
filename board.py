from PyQt6.QtWidgets import QFrame
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QPoint
from PyQt6.QtGui import QPainter, QColor, QBrush, QPen
from piece import Piece
from game_logic import GameLogic

class Board(QFrame):  
    updateTimerSignal = pyqtSignal(int)  #signal sent for the timer 
    clickLocationSignal = pyqtSignal(str)  #signal sent when there is a new click
    currentPlayerSignal = pyqtSignal(int) #signal for changing player
    currentPlayer = 1

    cellSize = 40  #size of each cell 
    timerSpeed = 1000  #the timer updates every 1 second
    counter = 10  #the start number for the counter

    def __init__(self, parent, board_size):
        super().__init__(parent)
        self.boardWidth = board_size
        self.boardHeight = board_size

        self.game_logic = GameLogic(board_size)
        self.current_player = Piece.Black
        self.current_player = 1
        self.initBoard()

    def initBoard(self):
        '''initiates board'''
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.timerEvent)
        self.isStarted = False
        self.start()

        self.boardArray = [[0 for _ in range(self.boardWidth)] for _ in range(self.boardHeight)]
        self.printBoardArray()

        # sets fixed size
        totalWidth = (self.boardWidth - 1) * self.cellSize + 40  
        totalHeight = (self.boardHeight - 1) * self.cellSize + 40
        self.setFixedSize(totalWidth, totalHeight)

    def printBoardArray(self):
        print("boardArray:")
        print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in self.boardArray]))

    def mousePosToColRow(self, event):
        
        '''converts the mouse click event to a row and column'''
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
        # TODO adapt this code to handle your timers
        if Board.counter == 0:
            print("Game over")
        self.counter -= 1
        print('timerEvent()', self.counter)
        self.updateTimerSignal.emit(self.counter)

    def paintEvent(self, event):
        '''paints the board and the pieces of the game'''
        painter = QPainter(self)
        self.drawBoardSquares(painter)
        self.drawPieces(painter)

    def mousePressEvent(self, event):
        row, col = self.mousePosToColRow(event)
        if 0 <= row < self.boardHeight and 0 <= col < self.boardWidth:

            clickLoc = f"[row: {row}, col: {col}]"
            print("mousePressEvent() - " + clickLoc)
            self.clickLocationSignal.emit(clickLoc)

            # Attempt to place via game_logic
            placed = self.game_logic.place_stone(row,col,self.current_player)
            if placed:
                #if stone placed, switch players
                if self.current_player == Piece.Black:
                    self.current_player = Piece.White
                    currentPlayer = 2
                else:
                    self.current_player = Piece.Black
                    currentPlayer = 1

            #print("Current Player: ", currentPlayer)
            self.currentPlayerSignal.emit(currentPlayer)
            self.update()  #triggers repaint

    def resetGame(self):
        '''clears pieces from the board'''
        self.game_logic.reset_board()
        self.update()  #triggers repaint


    def tryMove(self, newX, newY):
        '''tries to move a piece'''
        pass  #implement this method according to your logic

    def drawBoardSquares(self, painter):
        '''draw all the squares on the board with padding around the edges'''

        padding = 20
        boardPixelWidth = (self.boardWidth - 1) * self.cellSize
        boardPixelHeight = (self.boardHeight - 1) * self.cellSize

        painter.setPen(QPen(Qt.GlobalColor.black, 1))
        for i in range(self.boardWidth):
            painter.drawLine(padding + i * self.cellSize, padding,
                            padding + i * self.cellSize, padding + boardPixelHeight)
        for i in range(self.boardHeight):
            painter.drawLine(padding, padding + i * self.cellSize,
                            padding + boardPixelWidth, padding + i * self.cellSize)

    def drawPieces(self, painter):
        '''draw the pieces on the board'''
        padding = 20
        radius = self.cellSize // 2 - 2

        for row in range(self.boardHeight):
            for col in range(self.boardWidth):
                piece = self.game_logic.board[row][col]
                if piece != Piece.NoPiece:
                    painter.save()
                    painter.translate(padding + col * self.cellSize, padding + row * self.cellSize)
                    if piece == Piece.Black:
                        painter.setBrush(QBrush(Qt.GlobalColor.black))
                    elif piece == Piece.White:
                        painter.setBrush(QBrush(Qt.GlobalColor.white))
                    painter.drawEllipse(-radius, -radius, 2*radius, 2*radius)
                    painter.restore()

    def resetGame(self):
        '''clears pieces from the board'''
        self.boardArray = [[0 for _ in range(self.boardWidth)] for _ in range(self.boardHeight)]
        self.clicked_points = []  # clears all placed dots
        if hasattr(self, 'game_logic'):
            self.game_logic.reset_board()
        self.update()  # triggers repaint

    def switch_player(self):
            self.current_player = 3-self.current_player  #switches between 1 and 2 players
            self.currentPlayerSignal.emit(self.current_player)
            print(f"Current player switched to {self.current_player}")