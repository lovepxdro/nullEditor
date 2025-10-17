# run.py
import sys
from src.app.widgets.editor_widget import CodeEditor
from src.app.widgets.file_tree_widget import FileExplorer
from PySide6.QtWidgets import QApplication, QMainWindow, QSplitter, QLabel, QFileDialog, QMessageBox
from PySide6.QtGui import QIcon, QAction
from PySide6.QtCore import Qt, QEvent

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # ... (configurações da janela como antes)
        self.setWindowTitle("nullEditor")
        self.resize(1200, 720)
        self.current_file_path = None
        self.is_dirty = False
        main_splitter = QSplitter(Qt.Orientation.Vertical)
        top_splitter = QSplitter(Qt.Orientation.Horizontal)
        self.editor = CodeEditor()
        self.file_tree = FileExplorer()
        dark_panel_style = "border: 1px solid #333;"
        terminal_placeholder = QLabel("Área do Terminal")
        terminal_placeholder.setStyleSheet(dark_panel_style)
        top_splitter.addWidget(self.editor)
        top_splitter.addWidget(self.file_tree)
        top_splitter.setSizes([840, 360])
        main_splitter.addWidget(top_splitter)
        main_splitter.addWidget(terminal_placeholder)
        main_splitter.setSizes([540, 180])
        self.setCentralWidget(main_splitter)
        self.setup_actions()
        self.file_tree.file_selected.connect(self.open_file)
        self.editor.textChanged.connect(self.mark_as_dirty)
        self.center_on_screen()
        icon_path = "src/resources/icons/app_icon.png"
        self.setWindowIcon(QIcon(icon_path))

    def setup_actions(self):
        # ... (este método não muda)
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

    # --- NOVO MÉTODO CENTRAL PARA VERIFICAÇÃO ---
    def check_unsaved_changes(self):
        if not self.is_dirty:
            return True # Continua sem problemas

        reply = QMessageBox.question(self, "Alterações não salvas",
                                     "Você tem alterações não salvas. Deseja salvá-las?",
                                     QMessageBox.StandardButton.Save |
                                     QMessageBox.StandardButton.Discard |
                                     QMessageBox.StandardButton.Cancel)

        if reply == QMessageBox.StandardButton.Save:
            return self.save_file() # Tenta salvar e retorna sucesso/falha do salvamento
        elif reply == QMessageBox.StandardButton.Cancel:
            return False # Interrompe a ação
        
        return True # Continua a ação (usuário escolheu 'Discard')

    # --- MÉTODO ESPECIAL QUE É CHAMADO AO FECHAR A JANELA ---
    def closeEvent(self, event):
        # Se a verificação de segurança falhar (usuário cancelou), ignora o evento de fechar
        if not self.check_unsaved_changes():
            event.ignore()
        else:
            event.accept()

    def mark_as_dirty(self):
        self.is_dirty = True
        if not self.windowTitle().endswith('*'):
            self.setWindowTitle(self.windowTitle() + '*')

    def open_file(self, file_path=None):
        # --- MUDANÇA AQUI: Adiciona a verificação antes de abrir ---
        if not self.check_unsaved_changes():
            return # Interrompe se o usuário cancelou

        if not file_path:
            file_path, _ = QFileDialog.getOpenFileName(self, "Abrir Arquivo", "", "Todos os Arquivos (*.*)")
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                self.editor.setPlainText(content)
                self.current_file_path = file_path
                self.is_dirty = False
                self.setWindowTitle(f"nullEditor - {self.current_file_path}")
            except Exception as e:
                print(f"Erro ao abrir o arquivo: {e}")

    def save_file(self):
        if self.current_file_path is None:
            return self.save_as() # save_as já retorna True/False
        else:
            try:
                text = self.editor.toPlainText()
                with open(self.current_file_path, 'w', encoding='utf-8') as f:
                    f.write(text)
                self.is_dirty = False
                self.setWindowTitle(self.windowTitle().replace('*', ''))
                print(f"Arquivo salvo em: {self.current_file_path}")
                return True # Retorna sucesso
            except Exception as e:
                print(f"Erro ao salvar o arquivo: {e}")
                return False # Retorna falha

    def save_as(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Salvar Arquivo Como...", "", "Todos os Arquivos (*.*);;Arquivos de Texto (*.txt)")
        if file_path:
            self.current_file_path = file_path
            self.setWindowTitle(f"nullEditor - {self.current_file_path}")
            return self.save_file() # Reutiliza a lógica e o retorno de save_file
        return False # Usuário cancelou a caixa de diálogo
    
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