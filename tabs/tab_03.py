from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout,  QLabel, QLineEdit, QTextEdit, QPushButton, QSpacerItem, QSizePolicy, QFrame, QMessageBox, QTableWidget, QTableWidgetItem, QSlider,QSplitter
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtGui import QPixmap

tareas = ["Alineamiento estrella", "Neighbor Joining"]
from alignment.starAligment import startAligmentFunction


class Tab03(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        layout = QVBoxLayout()

        # Agregar un título
        titulo = QLabel("Alineamiento Múltiple")
        titulo.setFont(QFont("Arial", weight=QFont.Bold, italic=True))
        titulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(titulo,  alignment=Qt.AlignTop)

        # Crear un QTextEdit para insertar las cadenas a tratar
        self.cadenas_text = QTextEdit()
        self.cadenas_text.setReadOnly(False)
        self.cadenas_text.textChanged.connect(self.update_buttons_state)  # Conectar al cambio de texto

        layout.addWidget(self.cadenas_text)


        # Crear un QHBoxLayout para los botones
        boton_layout = QHBoxLayout()
        boton_layout.addStretch()  # Agrega un espacio flexible antes de los botones
        # Botón Reset
        boton_reset = QPushButton("Reset")
        boton_reset.setStyleSheet("background-color: #da1913;")
        boton_reset.clicked.connect(self.reset_cajaCadenasTexto)
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

        # Crear las 2 áreas con líneas verticales entre ellas
        self.area_widgets = []
        for i in range(2):
            area_layout = QVBoxLayout()
            boton_area = QPushButton(tareas[i])
            boton_area.setStyleSheet("background-color: #65f51d;")

            area_layout.addWidget(boton_area)
            if i == 0:
                boton_area.clicked.connect(self.funcion_para_primer_boton_AlineamientoEstrella)
            elif i == 1:
                boton_area.clicked.connect(self.funcion_para_segundo_boton)

            # Configurar el área
            area_widget = QWidget()
            area_widget.setLayout(area_layout)
            self.area_widgets.append(area_widget)

            # Agregar un stretch factor para que todas las áreas ocupen el mismo tamaño
            self.areas_layout.addWidget(area_widget)
            self.areas_layout.setStretch(self.areas_layout.count() - 1, 1)

            # Agregar una línea vertical entre áreas
            if i < 1:
                line = QFrame()
                line.setFrameShape(QFrame.VLine)
                line.setFrameShadow(QFrame.Sunken)
                line.setLineWidth(2)
                line.setStyleSheet("background-color: #65f51d;")
                self.areas_layout.addWidget(line)

        # Agregar el QHBoxLayout al layout principal
        layout.addLayout(self.areas_layout)



        self.setLayout(layout)
        # Actualizar el estado de los botones inicialmente
        self.update_buttons_state()


    def funcion_para_primer_boton_AlineamientoEstrella(self):
        texto_completo = self.cadenas_text.toPlainText()
        #QMessageBox.information(self, 'primer boton', '¡Funcion para el primer boton!')
        lineas = texto_completo.splitlines()
        #print(lineas)
        #print(len(lineas))
        #print(type(lineas)) # <class, 'list'>

        startAligmentFunction(lineas)

    def funcion_para_segundo_boton(self):
        QMessageBox.information(self, 'segundo boton', '¡Funcion para el segundo boton!')

    def reset_cajaCadenasTexto(self):
        self.cadenas_text.clear()

    def update_buttons_state(self):
        caja1 = self.cadenas_text.toPlainText()
        # Activar o desactivar los botones
        state = bool(caja1)
        #print("state: ", state)
        for widget in self.area_widgets:
            for child in widget.findChildren(QPushButton):
                child.setEnabled(state)
