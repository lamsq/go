from PyQt6.QtWidgets import QApplication, QMainWindow, QDockWidget, QMenuBar, QMenu, QMessageBox
from PyQt6.QtCore import Qt
from board import Board
from score_board import ScoreBoard
from board_size_dialog import BoardSizeDialog
import os

class Go(QMainWindow):

    def __init__(self):
        super().__init__()
        self.board_size = None
        self.board = None
        self.scoreBoard = None
        self.initUI()

    def initUI(self):
        '''initiates application UI'''
        self.create_menu_bar()
        if self.show_board_size_dialog():
            self.setup_game()
        else:
            self.close()

    def show_board_size_dialog(self):
        dialog = BoardSizeDialog(self)
        if dialog.exec():
            self.board_size = dialog.get_board_size()
            return True
        return False

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

    def setup_game(self):
        if self.board:
            self.board.setParent(None)
        if self.scoreBoard:
            self.scoreBoard.setParent(None)

        self.board = Board(self, self.board_size)
        self.setCentralWidget(self.board)

        self.scoreBoard = ScoreBoard()
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.scoreBoard)
        self.scoreBoard.make_connection(self.board)

        self.adjustSize()
        self.center()
        self.setWindowTitle('Go')

    def create_menu_bar(self):
        self.menuBar().clear()
        menubar = self.menuBar()

        #game menu
        game_menu = menubar.addMenu('Game')
        
        settings_action = game_menu.addAction('Settings')
        settings_action.triggered.connect(self.open_settings)
        
        quit_action = game_menu.addAction('Quit')
        quit_action.triggered.connect(self.close)

        #about menu
        about_menu = menubar.addMenu('About')
        
        rules_action = about_menu.addAction('Rules')
        rules_action.triggered.connect(self.show_rules)
        
        about_action = about_menu.addAction('About')
        about_action.triggered.connect(self.show_about)

    def open_settings(self):
        if self.show_board_size_dialog():
            self.setup_game()

    def show(self):
        if self.board_size is not None:
            super().show()
            return True
        return False

    def show_rules(self):
        rules_path = os.path.join(os.path.dirname(__file__), 'assets', 'rules.txt')
        try:
            with open(rules_path, 'r') as file:
                rules_text = file.read()
            QMessageBox.information(self, 'Go Rules', rules_text)
        except FileNotFoundError:
            QMessageBox.warning(self, 'File Not Found', f"The rules file could not be found at {rules_path}")
        except Exception as e:
            QMessageBox.critical(self, 'Error', f"An error occurred while reading the rules file: {str(e)}")

    def show_about(self):
        about_path = os.path.join(os.path.dirname(__file__), 'assets', 'about.txt')
        try:
            with open(about_path, 'r') as file:
                about_text = file.read()
            QMessageBox.information(self, 'About Go', about_text)
        except FileNotFoundError:
            QMessageBox.warning(self, 'File Not Found', f"The about file could not be found at {about_path}")
        except Exception as e:
            QMessageBox.critical(self, 'Error', f"An error occurred while reading the about file: {str(e)}")





