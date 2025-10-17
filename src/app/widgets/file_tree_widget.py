# src/app/widgets/file_tree_widget.py

# Mudança 1: Importar os módulos e widgets necessários
import os
import shutil
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QTreeView, 
                               QFileSystemModel, QStackedWidget, QFileDialog, 
                               QMenu, QInputDialog, QMessageBox)
from PySide6.QtCore import QDir, Signal, Qt
from PySide6.QtGui import QAction

class TreeView(QTreeView):
    def __init__(self):
        super().__init__()
        self.setColumnHidden(1, True)
        self.setColumnHidden(2, True)
        self.setColumnHidden(3, True)
        self.setHeaderHidden(True)
        self.setStyleSheet("background-color: transparent; color: #abb2bf; border: none;")

class FileExplorer(QWidget):
    file_selected = Signal(str)

    def __init__(self):
        super().__init__()
        self.stacked_widget = QStackedWidget()
        
        # ... (welcome_screen e tree_view_screen continuam iguais)
        self.welcome_screen = QWidget()
        welcome_layout = QVBoxLayout(self.welcome_screen)
        open_folder_button = QPushButton("Abrir Pasta")
        open_folder_button.clicked.connect(self.open_folder_dialog)
        welcome_layout.addWidget(open_folder_button)
        welcome_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.tree_view_screen = QWidget()
        tree_view_layout = QVBoxLayout(self.tree_view_screen)
        tree_view_layout.setContentsMargins(0, 5, 0, 0)
        tree_view_layout.setSpacing(5)
        change_folder_button = QPushButton("Trocar Pasta")
        change_folder_button.clicked.connect(self.open_folder_dialog)
        self.tree_view = TreeView()
        self.model = QFileSystemModel()
        self.model.setFilter(QDir.Filter.AllEntries | QDir.Filter.NoDotAndDotDot | QDir.Filter.Hidden)
        self.tree_view.setModel(self.model)
        self.tree_view.doubleClicked.connect(self.on_item_double_clicked)
        tree_view_layout.addWidget(change_folder_button)
        tree_view_layout.addWidget(self.tree_view)
        self.stacked_widget.addWidget(self.welcome_screen)
        self.stacked_widget.addWidget(self.tree_view_screen)
        self.stacked_widget.setCurrentWidget(self.welcome_screen)
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self.stacked_widget)

        # --- MUDANÇA 2: Habilitar e conectar o menu de contexto ---
        self.tree_view.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.tree_view.customContextMenuRequested.connect(self.show_context_menu)

    # --- MUDANÇA 3: Todos os novos métodos para as funcionalidades ---
    def show_context_menu(self, position):
        index = self.tree_view.indexAt(position)
        path = self.model.filePath(index) if index.isValid() else self.model.rootPath()

        menu = QMenu()
        new_file_action = menu.addAction("Novo Arquivo")
        new_folder_action = menu.addAction("Nova Pasta")
        menu.addSeparator()
        rename_action = menu.addAction("Renomear")
        delete_action = menu.addAction("Deletar")

        # Desabilita ações que não fazem sentido se não houver um item selecionado
        if not index.isValid():
            rename_action.setEnabled(False)
            delete_action.setEnabled(False)

        # Executa o menu e captura a ação escolhida pelo usuário
        action = menu.exec(self.tree_view.viewport().mapToGlobal(position))

        # Chama a função correspondente à ação escolhida
        if action == new_file_action:
            self.new_file(path)
        elif action == new_folder_action:
            self.new_folder(path)
        elif action == rename_action:
            self.rename_item(path)
        elif action == delete_action:
            self.delete_item(path)

    def new_file(self, base_path):
        # Se o caminho base é um arquivo, usa o diretório pai
        if os.path.isfile(base_path):
            base_path = os.path.dirname(base_path)
        
        file_name, ok = QInputDialog.getText(self, "Novo Arquivo", "Nome do arquivo:")
        if ok and file_name:
            file_path = os.path.join(base_path, file_name)
            try:
                open(file_path, 'a').close() # Cria um arquivo vazio
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Não foi possível criar o arquivo:\n{e}")

    def new_folder(self, base_path):
        if os.path.isfile(base_path):
            base_path = os.path.dirname(base_path)

        folder_name, ok = QInputDialog.getText(self, "Nova Pasta", "Nome da pasta:")
        if ok and folder_name:
            folder_path = os.path.join(base_path, folder_name)
            try:
                os.makedirs(folder_path)
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Não foi possível criar a pasta:\n{e}")
                
    def rename_item(self, old_path):
        old_name = os.path.basename(old_path)
        new_name, ok = QInputDialog.getText(self, "Renomear", "Novo nome:", text=old_name)
        if ok and new_name and new_name != old_name:
            new_path = os.path.join(os.path.dirname(old_path), new_name)
            try:
                os.rename(old_path, new_path)
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Não foi possível renomear:\n{e}")

    def delete_item(self, path):
        item_name = os.path.basename(path)
        reply = QMessageBox.question(self, "Deletar", f"Tem certeza que deseja deletar '{item_name}'?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                     QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            try:
                if os.path.isfile(path):
                    os.remove(path)
                elif os.path.isdir(path):
                    shutil.rmtree(path) # shutil.rmtree deleta pastas com conteúdo
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Não foi possível deletar:\n{e}")

    def open_folder_dialog(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Selecione uma Pasta", QDir.homePath())
        if folder_path:
            self.model.setRootPath(folder_path)
            self.tree_view.setRootIndex(self.model.index(folder_path))
            self.tree_view.setColumnHidden(1, True)
            self.tree_view.setColumnHidden(2, True)
            self.tree_view.setColumnHidden(3, True)
            self.stacked_widget.setCurrentWidget(self.tree_view_screen)
    
    def on_item_double_clicked(self, index):
        path = self.model.filePath(index)
        if self.model.fileInfo(index).isFile():
            self.file_selected.emit(path)