from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout,  QLabel, QLineEdit, QTextEdit, QPushButton, QSpacerItem, QSizePolicy, QFrame, QMessageBox, QTableWidget, QTableWidgetItem, QSlider
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtGui import QPixmap

from alignment.sequence_alignment import solve
import matplotlib.pyplot as plt
import numpy as np
import os
import tempfile

tareas = ["Matriz de Punto", "Alineamiento Global", "Alineamiento Local", "Alineamiento Proteinas"]


def generar_dot_plot(seq1, seq2):
    """Genera un dot plot para dos secuencias con etiquetas en los ejes."""
    matrix = np.zeros((len(seq1), len(seq2)))

    # Rellenar la matriz con coincidencias
    for i in range(len(seq1)):
        for j in range(len(seq2)):
            if seq1[i] == seq2[j]:
                matrix[i][j] = 1

    fig, ax = plt.subplots(figsize=(10, 10))

    # Dibujar la matriz de puntos con color azul
    cmap = plt.cm.colors.ListedColormap(['white', 'blue'])
    ax.imshow(matrix, cmap=cmap, aspect='auto', origin='upper')

    # Dibujar los puntos
    for i in range(len(seq1)):
        for j in range(len(seq2)):
            if matrix[i][j] == 1:
                ax.plot(j, i, 'ko')  # punto negro

    # Configurar las etiquetas de los ejes
    ax.set_xticks(range(len(seq2)))
    ax.set_xticklabels(seq2)
    ax.set_yticks(range(len(seq1)))
    ax.set_yticklabels(seq1)

    # Ajustar la cuadrícula
    ax.grid(True, which='both', color='black', linestyle='-', linewidth=1)
    ax.set_xticks(np.arange(-.5, len(seq2), 1), minor=True)
    ax.set_yticks(np.arange(-.5, len(seq1), 1), minor=True)
    ax.grid(which='minor', color='black', linestyle='-', linewidth=1)

    return fig


class VentanaDotPlot_matrizPuntos(QWidget):
    def __init__(self, seq1, seq2, parent=None):
        super().__init__(parent)
        self.seq1 = seq1
        self.seq2 = seq2
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        titulo = QLabel("Matriz de Puntos")
        titulo.setFont(QFont("Arial", weight=QFont.Bold, italic=True))
        titulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(titulo)

        fig = generar_dot_plot(self.seq1, self.seq2)

        temp_dir = tempfile.TemporaryDirectory()
        temp_path = os.path.join(temp_dir.name, "dot_plot.png")
        fig.savefig(temp_path)
        plt.close(fig)

        pixmap = QPixmap(temp_path)

        label = QLabel(self)
        label.setPixmap(pixmap)
        layout.addWidget(label)

        self.setLayout(layout)
        self.setWindowTitle("Dot Plot")
        self.resize(800, 800)
        self.temp_dir = temp_dir  # Guardar la referencia para evitar que se borre

    def closeEvent(self, event):
        self.temp_dir.cleanup()
        super().closeEvent(event)


class VentanaAlineacionesTotalesTexto(QWidget):
    def __init__(self, alineaciones_totales, parent=None):
        super().__init__(parent)
        self.alineaciones_totales = alineaciones_totales
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        titulo = QLabel("Alineaciones Totales")
        titulo.setFont(QFont("Arial", weight=QFont.Bold, italic=True))
        titulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(titulo)

        # Crear un QTextEdit para mostrar las alineaciones totales
        alineaciones_text = QTextEdit()
        alineaciones_text.setReadOnly(True)

        # Agregar las alineaciones totales al QTextEdit
        alineaciones_formateadas = []
        for i, alineacion in enumerate(self.alineaciones_totales):
            alineaciones_formateadas.append(f"Alineación {i + 1}:\n{alineacion[0]}\n{alineacion[1]}\n")
        alineaciones_text.setText("\n".join(alineaciones_formateadas))
        layout.addWidget(alineaciones_text)

        self.setLayout(layout)
        self.setWindowTitle("Alineaciones Totales")
        self.resize(400, 300)

class VentanaAlineacionesTotalesGrafica(QWidget):
    def __init__(self, alineaciones_totales, parent=None):
        super().__init__(parent)
        self.alineaciones_totales = alineaciones_totales
        self.temp_dir = tempfile.TemporaryDirectory()
        self.image_paths = []
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        titulo = QLabel("Alineaciones Totales")
        titulo.setFont(QFont("Arial", weight=QFont.Bold, italic=True))
        titulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(titulo)

        # Crear QLabel para mostrar el número de la alineación
        self.alineacion_label = QLabel(self)
        self.alineacion_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.alineacion_label)


        # Crear QLabel para mostrar la imagen de la alineación
        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

        # Crear QSlider para navegar entre las imágenes de las alineaciones
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(len(self.alineaciones_totales) - 1)
        self.slider.valueChanged.connect(self.update_image)
        layout.addWidget(self.slider)

        self.setLayout(layout)
        self.setWindowTitle("Alineaciones Totales")
        self.resize(1000, 400)

        self.generate_images()
        self.update_image(0)

    def generate_images(self):
        for index, (seq1, seq2) in enumerate(self.alineaciones_totales):
            fig, ax = plt.subplots(figsize=(10, 2))
            ax.set_axis_off()

            for i, (base1, base2) in enumerate(zip(seq1, seq2)):
                ax.text(i, 1, base1, ha='center', va='center', fontsize=14, color='blue')
                ax.text(i, 0, base2, ha='center', va='center', fontsize=14, color='green')
                if base1 == base2:
                    ax.annotate('', xy=(i, 0.8), xytext=(i, 0.2),
                                arrowprops=dict(facecolor='red', shrink=0.05, width=2, headwidth=8))
                elif base1 == '-' or base2 == '-':
                    ax.annotate('', xy=(i, 0.8), xytext=(i, 0.2),
                                arrowprops=dict(facecolor='black', shrink=0.05, width=1, headwidth=5, linestyle='--'))
                else:
                    ax.annotate('', xy=(i, 0.8), xytext=(i, 0.2),
                                arrowprops=dict(facecolor='gray', shrink=0.05, width=1, headwidth=5, linestyle='-.'))

            ax.set_xlim(-0.5, len(seq1) - 0.5)
            ax.set_ylim(-0.5, 1.5)

            temp_path = os.path.join(self.temp_dir.name, f"alignment_{index + 1}.png")
            fig.savefig(temp_path)
            plt.close(fig)
            self.image_paths.append(temp_path)

    def update_image(self, index):
        pixmap = QPixmap(self.image_paths[index])
        self.label.setPixmap(pixmap)
        self.alineacion_label.setText(f"Alineación {index + 1}")

    def closeEvent(self, event):
        self.temp_dir.cleanup()
        super().closeEvent(event)





class VentanaAlineacion(QWidget):
    def __init__(self, dp_matrix, cantidad_cadenas, alineaciones_totales, parent=None):
        super().__init__(parent)
        self.dp_matrix = dp_matrix
        self.cantidad_cadenas = cantidad_cadenas
        self.alineaciones_totales = alineaciones_totales
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Agregar título "Matriz generada"
        titulo_matriz = QLabel("Matriz generada")
        titulo_matriz.setFont(QFont("Arial", weight=QFont.Bold, italic=True))
        titulo_matriz.setAlignment(Qt.AlignCenter)
        layout.addWidget(titulo_matriz)

        # Crear la tabla para mostrar la matriz dp
        self.table = QTableWidget(len(self.dp_matrix), len(self.dp_matrix[0]))
        for i in range(len(self.dp_matrix)):
            for j in range(len(self.dp_matrix[i])):
                self.table.setItem(i, j, QTableWidgetItem(str(self.dp_matrix[i][j])))
        layout.addWidget(self.table)

        # Mostrar la cantidad de alineaciones generadas
        label_cantidad = QLabel(f"Cantidad de alineaciones generadas: {self.cantidad_cadenas}")
        label_cantidad.setFont(QFont("Arial", weight=QFont.Bold, italic=True))
        label_cantidad.setAlignment(Qt.AlignCenter)
        layout.addWidget(label_cantidad)

        # Crear un QHBoxLayout para los botones
        botones_layout = QHBoxLayout()

        # Crear el botón para mostrar alineaciones
        boton_mostrar_alineaciones = QPushButton("Mostrar Alineaciones texto")
        boton_mostrar_alineaciones.setStyleSheet("background-color: #0767e3;")
        boton_mostrar_alineaciones.clicked.connect(self.mostrar_alineacionesTexto)
        botones_layout.addWidget(boton_mostrar_alineaciones)

        # Crear el botón para mostrar alineaciones gráficas
        boton_mostrar_graficas = QPushButton("Mostrar Alineaciones Gráfica")
        boton_mostrar_graficas.setStyleSheet("background-color: #65f51d;")
        boton_mostrar_graficas.clicked.connect(self.mostrar_alineacionesGrafica)
        botones_layout.addWidget(boton_mostrar_graficas)

        layout.addLayout(botones_layout)

        self.setLayout(layout)
        self.setWindowTitle("Ventana de Alineación")
        self.resize(1200, 800)

    def mostrar_alineacionesGrafica(self):
        self.ventana_alineaciones_totales_grafica = VentanaAlineacionesTotalesGrafica(self.alineaciones_totales)
        self.ventana_alineaciones_totales_grafica.show()

    def mostrar_alineacionesTexto(self):
        self.ventana_alineaciones_totales_texto = VentanaAlineacionesTotalesTexto(self.alineaciones_totales)
        self.ventana_alineaciones_totales_texto.show()

class Tab02(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        layout = QVBoxLayout()

        # Agregar un título
        titulo = QLabel("Alineamiento Global")
        titulo.setFont(QFont("Arial", weight=QFont.Bold, italic=True))
        titulo.setAlignment(Qt.AlignCenter)
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
        boton_reset.setStyleSheet("background-color: #da1913;")
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
        self.area_widgets = []
        for i in range(4):
            area_layout = QVBoxLayout()
            boton_area = QPushButton(tareas[i])
            boton_area.setStyleSheet("background-color: #65f51d;")

            if i == 1:  # Segunda área
                boton_area.clicked.connect(self.funcion_para_segundo_boton_needleman)
                area_layout.addWidget(boton_area)

                label_penalizacion = QLabel("Penalizacion")
                area_layout.addWidget(label_penalizacion)

                self.caja_texto_penalizacion = QLineEdit()
                self.caja_texto_penalizacion.setPlaceholderText("Penalizacion default -2")
                area_layout.addWidget(self.caja_texto_penalizacion)
            else:
                if i == 0:
                    boton_area.clicked.connect(self.funcion_para_primer_boton)
                elif i == 2:
                    boton_area.clicked.connect(self.funcion_para_tercer_boton)
                elif i == 3:
                    boton_area.clicked.connect(self.funcion_para_cuarto_boton)
                area_layout.addWidget(boton_area)

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


    def reset_texts(self):
        self.caja_texto1.clear()
        self.caja_texto2.clear()
        self.caja_texto_penalizacion.clear()

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

    ##  FUNCIONES PARA LOS BOTONES
    ## FUNCION PARA EL PRIMER BOTON DE MATRIZ DE PUNTOS
    def funcion_para_primer_boton(self):
        texto1 = self.caja_texto1.text()
        texto2 = self.caja_texto2.text()
        self.ventana_dot_plot = VentanaDotPlot_matrizPuntos(texto1, texto2)
        self.ventana_dot_plot.show()


    ## FUNCION PARA EL SEGUNDO BOTON DE ALINEAMIENTO GLOBAL
    def funcion_para_segundo_boton_needleman(self):
        texto1 = self.caja_texto1.text()
        texto2 = self.caja_texto2.text()
        penalizacion = self.caja_texto_penalizacion.text()
        #print(f"Texto 1: {texto1}")
        #print(f"Texto 2: {texto2}")
        # Llamar a la función solve con los textos obtenidos
        if not penalizacion:
            penalizacion = 2
            print("penalizacion: ", penalizacion)
        else:
            penalizacion = int(penalizacion)
            print("penalizacion: ", penalizacion)
        dp, cantidadCadenas, alineacionesTotales = solve(texto1, texto2, penalizacion)
        print(f"Resultado de solve:\nDP Matrix: {dp}\nCantidad de Cadenas: {cantidadCadenas}\nAlineaciones Totales: {alineacionesTotales}")

        # Crear y mostrar la nueva ventana con la matriz dp
        self.matriz_alineacion = VentanaAlineacion(dp,cantidadCadenas,alineacionesTotales)
        self.matriz_alineacion.show()

    ## FUNCION PARA EL TERCER BOTON
    def funcion_para_tercer_boton(self):
        QMessageBox.information(self, 'Tercer boton', '¡Funcion para el tercer boton!')

    ## FUNCION PARA EL CUARTO BOTON
    def funcion_para_cuarto_boton(self):
        QMessageBox.information(self, 'Cuarto boton', '¡Funcion para el cuarto boton!')

