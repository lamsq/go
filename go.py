from PyQt6.QtWidgets import QApplication, QMainWindow, QDockWidget
from PyQt6.QtCore import Qt
from board import Board
from score_board import ScoreBoard
from board_size_dialog import BoardSizeDialog
from board import Board

class Go(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        '''initiates application UI'''
        #shows board size dialog
        dialog = BoardSizeDialog(self)
        if dialog.exec():
            board_size = dialog.get_board_size()
        else:
            board_size = 7  #default size 

        self.board = Board(self, board_size)
        self.setCentralWidget(self.board)

        self.scoreBoard = ScoreBoard()
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.scoreBoard)
        self.scoreBoard.make_connection(self.board)

        self.adjustSize()
        self.center()
        self.setWindowTitle('Go')
        self.show()

    def getBoard(self):
        return self.board
    
    def getScoreBoard(self):
        return self.scoreBoard

    def center(self):
        '''centers the window on the screen'''
        screen = QApplication.primaryScreen().availableGeometry()
        size = self.geometry()
        x = (screen.width() - size.width()) // 2
        y = (screen.height() - size.height()) // 2
        self.move(x, y)





