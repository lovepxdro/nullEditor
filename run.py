import sys
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *
# alterar apenas para os imports necessarios

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("nullEditor")
        self.resize(1200, 720)
        self.center_on_screen()

        main_splitter = QSplitter(Qt.Orientation.Vertical)
        top_splitter = QSplitter(Qt.Orientation.Horizontal)
        panel_style = "border: 1px solid #333;"
        
        editor_placeholder = QLabel("Área do Editor")
        editor_placeholder.setStyleSheet(panel_style)

        file_tree_placeholder = QLabel("Área da Árvore de Arquivos")
        file_tree_placeholder.setStyleSheet(panel_style)
        
        terminal_placeholder = QLabel("Área do Terminal")
        terminal_placeholder.setStyleSheet(panel_style)

        top_splitter.addWidget(editor_placeholder)
        top_splitter.addWidget(file_tree_placeholder)
        top_splitter.setSizes([840, 360])

        main_splitter.addWidget(top_splitter)
        main_splitter.addWidget(terminal_placeholder)
        main_splitter.setSizes([540, 180])

        self.setCentralWidget(main_splitter)

        icon_path = "src/resources/icons/app_icon.png"
        self.setWindowIcon(QIcon(icon_path))

    def center_on_screen(self):
        screen_geometry = QApplication.primaryScreen().geometry()
        window_geometry = self.frameGeometry()
        window_geometry.moveCenter(screen_geometry.center())
        self.move(window_geometry.topLeft())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()

    window.show()

    sys.exit(app.exec())