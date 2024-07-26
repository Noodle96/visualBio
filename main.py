import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QGridLayout, QGroupBox, QCheckBox, QPushButton, QMessageBox, QWidget, QTabWidget
from PySide6.QtGui import QAction

from tabs.tab_01 import Tab01
from tabs.tab_02 import Tab02
from tabs.tab_03 import Tab03
from tabs.tab_04 import Tab04
from tabs.tab_05 import Tab05
from tabs.tab_06 import Tab06
from tabs.tab_todo import TabTODO

class MiVentana(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
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
        tabs = QTabWidget()
        tabs.addTab(TabTODO(), "To Do")
        tabs.addTab(Tab01(), "01")
        tabs.addTab(Tab02(), "02")
        tabs.addTab(Tab03(), "03")
        tabs.addTab(Tab04(), "04")
        tabs.addTab(Tab05(), "05")
        tabs.addTab(Tab06(), "06")
        return tabs

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = MiVentana()
    ventana.show()
    sys.exit(app.exec())
