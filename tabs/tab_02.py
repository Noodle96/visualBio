from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QSpacerItem, QSizePolicy
from PySide6.QtCore import Qt
from alignment.sequence_alignment import solve

class Tab02(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        layout = QVBoxLayout()

        # Agregar un título
        titulo = QLabel("Alineamiento Global")
        layout.addWidget(titulo,  alignment=Qt.AlignTop)

        # Agregar dos cajas de texto
        self.caja_texto1 = QLineEdit()
        self.caja_texto1.setPlaceholderText("Cadena 01")
        layout.addWidget(self.caja_texto1, alignment=Qt.AlignTop)

        self.caja_texto2 = QLineEdit()
        self.caja_texto2.setPlaceholderText("Cadena 02")
        layout.addWidget(self.caja_texto2, alignment=Qt.AlignTop)

        # Crear un QHBoxLayout para el botón y alinearlo a la derecha
        boton_layout = QHBoxLayout()
        boton_layout.addStretch()  # Agrega un espacio flexible antes del botón
        boton = QPushButton("Alinear")
        boton.clicked.connect(self.Needleman)
        boton_layout.addWidget(boton, alignment=Qt.AlignRight)

        # Agregar el QHBoxLayout al layout principal
        layout.addLayout(boton_layout)

        # Agregar un espaciador para empujar los widgets hacia arriba
        layout.addItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.setLayout(layout)

    def Needleman(self):
        texto1 = self.caja_texto1.text()
        texto2 = self.caja_texto2.text()
        print(f"Texto 1: {texto1}")
        print(f"Texto 2: {texto2}")
        # Llamar a la función solve con los textos obtenidos
        dp, cantidadCadenas, alineacionesTotales = solve(texto1, texto2)
        print(f"Resultado de solve:\nDP Matrix: {dp}\nCantidad de Cadenas: {cantidadCadenas}\nAlineaciones Totales: {alineacionesTotales}")


