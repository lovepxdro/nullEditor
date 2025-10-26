# run.py
import sys
from PySide6.QtWidgets import QApplication
from src.app.main_window import MainWindow  # Importa a classe do novo arquivo

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())