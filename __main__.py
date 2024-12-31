from PyQt6.QtWidgets import QApplication
from go import Go
import sys

def main():
    app = QApplication([])
    myGo = Go()
    myGo.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()