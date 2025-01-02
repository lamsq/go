from PyQt6.QtWidgets import QDockWidget, QVBoxLayout, QWidget, QLabel, QPushButton
from PyQt6.QtCore import pyqtSlot, pyqtSignal
from PyQt6.QtGui import QFont

class ScoreBoard(QDockWidget):
    '''# base the score_board on a QDockWidget'''
    passClicked = pyqtSignal()
    switchPlayerSignal = pyqtSignal()

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

        bold_font = QFont()
        bold_font.setBold(True)
        bold_font.setPointSize(int(bold_font.pointSize() * 1.2))  #20% bigger

        #two labels which will be updated by signals
        self.label_clickLocation = QLabel("Click Location: ")
        self.label_timeRemaining = QLabel("Time remaining: ")
        label_current = QLabel("Current Player:")
        label_current.setFont(bold_font)
        self.label_currentPlayer = QLabel("Black")

        label_white = QLabel("White stats:")
        label_white.setFont(bold_font)
        self.label_white_terr = QLabel("Territory: 0")
        self.label_white_prisoners = QLabel("Prisoners: 0")
        label_black = QLabel("Black stats:")
        label_black.setFont(bold_font)
        self.label_black_terr = QLabel("Territory: 0")
        self.label_black_prisoners = QLabel("Prisoners: 0")
        self.pass_button = QPushButton("Pass")
        self.pass_button.clicked.connect(self.on_pass_clicked)

        self.mainWidget.setLayout(self.mainLayout)
        self.mainLayout.addWidget(self.label_clickLocation)
        self.mainLayout.addWidget(self.label_timeRemaining)
        self.mainLayout.addWidget(label_current)
        self.mainLayout.addWidget(self.label_currentPlayer)
        self.mainLayout.addWidget(label_white)
        self.mainLayout.addWidget(self.label_white_terr)
        self.mainLayout.addWidget(self.label_white_prisoners)
        self.mainLayout.addWidget(label_black)
        self.mainLayout.addWidget(self.label_black_terr)
        self.mainLayout.addWidget(self.label_black_prisoners)
        self.mainLayout.addWidget(self.pass_button) 
        self.setWidget(self.mainWidget)

        #sets word wrap for labels to ensure text fits within the fixed width
        self.label_clickLocation.setWordWrap(True)
        self.label_timeRemaining.setWordWrap(True)
        self.label_currentPlayer.setWordWrap(True)
        self.label_white_terr.setWordWrap(True)
        self.label_black_terr.setWordWrap(True)
        self.label_white_prisoners.setWordWrap(True)
        self.label_black_prisoners.setWordWrap(True)

    def make_connection_board(self, board):
        '''handles a signal from the board class'''
        board.clickLocationSignal.connect(self.setClickLocation)
        board.updateTimerSignal.connect(self.setTimeRemaining)
        board.currentPlayerSignal.connect(self.setCurrentPlayer)
        board.prisonersCapturedSignal.connect(self.updatePrisoners)
        board.territoriesUpdatedSignal.connect(self.updateTerritories)

    def updateTerritories(self, black_territory, white_territory):
        self.label_black_terr.setText(f"Territory: {black_territory}")
        self.label_white_terr.setText(f"Territory: {white_territory}")

    @pyqtSlot(int, int)
    def updatePrisoners(self, black_prisoners, white_prisoners):
        '''updates the prisoners labels'''
        self.label_black_prisoners.setText(f"Prisoners: {white_prisoners}")
        self.label_white_prisoners.setText(f"Prisoners: {black_prisoners}")


    @pyqtSlot(str) 
    def setClickLocation(self, clickLoc):
        '''updates the label to show the click location'''
        self.label_clickLocation.setText("Click Location: \n" + clickLoc)
        print('slot ' + clickLoc)

    @pyqtSlot(int)  
    def setCurrentPlayer(self, currentPlayer):
        '''updates the label to show the current player'''
        if currentPlayer == 2:
            p="White"
        else:
            p="Black"
        self.label_currentPlayer.setText(str(p))
        print('slot ' + str(currentPlayer))

    @pyqtSlot(int)
    def setTimeRemaining(self, timeRemaining):
        '''updates the time remaining label to show the time remaining'''
        update = "Time Remaining: " + str(timeRemaining)
        self.label_timeRemaining.setText(update)
        print('slot ' + str(timeRemaining))
        # self.redraw()

    def on_pass_clicked(self):
        print("Pass button clicked")
        self.passClicked.emit()  
        self.switchPlayerSignal.emit()
        self.switch_current_player()
        
    def switch_current_player(self):
        current = self.label_currentPlayer.text()
        new_player = "White" if current == "Black" else "Black"
        self.setCurrentPlayer(1 if new_player == "Black" else 2)

    def reset_score(self):
        #resets variables
        self.setClickLocation("")
        self.setTimeRemaining(0)
        self.updatePrisoners(0, 0)
        self.label_black_terr.setText("Territory: 0")  
        self.label_white_terr.setText("Territory: 0")
