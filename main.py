from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QStyleFactory, QTextEdit, QToolBar, QFileDialog, QLineEdit, QMessageBox
import sys, os, argparse

from PySide6.QtGui import QColor, QTextCharFormat, QFont
from PySide6.QtCore import Qt, QRegularExpression, QTimer

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        parser = argparse.ArgumentParser()
        parser.add_argument("path", nargs="?", default=None)
        args = parser.parse_args()
        self.path = args.path

        self.initUI()
        self.update_path_text()

    def initUI(self):
        self.setWindowTitle("uTextEditor")
        self.setGeometry(0, 0, 500, 600)

        self.layout = QVBoxLayout()

        self.toolbar = QToolBar()
        self.toolbar.addAction("save")
        self.toolbar.actions()[0].setShortcut("Ctrl+S")
        self.toolbar.actions()[0].triggered.connect(self.save)
        self.toolbar.addAction("save as")
        self.toolbar.actions()[1].setShortcut("Ctrl+Shift+S")
        self.toolbar.actions()[1].triggered.connect(self.save_as)
        self.toolbar.addAction("open")
        self.toolbar.actions()[2].setShortcut("Ctrl+O")
        self.toolbar.actions()[2].triggered.connect(self._open)
        self.toolbar.addAction("copy all")
        self.toolbar.actions()[3].triggered.connect(self.copy_all)
        self.toolbar.addAction("paste all")
        self.toolbar.actions()[4].triggered.connect(self.paste_all)
        self.toolbar.addAction("clear")
        self.toolbar.actions()[5].triggered.connect(lambda: self.text_box.clear())
        self.toolbar.addAction("delete")
        self.toolbar.actions()[6].triggered.connect(self.delete_file)
        self.toolbar.addAction("about")
        self.toolbar.actions()[7].triggered.connect(lambda: QMessageBox.information(self, "About", "uTextEditor\n\nA simple Qt text editor."))
        self.layout.addWidget(self.toolbar)

        self.text_box = QTextEdit()
        self.text_box.setAcceptRichText(False)
        self.text_box.setPlaceholderText("Start typing here...")
        self.layout.addWidget(self.text_box)

        self.path_text = QLineEdit()
        self.path_text.returnPressed.connect(self.open_path)
        self.layout.addWidget(self.path_text)

        self.setLayout(self.layout)
        
        if self.path != None:
            with open(self.path, "r") as f:
                self.text_box.setText(f.read())

        self.show()

    def update_path_text(self):
        if self.path == None:
            self.path_text.setPlaceholderText("No file path")
            font = self.path_text.font()
            font.setItalic(True)
            self.path_text.setFont(font)
        else:
            self.path_text.setText(self.path)

    def save(self):
        if self.path == None:
            chosen_path = QFileDialog.getSaveFileName(self, "Save file", "", "Text files (*)")[0]
            if chosen_path != "":
                self.path = chosen_path
            self.update_path_text()
            with open(self.path, "w") as f:
                f.write(self.text_box.toPlainText())
        else:
            with open(self.path, "w") as f:
                f.write(self.text_box.toPlainText())

    def save_as(self):
        chosen_path = QFileDialog.getSaveFileName(self, "Save file", "", "Text files (*)")[0]
        if chosen_path != "":
            self.path = chosen_path
        self.update_path_text()
        with open(self.path, "w") as f:
            f.write(self.text_box.toPlainText())

    def _open(self):
        chosen_path = QFileDialog.getOpenFileName(self, "Open file", "", "Text files (*)")[0]
        if chosen_path != "" and chosen_path != None:
            self.path = chosen_path
            self.update_path_text()
        
            with open(self.path, "r") as f:
                self.text_box.setText(f.read())

    def open_path(self):
        self.path = self.path_text.text()
        self.update_path_text()
        with open(self.path, "r") as f:
            self.text_box.setText(f.read())

    def copy_all(self):
        QApplication.clipboard().setText(self.text_box.toPlainText())

    def paste_all(self):
        self.text_box.setText(QApplication.clipboard().text())

    def delete_file(self):
        if self.path != None and os.path.exists(self.path):
            warning = QMessageBox.warning(self, "Delete file", "Are you sure you want to delete the file?", QMessageBox.Yes | QMessageBox.No)
            if warning == QMessageBox.Yes:
                if self.path != None:
                    os.remove(self.path)
                    self.path = None
                    self.update_path_text()
                    self.text_box.clear()
        else:
            QMessageBox.warning(self, "Delete file", "No file to delete", QMessageBox.Ok)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    app.processEvents()
    sys.exit(app.exec())
