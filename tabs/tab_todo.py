from PySide6.QtWidgets import QWidget, QGridLayout, QGroupBox, QVBoxLayout, QCheckBox

tareas = ["01 Basico", "02 Alineamiento de dos secuencias", "03 Alineamiento múltiple", "04 Clusterización", "05 Diagrama Filogenia", "06 Estructura Secundaria"]
subtareas = [
    ["¿Qué tipo es? ADN, ARN o proteína", "Cantidad de elementos", "Transcripción (ADN -> ARN)"],
    ["Matriz de punto", "Alineamiento global (que se pueda variar las penalizaciones)", "Alineamiento local", "Alineamiento proteínas (usar Blosum o Pam) - FASTA"],
    ["Alineamiento Estrella", "NJ"],
    ["Aglomerativo", "max", "min"],
    ["Creación de un árbol enraizado (diagrama)"],
    ["watson - crick"],
]

class TabTODO(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QGridLayout()
        for i in range(6):
            group_box = self.crearRecuadro(i)
            layout.addWidget(group_box, i // 3, i % 3)
        self.setLayout(layout)

    def crearRecuadro(self, num):
        group_box = QGroupBox(tareas[num])
        layout = QVBoxLayout()
        for j in range(len(subtareas[num])):
            checkbox = QCheckBox(subtareas[num][j])
            layout.addWidget(checkbox)
        group_box.setLayout(layout)
        return group_box
