# src/app/widgets/editor_widget.py

from PySide6.QtWidgets import QPlainTextEdit, QWidget, QTextEdit
from PySide6.QtCore import Qt, QRect, QSize
from PySide6.QtGui import QPainter, QColor, QTextFormat

class LineNumberWidget(QWidget):
    def __init__(self, editor, settings):
        super().__init__(editor)
        self.editor = editor
        self.settings = settings 

    def sizeHint(self):
        return QSize(self.editor.lineNumberAreaWidth(), 0)

    def paintEvent(self, event):
        self.editor.lineNumberAreaPaintEvent(event)

class CodeEditor(QPlainTextEdit):
    def __init__(self, settings):
        super().__init__()
        self.settings = settings
        
        # --- REFATORADO ---
        # Pega a string CSS inteira diretamente do JSON
        editor_settings = self.settings.get('editor', {})
        style_sheet = editor_settings.get('style_sheet', '') # Pega o CSS
        self.setStyleSheet(style_sheet)
        # --- FIM DA REFATORAÇÃO ---

        self.line_number_widget = LineNumberWidget(self, self.settings)
        
        self.blockCountChanged.connect(self.updateLineNumberAreaWidth)
        self.updateRequest.connect(self.updateLineNumberArea)
        self.cursorPositionChanged.connect(self.highlightCurrentLine)
        self.updateLineNumberAreaWidth(0)
        self.highlightCurrentLine()

    def highlightCurrentLine(self):
        extra_selections = []
        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()
            
            # --- CORRETO: Isto NÃO é CSS, é um valor de cor para QColor ---
            highlight_color_str = self.settings.get('editor', {}).get('current_line_highlight', '#3e4451')
            line_color = QColor(highlight_color_str)
            # --- FIM ---
            
            selection.format.setBackground(line_color)
            selection.format.setProperty(QTextFormat.Property.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extra_selections.append(selection)
        self.setExtraSelections(extra_selections)

    def updateLineNumberAreaWidth(self, _):
        self.setViewportMargins(self.lineNumberAreaWidth(), 0, 0, 0)

    def updateLineNumberArea(self, rect, dy):
        if dy:
            self.line_number_widget.scroll(0, dy)
        else:
            self.line_number_widget.update(0, rect.y(), self.line_number_widget.width(), rect.height())
        if rect.contains(self.viewport().rect()):
            self.updateLineNumberAreaWidth(0)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.line_number_widget.setGeometry(QRect(cr.left(), cr.top(), self.lineNumberAreaWidth(), cr.height()))

    def lineNumberAreaWidth(self):
        digits = 1
        count = max(1, self.blockCount())
        while count >= 10:
            count //= 10
            digits += 1
        space = 10 + self.fontMetrics().horizontalAdvance('9') * digits
        return space

    def lineNumberAreaPaintEvent(self, event):
        painter = QPainter(self.line_number_widget)
        
        block = self.firstVisibleBlock()
        block_number = block.blockNumber()
        top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        bottom = top + self.blockBoundingRect(block).height()

        # --- CORRETO: Isto NÃO é CSS, é um valor de cor para QPainter ---
        line_number_color_str = self.settings.get('editor', {}).get('line_number_color', '#636d83')
        # --- FIM ---
        
        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(block_number + 1)
                painter.setPen(QColor(line_number_color_str))
                painter.drawText(0, int(top), self.line_number_widget.width() - 5,
                                 self.fontMetrics().height(),
                                 Qt.AlignmentFlag.AlignRight, number)
            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            block_number += 1