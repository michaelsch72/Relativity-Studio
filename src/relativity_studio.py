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
from tabs.tab_animations import create_animations_tab
from tabs.tab_advanced_effects import create_advanced_effects_tab
from tabs.tab_doppler import create_doppler_tab
from tabs.tab_wormhole import create_wormhole_tab
from tabs.tab_expansion import create_expansion_tab
from tabs.tab_bh_collision import create_bh_collision_tab
from tabs.tab_multi_lens import create_multi_lens_tab
from tabs.tab_twins import create_twins_tab
from tabs.tab_horizon import create_horizon_tab
from tabs.tab_freefall import create_freefall_tab
from tabs.tab_kerr import create_kerr_tab
from tabs.tab_energy_momentum import create_energy_momentum_tab

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
        self.tabs.addTab(create_animations_tab(), "Animaciones")
        self.tabs.addTab(create_advanced_effects_tab(), "Simulaciones Avanzadas")
def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()