from PySide6.QtWidgets import QWidget, QVBoxLayout,QPushButton

class Tab03(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        layout = QVBoxLayout()
        layout.addWidget(QPushButton("Botón en la pestaña 03"))
        self.setLayout(layout)
