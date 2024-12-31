from PyQt6.QtWidgets import QDockWidget, QVBoxLayout, QWidget, QLabel
from PyQt6.QtCore import pyqtSlot

class ScoreBoard(QDockWidget):
    '''# base the score_board on a QDockWidget'''

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        '''initiates ScoreBoard UI'''
        self.setFixedWidth(130)  #sets width to 130 px
        self.setWindowTitle('ScoreBoard')

        #main widget 
        self.mainWidget = QWidget()
        self.mainLayout = QVBoxLayout()

        #two labels which will be updated by signals
        self.label_clickLocation = QLabel("Click Location: ")
        self.label_timeRemaining = QLabel("Time remaining: ")
        self.label_currentPlayer = QLabel("Current Player: \n1")

        self.mainWidget.setLayout(self.mainLayout)
        self.mainLayout.addWidget(self.label_clickLocation)
        self.mainLayout.addWidget(self.label_timeRemaining)
        self.mainLayout.addWidget(self.label_currentPlayer)
        self.setWidget(self.mainWidget)

        #sets word wrap for labels to ensure text fits within the fixed width
        self.label_clickLocation.setWordWrap(True)
        self.label_timeRemaining.setWordWrap(True)
        self.label_currentPlayer.setWordWrap(True)

    def make_connection(self, board):
        '''this handles a signal sent from the board class'''
        board.clickLocationSignal.connect(self.setClickLocation)
        board.updateTimerSignal.connect(self.setTimeRemaining)
        board.currentPlayerSignal.connect(self.setCurrentPlayer)

    @pyqtSlot(str) 
    def setClickLocation(self, clickLoc):
        '''updates the label to show the click location'''
        self.label_clickLocation.setText("Click Location: \n" + clickLoc)
        print('slot ' + clickLoc)

    @pyqtSlot(int)  
    def setCurrentPlayer(self, currentPlayer):
        '''updates the label to show the current player'''
        self.label_currentPlayer.setText("Current Player: \n" + str(currentPlayer))
        print('slot ' + str(currentPlayer))

    @pyqtSlot(int)
    def setTimeRemaining(self, timeRemaining):
        '''updates the time remaining label to show the time remaining'''
        update = "Time Remaining: " + str(timeRemaining)
        self.label_timeRemaining.setText(update)
        print('slot ' + str(timeRemaining))
        # self.redraw()
