import sys
from src.app.widgets.editor_widget import CodeEditor
from PySide6.QtWidgets import QApplication, QMainWindow, QSplitter, QLabel
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("nullEditor")
        self.resize(1200, 720)

        main_splitter = QSplitter(Qt.Orientation.Vertical)
        top_splitter = QSplitter(Qt.Orientation.Horizontal)
        panel_style = "border: 1px solid #333;"
        
        self.editor = CodeEditor()
        self.editor.setStyleSheet(panel_style + "font-family: 'Courier New', monospace; font-size: 14px;")

        file_tree_placeholder = QLabel("Área da Árvore de Arquivos")
        file_tree_placeholder.setStyleSheet(panel_style)
        
        terminal_placeholder = QLabel("Área do Terminal")
        terminal_placeholder.setStyleSheet(panel_style)

        top_splitter.addWidget(self.editor)
        top_splitter.addWidget(file_tree_placeholder)
        top_splitter.setSizes([840, 360])

        main_splitter.addWidget(top_splitter)
        main_splitter.addWidget(terminal_placeholder)
        main_splitter.setSizes([540, 180])

        self.setCentralWidget(main_splitter)

        self.center_on_screen()
        
        icon_path = "src/resources/icons/app_icon.png"
        self.setWindowIcon(QIcon(icon_path))


    def center_on_screen(self):
        screen_geometry = self.screen().geometry()
        window_geometry = self.frameGeometry()
        window_geometry.moveCenter(screen_geometry.center())
        self.move(window_geometry.topLeft())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())