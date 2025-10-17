# run.py
import sys
from src.app.widgets.editor_widget import CodeEditor
from PySide6.QtWidgets import QApplication, QMainWindow, QSplitter, QLabel, QFileDialog
from PySide6.QtGui import QIcon, QAction
from PySide6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("nullEditor")
        self.resize(1200, 720)
        self.current_file_path = None

        main_splitter = QSplitter(Qt.Orientation.Vertical)
        top_splitter = QSplitter(Qt.Orientation.Horizontal)
        
        self.editor = CodeEditor()

        dark_panel_style = "border: 1px solid #333;"
        
        file_tree_placeholder = QLabel("Área da Árvore de Arquivos")
        file_tree_placeholder.setStyleSheet(dark_panel_style)
        
        terminal_placeholder = QLabel("Área do Terminal")
        terminal_placeholder.setStyleSheet(dark_panel_style)

        top_splitter.addWidget(self.editor)
        top_splitter.addWidget(file_tree_placeholder)
        top_splitter.setSizes([840, 360])
        main_splitter.addWidget(top_splitter)
        main_splitter.addWidget(terminal_placeholder)
        main_splitter.setSizes([540, 180])
        self.setCentralWidget(main_splitter)
        
        self.setup_actions()

        self.center_on_screen()
        icon_path = "src/resources/icons/app_icon.png"
        self.setWindowIcon(QIcon(icon_path))

    def setup_actions(self):
        open_action = QAction("Abrir", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.open_file)
        self.addAction(open_action)

        save_action = QAction("Salvar", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.save_file)
        self.addAction(save_action)

        save_as_action = QAction("Salvar como...", self)
        save_as_action.setShortcut("Ctrl+Shift+S")
        save_as_action.triggered.connect(self.save_as)
        self.addAction(save_as_action)

    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Abrir Arquivo", "", "Todos os Arquivos (*.*)")
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                self.editor.setPlainText(content)
                self.current_file_path = file_path
                self.setWindowTitle(f"nullEditor - {self.current_file_path}")
            except Exception as e:
                print(f"Erro ao abrir o arquivo: {e}")

    def save_file(self):
        if self.current_file_path is None:
            self.save_as()
        else:
            try:
                text = self.editor.toPlainText()
                with open(self.current_file_path, 'w', encoding='utf-8') as f:
                    f.write(text)
                print(f"Arquivo salvo em: {self.current_file_path}")
            except Exception as e:
                print(f"Erro ao salvar o arquivo: {e}")

    def save_as(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Salvar Arquivo Como...", "", "Todos os Arquivos (*.*);;Arquivos de Texto (*.txt)")
        if file_path:
            self.current_file_path = file_path
            self.save_file()
            self.setWindowTitle(f"nullEditor - {self.current_file_path}")
    
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