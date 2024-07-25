import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QGridLayout, QGroupBox, QCheckBox, QPushButton, QMessageBox, QWidget, QTabWidget
from PySide6.QtGui import QAction

tareas = ["01 Basico", "02 Alineamiento de dos secuencias","03 Alineamiento múltiple","04 Clusterización","05 Diagrama Filogenia","06 Estructura Secundaria"]
subtareas = [
                ["¿Qué tipo es? ADN, ARN o proteína", "Cantidad de elementos","Transcripción (ADN -> ARN)"],
                ["Matriz de punto","Alineamiento global (que se pueda variar las penalizaciones)","Alineamiento local","Alineamiento proteínas (usar Blosum o Pam) - FASTA"],
                ["Alineamiento Estrella","NJ"],
                ["Aglomerativo ","max","min"],
                ["Creación de un árbol enraizado (diagrama)"],
                ["watson - crick"],
            ]

class MiVentana(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        for e in range(6):
            print(tareas[e])
        self.configurarVentana()
        self.configurarMenu()

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()

        tabs = self.crearPestanas()
        layout.addWidget(tabs)
        central_widget.setLayout(layout)

    def mostrarMensaje(self):
        QMessageBox.information(self, 'Mensaje', '¡Hola, PySide6!')

    def configurarVentana(self):
        self.setWindowTitle('Visualizador Bioinformatica')
        self.setGeometry(100, 100, 800, 700)

    def configurarMenu(self):
        # Crear barra de menú
        menubar = self.menuBar()
        # Crear menú "File"
        fileMenu = menubar.addMenu('File')
        # Crear acción "Quit"
        quitAction = QAction('Quit', self)
        quitAction.setShortcut('Ctrl+Q')
        quitAction.triggered.connect(self.close)

        # Añadir acción "Quit" al menú "File"
        fileMenu.addAction(quitAction)
    def crearPestanas(self):
        # Crear QTabWidget
        tabs = QTabWidget()

        # Crear las pestañas
        tab_todo = QWidget()
        tab_01 = QWidget()
        tab_02 = QWidget()
        tab_03 = QWidget()
        tab_04 = QWidget()
        tab_05 = QWidget()
        tab_06 = QWidget()

        # Añadir las pestañas al QTabWidget
        tabs.addTab(tab_todo, "TO DO")
        tabs.addTab(tab_01, "01")
        tabs.addTab(tab_02, "02")
        tabs.addTab(tab_03, "03")
        tabs.addTab(tab_04, "04")
        tabs.addTab(tab_05, "05")
        tabs.addTab(tab_06, "06")

        # Crear contenido para la pestaña "TODO"
        tab_todo_layout = QGridLayout()
        for i in range(6):
           group_box = self.crearRecuadro(i)
           tab_todo_layout.addWidget(group_box, i // 3, i % 3)

        tab_todo.setLayout(tab_todo_layout)

        tab_01_layout = QVBoxLayout()
        tab_01_layout.addWidget(QPushButton("Botón en la pestaña 01"))
        tab_01.setLayout(tab_01_layout)

        tab_02_layout = QVBoxLayout()
        tab_02_layout.addWidget(QPushButton("Botón en la pestaña 02"))
        tab_02.setLayout(tab_02_layout)

        tab_03_layout = QVBoxLayout()
        tab_03_layout.addWidget(QPushButton("Botón en la pestaña 03"))
        tab_03.setLayout(tab_03_layout)

        tab_04_layout = QVBoxLayout()
        tab_04_layout.addWidget(QPushButton("Botón en la pestaña 04"))
        tab_04.setLayout(tab_04_layout)

        tab_05_layout = QVBoxLayout()
        tab_05_layout.addWidget(QPushButton("Botón en la pestaña 05"))
        tab_05.setLayout(tab_05_layout)

        tab_06_layout = QVBoxLayout()
        tab_06_layout.addWidget(QPushButton("Botón en la pestaña 06"))
        tab_06.setLayout(tab_06_layout)
        return tabs

    def crearRecuadro(self, num):
        #group_box = QGroupBox(f"{num+1}")
        group_box = QGroupBox(tareas[num])
        layout = QVBoxLayout()
        for j in range(len(subtareas[num])):
            checkbox = QCheckBox(subtareas[num][j])
            layout.addWidget(checkbox)
        group_box.setLayout(layout)
        return group_box

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = MiVentana()
    ventana.show()
    sys.exit(app.exec())
