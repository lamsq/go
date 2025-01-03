from PyQt6.QtWidgets import QApplication
from go import Go
import sys

def main():
    # Create the application object and show the main window
    app = QApplication([])
    myGo = Go()
    myGo.show()
    sys.exit(app.exec())

if __name__ == "__main__": # Entry point for the script
    main()