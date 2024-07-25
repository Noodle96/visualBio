import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QMessageBox

class MiVentana(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Ejemplo de PySide6')
        self.setGeometry(100, 100, 300, 200)

        layout = QVBoxLayout()

        self.boton = QPushButton('Presióname', self)
        self.boton.clicked.connect(self.mostrarMensaje)

        layout.addWidget(self.boton)
        self.setLayout(layout)

    def mostrarMensaje(self):
        QMessageBox.information(self, 'Mensaje', '¡Hola, PySide6!')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = MiVentana()
    ventana.show()
    sys.exit(app.exec())
