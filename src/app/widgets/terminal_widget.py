# src/app/widgets/terminal_widget.py

import sys
import os
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPlainTextEdit
from PySide6.QtCore import QProcess, Qt, QDir
from PySide6.QtGui import QTextCursor, QKeyEvent, QMouseEvent, QKeySequence, QColor, QTextOption

class TerminalDisplay(QPlainTextEdit):
    # --- MODIFICADO: Aceita 'settings' ---
    def __init__(self, process: QProcess, settings, parent=None):
        super().__init__(parent)
        self.process = process
        self.settings = settings
    # --- FIM DA MODIFICAÇÃO ---
        
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setUndoRedoEnabled(False)
        self.setWordWrapMode(QTextOption.WrapMode.NoWrap)
        
        self.prompt = ""
        self.prompt_position = 0

        # --- REFATORADO: Carrega CSS do JSON ---
        # O estilo fixo foi removido
        term_settings = self.settings.get('terminal', {})
        style_sheet = term_settings.get('style_sheet', '') # Pega o CSS
        self.setStyleSheet(style_sheet)
        # --- FIM DA REFATORAÇÃO ---

    def _insert_prompt(self):
        self.moveCursor(QTextCursor.MoveOperation.End)
        self.prompt_position = self.textCursor().position()

    def mousePressEvent(self, event: QMouseEvent):
        super().mousePressEvent(event)
        self.setFocus()
    
    def keyPressEvent(self, event: QKeyEvent):
        cursor = self.textCursor()

        if cursor.position() < self.prompt_position:
            cursor.setPosition(self.document().characterCount() - 1)
            self.setTextCursor(cursor)

        key = event.key()

        if key in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            line_block = self.document().lastBlock()
            line = line_block.text()
            
            command = self.toPlainText()[self.prompt_position:].strip()
            
            self.appendPlainText("")
            
            if command.lower() == "cls" or command.lower() == "clear":
                self.clear()
            elif command:
                self.process.write((command + os.linesep).encode())
            else:
                self.process.write(os.linesep.encode())
                
            return

        if key == Qt.Key.Key_Backspace:
            if cursor.position() > self.prompt_position:
                super().keyPressEvent(event)
            return
        
        if event.matches(QKeySequence.StandardKey.Copy):
            self.process.write(b"\x03")
            return

        super().keyPressEvent(event)

class TerminalWidget(QWidget):
    # --- MODIFICADO: Aceita 'settings' ---
    def __init__(self, settings):
        super().__init__()
        self.settings = settings # Guarda as configurações
    # --- FIM DA MODIFICAÇÃO ---
        
        self.process = QProcess()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # --- MODIFICADO: Passa 'settings' para o TerminalDisplay ---
        self.display = TerminalDisplay(self.process, self.settings)
        # --- FIM DA MODIFICAÇÃO ---
        
        layout.addWidget(self.display)

        self.process.setProcessChannelMode(QProcess.ProcessChannelMode.MergedChannels)
        self.process.readyReadStandardOutput.connect(self.read_output)
        self.process.finished.connect(self.process_finished)
        self.process.errorOccurred.connect(self.process_error)

        self.start_shell()

    #
    # O restante do arquivo (start_shell, set_working_directory, etc.)
    # não precisa de configurações de estilo e permanece idêntico.
    #

    def start_shell(self):
        self.display.clear()

        if sys.platform == "win32":
            shell_program = "cmd.exe"
        else:
            shell_program = os.environ.get("SHELL", "/bin/bash")

        self.process.setProgram(shell_program)
        self.process.setWorkingDirectory(QDir.homePath())
        self.process.start()
        self.display.setFocus()

    def set_working_directory(self, path):
        if self.process.state() != QProcess.ProcessState.Running:
            return

        command = f'cd /d "{path}"{os.linesep}' if sys.platform == "win32" else f'cd "{path}"{os.linesep}'
        self.process.write(command.encode())
        
        self.display.clear()
        self.process.write(os.linesep.encode())

    def read_output(self):
        output = str(self.process.readAllStandardOutput(), sys.getdefaultencoding(), 'replace')
        self.display.moveCursor(QTextCursor.MoveOperation.End)
        self.display.insertPlainText(output)
        self.display.moveCursor(QTextCursor.MoveOperation.End)
        self.display.prompt_position = self.display.textCursor().position()

    def process_finished(self):
        self.display.appendPlainText("\n[PROCESSO DO TERMINAL ENCERRADO, REINICIANDO...]")
        self.start_shell()

    def process_error(self, error):
        self.display.appendPlainText(f"\n[ERRO NO PROCESSO: {error}]")

    def closeEvent(self, event):
        if self.process.state() == QProcess.ProcessState.Running:
            self.process.kill()
        super().closeEvent(event)