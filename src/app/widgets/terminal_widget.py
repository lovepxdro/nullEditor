# src/app/widgets/terminal_widget.py

import subprocess
from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QLineEdit
from PySide6.QtCore import Qt, QObject, Signal, QThread, QDir

# --- O Worker (CommandRunner) permanece o mesmo ---
class CommandRunner(QObject):
    output_ready = Signal(str)
    finished = Signal()

    def run_command(self, command, working_directory):
        try:
            process = subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding='utf-8',
                errors='replace',
                cwd=working_directory
            )
            for line in iter(process.stdout.readline, ''):
                self.output_ready.emit(line)
            process.stdout.close()
            process.wait()
        except Exception as e:
            self.output_ready.emit(f"Erro ao executar o comando: {e}\n")
        finally:
            self.finished.emit()

class TerminalWidget(QWidget):
    command_to_run = Signal(str, str)

    def __init__(self):
        super().__init__()
        self.working_directory = None

        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)
        self.output_area = QTextEdit()
        self.output_area.setReadOnly(True)
        self.input_line = QLineEdit()
        self.input_line.setPlaceholderText("Abra uma pasta para começar a usar o terminal...")
        
        # --- MUDANÇA 1: Corrigindo o Estilo ---
        # Adicionamos 'QWidget' para garantir que o fundo do widget principal também seja escuro.
        dark_theme_style = """
            QWidget {
                background-color: #1e2227;
            }
            QTextEdit, QLineEdit {
                background-color: #1e2227;
                color: #dcdfe4;
                border: 1px solid #333;
                font-family: 'Courier New', monospace;
                font-size: 13px;
            }
        """
        self.setStyleSheet(dark_theme_style)
        # --- FIM DA MUDANÇA 1 ---

        layout.addWidget(self.output_area)
        layout.addWidget(self.input_line)

        # Desabilita a entrada no início, pois nenhuma pasta está aberta
        self.input_line.setEnabled(False)

        self.thread = QThread()
        self.worker = CommandRunner()
        self.worker.moveToThread(self.thread)
        self.input_line.returnPressed.connect(self.on_command_entered)
        self.command_to_run.connect(self.worker.run_command)
        self.worker.output_ready.connect(self.append_output)
        self.worker.finished.connect(self.on_command_finished)
        self.thread.start()

    def set_working_directory(self, path):
        self.working_directory = path
        self.output_area.clear()
        self.output_area.append(f"Diretório de trabalho: {path}\n")
        # Habilita a entrada e muda o texto de ajuda
        self.input_line.setEnabled(True)
        self.input_line.setPlaceholderText("Digite um comando e pressione Enter...")
        self.input_line.setFocus() # Coloca o foco aqui para o usuário poder digitar

    def on_command_entered(self):
        # --- MUDANÇA 2: Verificação de Segurança ---
        # Não faz nada se nenhuma pasta estiver aberta ou se um comando já estiver rodando
        if not self.working_directory or not self.input_line.isEnabled():
            return

        command = self.input_line.text().strip()
        if command:
            self.input_line.clear()
            self.output_area.append(f"[{self.working_directory}]$ {command}\n") # Estilo de prompt
            self.input_line.setEnabled(False)
            self.command_to_run.emit(command, self.working_directory)

    def append_output(self, text):
        self.output_area.insertPlainText(text)
        self.output_area.verticalScrollBar().setValue(self.output_area.verticalScrollBar().maximum())

    def on_command_finished(self):
        self.input_line.setEnabled(True)
        self.input_line.setFocus()