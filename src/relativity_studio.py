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

# Sugerencias para mejorar tu programa:
# - Añadir exportación de gráficos a imagen (botón "Guardar gráfico").
# - Permitir cambiar parámetros físicos (G, c, masas) en una pestaña de configuración.
# - Añadir animaciones temporales (evolución de órbitas o trayectorias).  # <-- Puedes crear una pestaña "Animaciones" con ejemplos animados de órbitas, dilatación temporal, etc.
# - Incluir una pestaña de "Preguntas frecuentes" o "Glosario" para términos de relatividad.
# - Permitir comparar dos escenarios en paralelo (doble gráfico).
# - Añadir accesibilidad: modo oscuro, fuentes más grandes, etc.
# - Permitir copiar los cálculos de la "pizarra" como texto.
# - Añadir soporte para inglés/español (internacionalización).
# - Incluir referencias bibliográficas y enlaces a recursos didácticos.
# - Añadir simulaciones de efectos relativistas adicionales (ondas gravitacionales, lentes gravitacionales, etc).  # <-- Puedes crear una pestaña "Simulaciones avanzadas" para efectos como ondas gravitacionales o lentes gravitacionales.

# Para implementar:
# 1. Crea un archivo src/tabs/tab_animations.py con animaciones usando matplotlib.animation o QTimer.
# 2. Crea un archivo src/tabs/tab_advanced_effects.py para simulaciones como ondas gravitacionales o lentes gravitacionales.
# 3. Añade las nuevas pestañas en init_tabs():
#     self.tabs.addTab(create_animations_tab(), "Animaciones")
#     self.tabs.addTab(create_advanced_effects_tab(), "Simulaciones Avanzadas")

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()