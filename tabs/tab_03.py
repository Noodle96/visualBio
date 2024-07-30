from PySide6.QtWidgets import QPlainTextEdit, QWidget, QVBoxLayout, QHBoxLayout,  QLabel, QLineEdit, QTextEdit, QPushButton, QSpacerItem, QSizePolicy, QFrame, QMessageBox, QTableWidget, QTableWidgetItem, QSlider, QSplitter, QMainWindow, QTabWidget
from PySide6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsTextItem
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtGui import QPixmap
from PySide6.QtGui import QIcon
from PySide6.QtGui import QColor

import tempfile
import networkx as nx
import matplotlib.pyplot as plt
import os


tareas = ["Alineamiento estrella", "Neighbor Joining"]
from alignment.starAligment import startAligmentFunction

class AlineacionesTableWidget(QWidget):
    def __init__(self, multiple_alignment_representation, parent=None):
        super().__init__(parent)
        self.multiple_alignment_representation = multiple_alignment_representation
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        num_filas = len(self.multiple_alignment_representation)
        num_columnas = len(self.multiple_alignment_representation[0]) + 1

        self.table_widget = QTableWidget(num_filas, num_columnas)
        self.table_widget.setHorizontalHeaderLabels([""] + [str(i) for i in range(1, num_columnas)])
        self.table_widget.verticalHeader().setVisible(False)

        # Llenar la tabla con los datos de las secuencias alineadas
        for row_index, alignment in enumerate(self.multiple_alignment_representation):
            # Establecer la etiqueta de la fila como "S_i"
            row_label = QTableWidgetItem(f"S{row_index + 1}")
            row_label.setTextAlignment(Qt.AlignCenter)
            self.table_widget.setItem(row_index, 0, row_label)

            for col_index, char in enumerate(alignment):
                item = QTableWidgetItem(char)
                item.setTextAlignment(Qt.AlignCenter)
                self.table_widget.setItem(row_index, col_index + 1, item)

        self.table_widget.setFont(QFont("Courier", 10))  # Fuente monoespaciada para alineación precisa

        # Ajustar el ancho de las columnas
        for i in range(num_columnas):
            self.table_widget.setColumnWidth(i, 40)  # Ajustar el ancho de cada columna a 30 píxeles

        layout.addWidget(self.table_widget)
        self.setLayout(layout)
class VentanaAlignStar(QMainWindow):
    def __init__(self, matriz_scores, row_max, multipleAligment_representation, secuencias, map_first_alignment):
        super().__init__()
        self.matriz_scores = matriz_scores
        self.row_max = row_max
        self.multipleAligment_representation = multipleAligment_representation
        self.secuencias = secuencias
        self.map_first_alignment = map_first_alignment
        self.temp_dir = tempfile.TemporaryDirectory()
        self.image_paths = []
        self.initUI()

    def initUI(self):
        # Configurar la ventana principal
        self.configurarVentana()

        # Crear el widget central y establecerlo
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Crear el layout principal y el widget de pestañas
        layout = QVBoxLayout()
        tabs = self.crearPestanas()
        layout.addWidget(tabs)
        central_widget.setLayout(layout)

    def configurarVentana(self):
        self.setWindowTitle("Ventana de Alineamiento Estrella")
        #self.setWindowIcon(QIcon("icono.png"))  # Ajusta el icono si es necesario
        self.resize(800, 600)  # Ajusta el tamaño inicial si es necesario


    def crearPestanas(self):
        # Crear el widget de pestañas
        tabs = QTabWidget()
        # Crear las pestañas y añadirlas al widget de pestañas
        tabs.addTab(self.crearTab1(), "Matriz de scores por pares")
        tabs.addTab(self.crearTab2(), "Secuencia estrella")
        tabs.addTab(self.crearTab3(), "alineacion con la estrella")
        tabs.addTab(self.crearTab4(), "alineacion multiple")
        return tabs

    def crearTab1(self):
        # Crear el contenido para la primera pestaña (Matriz de Scores)
        widget = QWidget()
        layout = QVBoxLayout()

        # Agregar título "Matriz de Scores"
        titulo_matriz = QLabel("Matriz de Scores")
        titulo_matriz.setFont(QFont("Arial", weight=QFont.Bold, italic=True))
        titulo_matriz.setAlignment(Qt.AlignCenter)
        layout.addWidget(titulo_matriz)

        # Crear la tabla para mostrar la matriz de scores
        num_filas = len(self.matriz_scores)
        num_columnas = len(self.matriz_scores[0]) if num_filas > 0 else 0
        self.table = QTableWidget(num_filas + 1, num_columnas + 1)  # Añadir una fila y columna extra para las sumas

        # Llenar la tabla con los datos de la matriz
        columna_sumas = [0] * num_columnas  # Inicializar la suma de cada columna
        fila_max_valor = -float('inf')
        columna_max_valor = -float('inf')
        fila_max_pos = -1
        columna_max_pos = -1

        for i in range(num_filas):
            fila_suma = 0  # Inicializar la suma de la fila
            for j in range(num_columnas):
                valor = self.matriz_scores[i][j]
                item = QTableWidgetItem(str(valor))
                item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(i, j, item)
                fila_suma += valor  # Sumar los valores de la fila
                columna_sumas[j] += valor  # Sumar los valores de la columna

            # Añadir la suma al final de la fila
            suma_item = QTableWidgetItem(str(fila_suma))
            suma_item.setTextAlignment(Qt.AlignCenter)
            suma_item.setBackground(QColor(173, 216, 230))  # Establecer el color de fondo azul claro
            self.table.setItem(i, num_columnas, suma_item)

            # Buscar el mayor valor en la última columna
            if fila_suma > columna_max_valor:
                columna_max_valor = fila_suma
                columna_max_pos = i

        # Añadir la fila de sumas al final de la tabla
        for j in range(num_columnas):
            valor = columna_sumas[j]
            suma_item = QTableWidgetItem(str(valor))
            suma_item.setTextAlignment(Qt.AlignCenter)
            suma_item.setBackground(QColor(173, 216, 230))  # Establecer el color de fondo azul claro
            self.table.setItem(num_filas, j, suma_item)

            # Buscar el mayor valor en la última fila
            if valor > fila_max_valor:
                fila_max_valor = valor
                fila_max_pos = j

        # Establecer el valor total de la última celda en la última fila y columna
        total_suma = sum(columna_sumas)
        total_item = QTableWidgetItem(str(total_suma))
        total_item.setTextAlignment(Qt.AlignCenter)
        total_item.setBackground(QColor(173, 216, 230))
        self.table.setItem(num_filas, num_columnas, total_item)

        # Resaltar el mayor valor en la última fila (suma de columnas)
        if fila_max_pos != -1:
            item_max_fila = self.table.item(num_filas, fila_max_pos)
            item_max_fila.setBackground(QColor(255, 255, 0))  # Establecer el color de fondo amarillo

        # Resaltar el mayor valor en la última columna (suma de filas)
        if columna_max_pos != -1:
            item_max_columna = self.table.item(columna_max_pos, num_columnas)
            item_max_columna.setBackground(QColor(255, 255, 0))  # Establecer el color de fondo amarillo

        # Añadir la tabla al layout
        layout.addWidget(self.table)

        widget.setLayout(layout)
        return widget

    def crearTab2(self):
        # Crear el contenido para la segunda pestaña
        widget = QWidget()
        layout = QVBoxLayout()

        # Mensaje sobre el centro del alineamiento
        centro = self.row_max
        secuencia_centro = self.secuencias[centro]
        mensaje_centro = f"El centro es: S{centro + 1}: {secuencia_centro}"
        mensaje_label = QLabel(mensaje_centro)
        mensaje_label.setFont(QFont("Arial", weight=QFont.Bold))
        mensaje_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(mensaje_label)

        # Crear un QLabel para mostrar la imagen del grafo
        imagen_grafo = QLabel()
        imagen_grafo.setAlignment(Qt.AlignCenter)
        layout.addWidget(imagen_grafo)

        # Generar la imagen del grafo temporalmente y mostrarla
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp_file:
            ruta_imagen = tmp_file.name
            self.crear_imagen_grafo_temporal(self.secuencias, self.row_max, ruta_imagen)
            pixmap = QPixmap(ruta_imagen)
            imagen_grafo.setPixmap(pixmap)

        widget.setLayout(layout)
        return widget

    def crear_imagen_grafo_temporal(self, secuencias, row_max, ruta_imagen):
        # Crear un grafo dirigido
        G = nx.DiGraph()

        # Nodo raíz
        centro = row_max
        G.add_node(f"S{centro+1}")

        # Añadir nodos hijos
        for i, secuencia in enumerate(secuencias):
            if i != row_max:
                G.add_edge(f"S{centro+1}", f"S{i+1}")

        # Dibujar el grafo
        pos = nx.spring_layout(G)
        plt.figure(figsize=(8, 6))
        nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=2000, font_size=10, font_weight='bold')
        plt.title(f"Grafo de alineamiento con centro S{row_max + 1}")
        plt.savefig(ruta_imagen)
        plt.close()

    def crearTab3(self):
        # Crear el contenido para la tercera pestaña (Alineaciones)
        widget = QWidget()
        layout = QVBoxLayout()

        # Crear título para el tab
        titulo = QLabel(f"El centro es: S{self.row_max + 1}: {self.secuencias[self.row_max]}")
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
        self.slider.setMaximum(len(self.secuencias) - 2)  # -2 porque el centro no se cuenta
        self.slider.valueChanged.connect(self.update_image)
        layout.addWidget(self.slider)

        # Generar imágenes y actualizar la primera
        self.generate_images()
        self.update_image(0)

        widget.setLayout(layout)
        return widget

    def generate_images(self):
        self.image_paths = []
        for index, (e, alineamiento) in enumerate(self.map_first_alignment[self.row_max].items()):
            if e != self.row_max:
                seq1, seq2 = alineamiento.split("|")

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
        #self.alineacion_label.setText(f"Emparejamiento {index+1}")

        # Obtener las secuencias alineadas usando self.row_max y el índice actual (index)
        #seq1, seq2 = self.map_first_alignment[self.row_max][index].split("|")

        # Crear etiquetas para las secuencias alineadas
        #S1 = f"S{self.row_max + 1}"
        #Sx = f"S{index + 1}"

        # Actualizar el QLabel para mostrar las secuencias alineadas
        #self.alineacion_label.setText(f"{S1}\n{Sx}")
        #self.alineacion_label.setFont(QFont("Arial", weight=QFont.Bold, italic=True))

    def crearTab4(self):
        # Crear el contenido para la cuarta pestaña
        widget = AlineacionesTableWidget(self.multipleAligment_representation)
        return widget


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

        # Llamar a la función de alineamiento
        matriz_scores, row_max, multiple_alignment, map_first_alignment = startAligmentFunction(lineas)

        # Crear y mostrar la nueva ventana con los resultados
        self.ventana_align_star = VentanaAlignStar(matriz_scores, row_max, multiple_alignment,lineas,map_first_alignment)
        self.ventana_align_star.show()

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
