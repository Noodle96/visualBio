from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QSpacerItem, QSizePolicy, QFrame
from PySide6.QtCore import Qt
from alignment.sequence_alignment import solve

tareas = ["Matriz de Punto", "Alineamiento Global", "Alineamiento Local", "Alineamiento Proteinas"]

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
        self.caja_texto1.textChanged.connect(self.update_buttons_state)  # Conectar al cambio de texto
        layout.addWidget(self.caja_texto1, alignment=Qt.AlignTop)

        self.caja_texto2 = QLineEdit()
        self.caja_texto2.setPlaceholderText("Cadena 02")
        self.caja_texto2.textChanged.connect(self.update_buttons_state)  # Conectar al cambio de texto
        layout.addWidget(self.caja_texto2, alignment=Qt.AlignTop)

        # Crear un QHBoxLayout para los botones
        boton_layout = QHBoxLayout()
        boton_layout.addStretch()  # Agrega un espacio flexible antes de los botones

        # Botón Alinear
        #boton_alinear = QPushButton("Alinear")
        #boton_alinear.clicked.connect(self.Needleman)
        #boton_layout.addWidget(boton_alinear)

        # Botón Reset
        boton_reset = QPushButton("Reset")
        boton_reset.clicked.connect(self.reset_texts)
        boton_layout.addWidget(boton_reset)

        # Agregar el QHBoxLayout al layout principal
        layout.addLayout(boton_layout)
        # Agregar un espaciador vertical para empujar la línea horizontal más abajo
        layout.addItem(QSpacerItem(0, 20, QSizePolicy.Minimum, QSizePolicy.Fixed))


        # Agregar una línea horizontal verde
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setLineWidth(5)
        line.setStyleSheet("background-color: #65f51d;")
        layout.addWidget(line)


        # Crear un QHBoxLayout para las áreas con botones
        self.areas_layout = QHBoxLayout()

        # Crear las 4 áreas con líneas verticales entre ellas
        # Crear las 4 áreas con líneas verticales entre ellas
        self.area_widgets = []
        for i in range(4):
            area_layout = QVBoxLayout()
            if i == 1:  # Segunda área
                # Agregar un botón y una caja de texto en la segunda área
                area_layout.addWidget(QPushButton(tareas[i]))
                caja_texto = QLineEdit()
                caja_texto.setPlaceholderText(f"Texto {i+1}")
                area_layout.addWidget(caja_texto)
            else:
                # Agregar solo un botón en las otras áreas
                area_layout.addWidget(QPushButton(tareas[i]))

            # Configurar el área
            area_widget = QWidget()
            area_widget.setLayout(area_layout)
            self.area_widgets.append(area_widget)

            # Agregar un stretch factor para que todas las áreas ocupen el mismo tamaño
            self.areas_layout.addWidget(area_widget)
            self.areas_layout.setStretch(self.areas_layout.count() - 1, 1)

            # Agregar una línea vertical entre áreas
            if i < 3:
                line = QFrame()
                line.setFrameShape(QFrame.VLine)
                line.setFrameShadow(QFrame.Sunken)
                line.setLineWidth(2)
                line.setStyleSheet("background-color: #65f51d;")
                self.areas_layout.addWidget(line)

        # Agregar el QHBoxLayout al layout principal
        layout.addLayout(self.areas_layout)


        # Agregar un espaciador para empujar los widgets hacia arriba
        layout.addItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.setLayout(layout)
        # Actualizar el estado de los botones inicialmente
        self.update_buttons_state()

    def Needleman(self):
        texto1 = self.caja_texto1.text()
        texto2 = self.caja_texto2.text()
        print(f"Texto 1: {texto1}")
        print(f"Texto 2: {texto2}")
        # Llamar a la función solve con los textos obtenidos
        dp, cantidadCadenas, alineacionesTotales = solve(texto1, texto2)
        print(f"Resultado de solve:\nDP Matrix: {dp}\nCantidad de Cadenas: {cantidadCadenas}\nAlineaciones Totales: {alineacionesTotales}")

    def reset_texts(self):
        self.caja_texto1.clear()
        self.caja_texto2.clear()

    def update_buttons_state(self):
        texto1 = self.caja_texto1.text()
        texto2 = self.caja_texto2.text()
        # Activar o desactivar los botones dependiendo de si las cajas de texto están vacías
        state = bool(texto1 and texto2)
        for widget in self.area_widgets:
            for child in widget.findChildren(QPushButton):
                child.setEnabled(state)
            for child in widget.findChildren(QLineEdit):
                child.setEnabled(state)


