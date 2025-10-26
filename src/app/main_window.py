# src/app/main_window.py

import sys
from src.app.widgets.editor_widget import CodeEditor
from src.app.widgets.file_tree_widget import FileExplorer
from src.app.widgets.terminal_widget import TerminalWidget
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QSplitter, QFileDialog, QMessageBox
)
from PySide6.QtGui import QIcon, QAction
from PySide6.QtCore import Qt, QEvent

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("nullEditor")
        self.resize(1200, 720) # Define o tamanho inicial
        self.current_file_path = None
        self.is_dirty = False

        # --- MELHORIA: Porcentagens para o layout ---
        # [Editor, FileTree]
        self.top_splitter_percentages = [0.70, 0.30] # 70% para o editor, 30% para a árvore
        # [TopSplitter (Editor/Tree), Terminal]
        self.main_splitter_percentages = [0.75, 0.25] # 75% para a área de cima, 25% para o terminal
        
        # Flag para garantir que o 'showEvent' só configure os tamanhos uma vez
        self._initial_sizes_set = False
        # --- FIM DA MELHORIA ---

        main_splitter = QSplitter(Qt.Orientation.Vertical)
        top_splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Guardamos os splitters como atributos (self.) para acessá-los depois
        self.editor = CodeEditor()
        self.file_tree = FileExplorer()
        self.terminal = TerminalWidget()
        self.top_splitter = top_splitter
        self.main_splitter = main_splitter

        top_splitter.addWidget(self.editor)
        top_splitter.addWidget(self.file_tree)
        # Os tamanhos fixos foram removidos daqui
        
        main_splitter.addWidget(top_splitter)
        main_splitter.addWidget(self.terminal)
        # Os tamanhos fixos foram removidos daqui

        self.setCentralWidget(main_splitter)
        
        self.setup_actions() #
        self.file_tree.file_selected.connect(self.open_file) #
        self.editor.textChanged.connect(self.mark_as_dirty) #
        self.file_tree.folder_opened.connect(self.on_folder_opened) #
        self.center_on_screen() #
        icon_path = "src/resources/icons/app_icon.png" #
        self.setWindowIcon(QIcon(icon_path)) #
    
    # --- NOVO MÉTODO (Função de conversão) ---
    def _apply_splitter_percentages(self):
        """
        Calcula e aplica os tamanhos dos splitters com base 
        nas porcentagens definidas em self.
        """
        
        # 1. Configura o splitter horizontal (Editor / Árvore)
        total_width = self.top_splitter.width()
        sizes_top = [
            int(total_width * self.top_splitter_percentages[0]), # 70% da largura
            int(total_width * self.top_splitter_percentages[1])  # 30% da largura
        ]
        # Garante que o último widget ocupe o espaço restante (evita erros de arredondamento)
        sizes_top[-1] = total_width - sum(sizes_top[:-1])
        self.top_splitter.setSizes(sizes_top)

        # 2. Configura o splitter vertical (Principal / Terminal)
        total_height = self.main_splitter.height()
        sizes_main = [
            int(total_height * self.main_splitter_percentages[0]), # 75% da altura
            int(total_height * self.main_splitter_percentages[1])  # 25% da altura
        ]
        sizes_main[-1] = total_height - sum(sizes_main[:-1])
        self.main_splitter.setSizes(sizes_main)
        
    # --- NOVO MÉTODO (Sobrescrita de QMainWindow) ---
    def showEvent(self, event: QEvent):
        """
        Sobrescreve o evento show para aplicar os tamanhos iniciais
        depois que a janela tiver seu tamanho final.
        """
        # Primeiro, executa o showEvent original
        super().showEvent(event)
        
        # Só executamos isso na PRIMEIRA vez que a janela é exibida
        if not self._initial_sizes_set:
            self._initial_sizes_set = True
            self._apply_splitter_percentages() # Aqui chamamos sua função!

    # --- Métodos movidos do run.py ---

    def on_folder_opened(self, path): #
        if self.terminal:
            self.terminal.set_working_directory(path)
            self.terminal.display.setFocus()

    def setup_actions(self): #
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
        
    def check_unsaved_changes(self): #
        if not self.is_dirty:
            return True
        reply = QMessageBox.question(self, "Alterações não salvas",
                                     "Você tem alterações não salvas. Deseja salvá-las?",
                                     QMessageBox.StandardButton.Save |
                                     QMessageBox.StandardButton.Discard |
                                     QMessageBox.StandardButton.Cancel)
        if reply == QMessageBox.StandardButton.Save:
            return self.save_file()
        elif reply == QMessageBox.StandardButton.Cancel:
            return False
        return True
        
    def closeEvent(self, event): #
        if not self.check_unsaved_changes():
            event.ignore()
        else:
            event.accept()
            
    def mark_as_dirty(self): #
        self.is_dirty = True
        if not self.windowTitle().endswith('*'):
            self.setWindowTitle(self.windowTitle() + '*')
            
    def open_file(self, file_path=None): #
        if not self.check_unsaved_changes():
            return
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
                
    def save_file(self): #
        if self.current_file_path is None:
            return self.save_as()
        else:
            try:
                text = self.editor.toPlainText()
                with open(self.current_file_path, 'w', encoding='utf-8') as f:
                    f.write(text)
                self.is_dirty = False
                self.setWindowTitle(self.windowTitle().replace('*', ''))
                print(f"Arquivo salvo em: {self.current_file_path}")
                return True
            except Exception as e:
                print(f"Erro ao salvar o arquivo: {e}")
                return False
                
    def save_as(self): #
        file_path, _ = QFileDialog.getSaveFileName(self, "Salvar Arquivo Como...", "", "Todos os Arquivos (*.*);;Arquivos de Texto (*.txt)")
        if file_path:
            self.current_file_path = file_path
            self.setWindowTitle(f"nullEditor - {self.current_file_path}")
            return self.save_file()
        return False
        
    def center_on_screen(self): #
        screen_geometry = QApplication.primaryScreen().geometry()
        window_geometry = self.frameGeometry()
        window_geometry.moveCenter(screen_geometry.center())
        self.move(window_geometry.topLeft())