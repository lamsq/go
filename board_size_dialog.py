from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QRadioButton, QButtonGroup, QLabel
from PyQt6.QtGui import QIcon

class BoardSizeDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Game settings")
        self.board_size = 7  #default
        self.timer_value = 300

        icon = QIcon("./assets/icons/logo.png")
        self.setWindowIcon(icon)

        layout = QVBoxLayout()

        #game settings
        caption = QLabel("Board size:")
        layout.addWidget(caption)

        hbox = QHBoxLayout()

        #game size options
        self.radio_7x7 = QRadioButton("7x7")
        self.radio_13x13 = QRadioButton("13x13")
        self.radio_19x19 = QRadioButton("19x19")

        self.button_group = QButtonGroup()
        self.button_group.addButton(self.radio_7x7)
        self.button_group.addButton(self.radio_13x13)
        self.button_group.addButton(self.radio_19x19)

        self.radio_7x7.setChecked(True)

        #adding radio buttons to layout
        hbox.addWidget(self.radio_7x7)
        hbox.addWidget(self.radio_13x13)
        hbox.addWidget(self.radio_19x19)
        
        layout.addLayout(hbox)

        #timer settings
        timer_caption = QLabel("Timer (seconds):")
        layout.addWidget(timer_caption)

        timer_hbox = QHBoxLayout()

        #timer options
        self.radio_150 = QRadioButton("150")
        self.radio_300 = QRadioButton("300")
        self.radio_600 = QRadioButton("600")

        self.timer_group = QButtonGroup()
        self.timer_group.addButton(self.radio_150)
        self.timer_group.addButton(self.radio_300)
        self.timer_group.addButton(self.radio_600)

        self.radio_300.setChecked(True)

        #adds timer radio buttons 
        timer_hbox.addWidget(self.radio_150)
        timer_hbox.addWidget(self.radio_300)
        timer_hbox.addWidget(self.radio_600)

        layout.addLayout(timer_hbox)

        #ok button
        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.on_ok)
        layout.addWidget(ok_button)

        self.setLayout(layout)

    def on_ok(self):
        if self.radio_7x7.isChecked():
            self.board_size = 7
        elif self.radio_13x13.isChecked():
            self.board_size = 13
        elif self.radio_19x19.isChecked():
            self.board_size = 19

        if self.radio_150.isChecked():
            self.timer_value = 150
        elif self.radio_300.isChecked():
            self.timer_value = 300
        elif self.radio_600.isChecked():
            self.timer_value = 600

        self.accept()

    def get_board_size(self):
        return self.board_size
    
    def get_timer_value(self):
        return self.timer_value