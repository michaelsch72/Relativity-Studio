"""
Módulo principal de la app Relativity Studio
"""
import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QLabel, QSlider, QHBoxLayout
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class MainWindow(QMainWindow):
    # --- INICIO: Código restaurado tal cual el original ---
    def create_numeric_geodesics_tab(self):
        from scipy.integrate import solve_ivp
        from PyQt5.QtWidgets import QComboBox
        tab = QWidget()
        layout = QVBoxLayout()
        label = QLabel("""
<b>Geodésicas numéricas (Schwarzschild)</b><br>
Esta pestaña integra numéricamente las ecuaciones de las geodésicas en el espacio-tiempo de Schwarzschild para trayectorias de luz y partículas.<br>
<b>Visualización:</b> Ajusta el parámetro de impacto y elige tipo de partícula para ver la trayectoria real en el espacio-tiempo curvo.
        """)
        label.setWordWrap(True)
        layout.addWidget(label)

        controls = QHBoxLayout()
        slider_label = QLabel("Parámetro de impacto b:")
        slider = QSlider(Qt.Horizontal)
        slider.setMinimum(15)
        slider.setMaximum(100)
        slider.setValue(30)
        slider.setTickInterval(1)
        slider.setTickPosition(QSlider.TicksBelow)
        value_label = QLabel("3.0")
        controls.addWidget(slider_label)
        controls.addWidget(slider)
        controls.addWidget(value_label)

        type_label = QLabel("Tipo:")
        type_combo = QComboBox()
        type_combo.addItems(["Luz", "Partícula con masa"])
        controls.addWidget(type_label)
        controls.addWidget(type_combo)
        layout.addLayout(controls)

        fig = Figure(figsize=(4,4))
        canvas = FigureCanvas(fig)
        layout.addWidget(canvas)

        def geodesic_rhs(phi, y, b, is_light):
            r, pr = y
            rs = 1.0
            if is_light:
                E = 1.0
                L = b
                f = 1 - rs/r
                dpr = (L**2/r**3 - rs*L**2/r**4)
                dr = pr
                return [dr, dpr/f]
            else:
                E = 1.0
                L = b
                f = 1 - rs/r
                dpr = (L**2/r**3 - rs*L**2/r**4) - rs/(2*r**2)*pr**2/f
                dr = pr
                return [dr, dpr/f]

        def plot_geodesic():
            b = slider.value() / 10
            value_label.setText(f"{b:.1f}")
            is_light = (type_combo.currentIndex() == 0)
            r0 = 10.0
            pr0 = -0.1
            y0 = [r0, pr0]
            phis = np.linspace(0, 8*np.pi, 2000)
            try:
                sol = solve_ivp(lambda phi, y: geodesic_rhs(phi, y, b, is_light), [phis[0], phis[-1]], y0, t_eval=phis, rtol=1e-6)
                r = sol.y[0]
                phi = sol.t
                # Filtrar valores no físicos (r <= 1)
                mask = r > 1.01
                if not np.any(mask):
                    raise ValueError("La trayectoria cae en el horizonte de eventos.")
                x = r[mask] * np.cos(phi[mask])
                y = r[mask] * np.sin(phi[mask])
                fig.clear()
                ax = fig.add_subplot(111)
                ax.plot(x, y, label="Trayectoria")
                ax.plot(0, 0, 'ko', markersize=10, label="Masa central")
                ax.set_aspect('equal')
                ax.set_xlabel("x")
                ax.set_ylabel("y")
                ax.set_title("Geodésica en Schwarzschild")
                ax.legend()
                ax.grid(True)
                canvas.draw()
            except Exception as e:
                fig.clear()
                ax = fig.add_subplot(111)
                ax.text(0.5, 0.5, f"Error en la integración:\n{str(e)}", ha='center', va='center', fontsize=12, color='red', transform=ax.transAxes)
                ax.set_xticks([])
                ax.set_yticks([])
                canvas.draw()

        slider.valueChanged.connect(plot_geodesic)
        type_combo.currentIndexChanged.connect(plot_geodesic)
        plot_geodesic()

        tab.setLayout(layout)
        return tab

    def create_curvature_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        label = QLabel("Curvatura del espacio-tiempo: Visualización y explicación.")
        label.setWordWrap(True)
        layout.addWidget(label)
        tab.setLayout(layout)
        return tab

    def create_time_dilation_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        label = QLabel("""
<b>Dilatación temporal gravitacional</b><br>
Esta pestaña muestra cómo el tiempo transcurre más lento cerca de un objeto masivo.<br>
Usa el control deslizante para cambiar la distancia al centro de la masa (en radios de Schwarzschild).<br>
<i>Fórmula:</i> Δt' = Δt · sqrt(1 - r_s/r)
<br><br>
<b>r_s</b>: radio de Schwarzschild, <b>r</b>: distancia al centro
        """)
        label.setWordWrap(True)
        layout.addWidget(label)

        slider_layout = QHBoxLayout()
        slider_label = QLabel("r/r_s:")
        slider = QSlider(Qt.Horizontal)
        slider.setMinimum(11)
        slider.setMaximum(100)
        slider.setValue(20)
        slider.setTickInterval(1)
        slider.setTickPosition(QSlider.TicksBelow)
        value_label = QLabel("2.0")
        slider_layout.addWidget(slider_label)
        slider_layout.addWidget(slider)
        slider_layout.addWidget(value_label)
        layout.addLayout(slider_layout)

        result_label = QLabel()
        layout.addWidget(result_label)

        fig = Figure(figsize=(4,2))
        canvas = FigureCanvas(fig)
        layout.addWidget(canvas)

        def update():
            r_over_rs = slider.value() / 10
            value_label.setText(f"{r_over_rs:.1f}")
            rs = 1.0
            r = r_over_rs * rs
            if r <= rs:
                result_label.setText("r debe ser mayor que r_s")
                return
            dilation = np.sqrt(1 - rs/r)
            result_label.setText(f"Δt'/Δt = {dilation:.5f}")
            fig.clear()
            ax = fig.add_subplot(111)
            r_vals = np.linspace(1.01, 10, 200)
            y = np.sqrt(1 - 1/r_vals)
            ax.plot(r_vals, y)
            ax.axvline(r_over_rs, color='r', linestyle='--')
            ax.set_xlabel("r/r_s")
            ax.set_ylabel("Δt'/Δt")
            ax.set_title("Dilatación temporal gravitacional")
            ax.grid(True)
            canvas.draw()

        slider.valueChanged.connect(update)
        update()

        tab.setLayout(layout)
        return tab

    def create_intro_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        label = QLabel("Bienvenido a Relativity Studio. Explora la relatividad general de forma interactiva.")
        label.setWordWrap(True)
        layout.addWidget(label)
        tab.setLayout(layout)
        return tab

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Relativity Studio - Relatividad General Didáctica")
        self.setGeometry(100, 100, 1000, 700)
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        self.init_tabs()

    def init_tabs(self):
        self.tabs.addTab(self.create_intro_tab(), "Introducción")
        self.tabs.addTab(self.create_time_dilation_tab(), "Dilatación Temporal")
        self.tabs.addTab(self.create_curvature_tab(), "Curvatura Espacio-Tiempo")
        self.tabs.addTab(self.create_numeric_geodesics_tab(), "Geodésicas Numéricas")
        self.tabs.addTab(self.create_light_deflection_tab(), "Deflexión de la Luz")
        self.tabs.addTab(self.create_orbits_tab(), "Órbitas Relativistas")

    def create_light_deflection_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        label = QLabel("Deflexión de la luz: Simulación y explicación.")
        label.setWordWrap(True)
        layout.addWidget(label)
        tab.setLayout(layout)
        return tab

    def create_orbits_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        label = QLabel("Órbitas relativistas: Visualización y explicación.")
        label.setWordWrap(True)
        layout.addWidget(label)
        tab.setLayout(layout)
        return tab
    # --- FIN: Código restaurado ---

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
