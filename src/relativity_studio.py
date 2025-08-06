"""
Lanzador principal de Relativity Studio
"""

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget

# Importar los módulos de pestañas
from tabs.tab_intro import create_intro_tab
from tabs.tab_time_dilation import create_time_dilation_tab
from tabs.tab_curvature import create_curvature_tab
from tabs.tab_geodesics import create_numeric_geodesics_tab
from tabs.tab_light_deflection import create_light_deflection_tab
from tabs.tab_orbits import create_orbits_tab

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Relativity Studio - Relatividad General Didáctica")
        self.setGeometry(100, 100, 1000, 700)
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        self.init_tabs()

    def init_tabs(self):
        self.tabs.addTab(create_intro_tab(), "Introducción")
        self.tabs.addTab(create_time_dilation_tab(), "Dilatación Temporal")
        self.tabs.addTab(create_curvature_tab(), "Curvatura Espacio-Tiempo")
        self.tabs.addTab(create_numeric_geodesics_tab(), "Geodésicas Numéricas")
        self.tabs.addTab(create_light_deflection_tab(), "Deflexión de la Luz")
        self.tabs.addTab(create_orbits_tab(), "Órbitas Relativistas")

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()