from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QSlider, QHBoxLayout, QComboBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from scipy.integrate import solve_ivp
import numpy as np

import numpy as np
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QSlider, QHBoxLayout, QComboBox
from PyQt5.QtCore import Qt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from scipy.integrate import solve_ivp

def create_numeric_geodesics_tab():
    tab = QWidget()
    layout = QVBoxLayout()
    label = QLabel("""
<div style='background:linear-gradient(120deg,#e0f7fa 60%,#b2ebf2 100%); border-radius:18px; box-shadow:0 4px 18px #0001; padding:20px 18px 18px 18px; margin-bottom:18px; font-family:Segoe UI,Arial,sans-serif;'>
<h2 style='color:#00897b; font-size:1.7em; margin-top:0; margin-bottom:10px; letter-spacing:1px; text-shadow:0 2px 8px #0002;'>Geodésicas numéricas <span style="font-size:0.7em; color:#555;">(Schwarzschild)</span></h2>
<div style='font-size:1.1em; margin-bottom:10px;'><b>¿Cómo se mueven la luz y las partículas en el espacio-tiempo curvo?</b></div>
<div style='margin-bottom:8px;'><b>Explicación:</b> Las geodésicas son las trayectorias más "rectas" posibles en un espacio-tiempo curvado. En Schwarzschild, describen cómo la gravedad afecta el movimiento de la luz y de las partículas.</div>
<div style='margin-bottom:8px;'><b>Visualización:</b> <span style='color:#00897b;'>Ajusta el parámetro de impacto y elige el tipo de partícula para ver la trayectoria real en el espacio-tiempo curvo.</span></div>
<div style='margin-bottom:8px;'><b>Fórmulas:</b>
<ul style='margin:0 0 0 18px;'>
<li>Para luz: <span style='background:#fffde7; border-radius:8px; padding:2px 8px; color:#b26500; font-weight:bold;'>d²r/dφ² = r - 3rₛ/2</span></li>
<li>Para partículas: <span style='background:#fffde7; border-radius:8px; padding:2px 8px; color:#b26500;'>ecuación similar, pero con energía y masa</span></li>
</ul></div>
<div style='margin-bottom:8px;'><b>Historia:</b> <span style='color:#00897b;'>El cálculo de geodésicas permitió predecir la precesión del perihelio de Mercurio y la deflexión de la luz.</span></div>
<div style='font-size:0.98em;'><b>Referencia:</b> <a href='https://es.wikipedia.org/wiki/Geod%C3%A9sica' style='color:#00897b; text-decoration:underline;'>Wikipedia</a></div>
</div>
        """)
    label.setOpenExternalLinks(True)
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
    value_label.setText(f"{slider.value()/10:.1f}")
    plot_geodesic()

    tab.setLayout(layout)
    return tab
