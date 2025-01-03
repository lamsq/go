from PyQt6.QtWidgets import QApplication, QTextBrowser, QMainWindow, QDockWidget, QMenuBar, QMenu, QMessageBox, QToolBar, QDialog, QVBoxLayout, QPushButton
from PyQt6.QtCore import Qt, QUrl, QTimer
from PyQt6.QtGui import QIcon, QAction
from board import Board
from score_board import ScoreBoard
from board_size_dialog import BoardSizeDialog
import os
import sys


class Go(QMainWindow):

    def __init__(self):
        super().__init__()
        # initialize board size and board/scoreboard instances
        self.board_size = None
        self.board = None
        self.scoreBoard = None
        # setup game
        self.initUI()
        icon = QIcon("./assets/icons/logo.png")
        self.setWindowIcon(icon)

    def initUI(self):
        '''initiates application UI'''
        # create main window widgets
        self.create_menu_bar()
        self.create_toolbar()
        # create main window layout
        if self.show_board_size_dialog():
            self.setup_game()
        else:
            sys.exit()

    def create_toolbar(self):
        # create toolbar with reset and settings actions
        toolbar = QToolBar()
        self.addToolBar(toolbar)
        # create reset action with shortcut and connects to reset_game method
        reset_icon = QIcon("./assets/icons/toolbar/reset.png")
        reset_action = QAction(reset_icon, 'Reset', self)
        reset_action.setShortcut("Ctrl+R")
        reset_action.triggered.connect(self.reset_game)
        toolbar.addAction(reset_action)
        
        # create settings action with shortcut and connects to open_settings method
        settings_icon = QIcon("./assets/icons/toolbar/settings.png")
        settings_action = QAction(settings_icon, "Settings", self)
        settings_action.setShortcut("Ctrl+S")
        settings_action.triggered.connect(self.open_settings)
        toolbar.addAction(settings_action)

    def reset_game(self):
        if self.board: # clear board if it exists
            self.board.resetGame()
        if hasattr(self.board, 'game_logic'): # clear scoreboard if it exists
            self.board.game_logic.current_player = 1  #sets current player to 1
        if self.scoreBoard: # clear scoreboard if it exists
            self.scoreBoard.reset_score()  
        #print("Game has been reset")

    def show_board_size_dialog(self):
        dialog = BoardSizeDialog(self) # create board size dialog instance
        if dialog.exec(): # if user clicks ok
            self.board_size = dialog.get_board_size()
            self.timer_value = dialog.get_timer_value()
            return True
        return False

    def getBoard(self):
        return self.board
    
    def getScoreBoard(self):
        return self.scoreBoard

    def center(self):
        '''centers the window on the screen'''
        screen = QApplication.primaryScreen().availableGeometry() # get screen geometry
        # calculate window position to center on the screen according to window size and position in the screen
        size = self.geometry()
        x = (screen.width() - size.width()) // 2
        y = (screen.height() - size.height()) // 2
        self.move(x, y)

    def setup_game(self):
        # clear previous board and scoreboard if they exist
        if self.board:
            self.board.setParent(None)
        if self.scoreBoard:
            self.scoreBoard.setParent(None)
        # create new board and scoreboard with given board size and timer value
        self.board = Board(self, self.board_size, self.timer_value)
        self.setCentralWidget(self.board)
        # create new scoreboard and add it to the right dock widget area
        self.scoreBoard = ScoreBoard()
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.scoreBoard)
        self.scoreBoard.make_connection_board(self.board)
        # connect signals and slots
        self.scoreBoard.switchPlayerSignal.connect(self.board.switch_player)
        self.board.gameOverSignal.connect(self.show_game_over_dialog)
        # adjust window size and center it
        self.adjustSize()
        self.center()
        self.setWindowTitle('Go')        
        QTimer.singleShot(50, self.center) # center the window after a short delay 

    def show_game_over_dialog(self, winner, winner_score, loser_score):
        # create game over dialog with winner, winner score, loser score, and buttons to restart or exit the game
        dialog = QMessageBox(self)
        dialog.setWindowTitle("Game Over")
        dialog.setText(f"<div style='text-align: center;'><b>{winner} won!</b><br>{winner} score: {winner_score}<br>Opponent score: {loser_score}</div>")
        # create buttons for restart and exit
        restart_button = QPushButton("Restart")
        exit_button = QPushButton("Exit")
        # connect buttons to methods
        dialog.addButton(restart_button, QMessageBox.ButtonRole.AcceptRole)
        dialog.addButton(exit_button, QMessageBox.ButtonRole.RejectRole)
        # show dialog and handle user choice
        result = dialog.exec()
        if result == QMessageBox.ButtonRole.AcceptRole:
            self.reset_game()
        else:
            self.close()

    def create_menu_bar(self):
        # create menu bar and add game and about menus
        self.menuBar().clear()
        menubar = self.menuBar()

        #game menu
        game_menu = menubar.addMenu('Game')
        #quit suboption
        quit_icon = QIcon("./assets/icons/menubar/game/exit.png")
        quit_action = game_menu.addAction(quit_icon,'Quit')
        quit_action.triggered.connect(self.close)
        quit_action.setShortcut("Ctrl+Q")

        #about menu
        about_menu = menubar.addMenu('About')
        #rues suboption
        rules_icon = QIcon("./assets/icons/menubar/about/rules.png")
        rules_action = about_menu.addAction(rules_icon, 'Rules')
        rules_action.triggered.connect(self.show_rules)
        rules_action.setShortcut("Ctrl+H")
        # about suboption
        about_icon = QIcon("./assets/icons/menubar/about/about.png")
        about_action = about_menu.addAction(about_icon, 'About')
        about_action.triggered.connect(self.show_about)
        about_action.setShortcut("Ctrl+A")

    def open_settings(self):
        # create settings dialog with board size and timer values
        if self.show_board_size_dialog():
            self.setup_game()
            QTimer.singleShot(50, self.center)
            
    def show(self):
        # show main window only if board size has been set
        if self.board_size is not None:
            super().show()
            return True
        return False

    def show_html_content(self, title, file_path): #funct to show text files as html content
        try:
            with open(file_path, 'r', encoding='utf-8') as file: # read the file content as html content
                html_content = file.read()
            # create dialog with html content and a button to close it
            dialog = QDialog(self)
            dialog.setWindowTitle(title)
            layout = QVBoxLayout()
            # create a text browser widget to display the html content 
            browser = QTextBrowser()
            browser.setOpenExternalLinks(True)
            browser.setHtml(html_content)
            # set the search paths to enable opening links in the default web browser 
            url = QUrl.fromLocalFile(os.path.dirname(file_path) + '/')
            browser.setSearchPaths([url.toString()])
            layout.addWidget(browser)
            button = QPushButton('Ok')
            button.clicked.connect(dialog.close)
            layout.addWidget(button)
            # set dialog layout and show it
            dialog.setLayout(layout)
            dialog.resize(700, 500) 
            dialog.exec()

        except FileNotFoundError:
            QMessageBox.warning(self, 'File Not Found', f"The file could not be found at {file_path}")
        except Exception as e:
            QMessageBox.critical(self, 'Error', f"An error occurred while reading the file: {str(e)}")

    def show_rules(self):
        # show rules in dialog as html from a text file 
        rules_path = os.path.join("./assets/rules.txt")
        self.show_html_content('Go Rules', rules_path)

    def show_about(self):
        # show about in dialog as html from a text file 
        about_path = os.path.join("./assets/about.txt")
        self.show_html_content('About Go', about_path)



