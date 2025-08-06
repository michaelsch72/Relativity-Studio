from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QSlider, QHBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from scipy.integrate import solve_ivp
import numpy as np

import numpy as np
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QSlider, QHBoxLayout
from PyQt5.QtCore import Qt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from scipy.integrate import solve_ivp

def create_orbits_tab():
    tab = QWidget()
    layout = QVBoxLayout()
    label = QLabel("""
<div style='background:linear-gradient(120deg,#e1f5fe 60%,#b3e5fc 100%); border-radius:18px; box-shadow:0 4px 18px #0001; padding:20px 18px 18px 18px; margin-bottom:18px; font-family:Segoe UI,Arial,sans-serif;'>
<h2 style='color:#0277bd; font-size:1.7em; margin-top:0; margin-bottom:10px; letter-spacing:1px; text-shadow:0 2px 8px #0002;'>Órbitas relativistas</h2>
<div style='font-size:1.1em; margin-bottom:10px;'><b>¿Por qué las órbitas cerca de objetos masivos no son elipses perfectas?</b></div>
<div style='margin-bottom:8px;'><b>Explicación:</b> En la relatividad general, las órbitas de partículas alrededor de una masa central (como el Sol o un agujero negro) presentan precesión y pueden ser inestables o de escape, dependiendo del momento angular.</div>
<div style='margin-bottom:8px;'><b>Visualización:</b> <span style='color:#0277bd;'>Ajusta el momento angular para ver órbitas circulares, elípticas o trayectorias de escape.</span></div>
<div style='margin-bottom:8px;'><b>Fórmula:</b> <span style='background:#fffde7; border-radius:8px; padding:2px 8px; color:#b26500; font-weight:bold;'>d²u/dφ² + u = GM/L² + 3GMu²/c²</span> <span style='font-size:0.95em;'>(ecuación relativista para órbitas)</span></div>
<ul style='margin:0 0 0 18px;'>
<li><b>L:</b> momento angular</li>
<li><b>u = 1/r</b></li>
<li><b>G, M, c:</b> constantes universales</li>
</ul>
<div style='margin-bottom:8px;'><b>Historia:</b> <span style='color:#0277bd;'>La precesión del perihelio de Mercurio fue una de las primeras pruebas de la relatividad general.</span></div>
<div style='font-size:0.98em;'><b>Referencia:</b> <a href='https://es.wikipedia.org/wiki/%C3%93rbita_relativista' style='color:#0277bd; text-decoration:underline;'>Wikipedia</a></div>
</div>
        """)
    label.setOpenExternalLinks(True)
    label.setWordWrap(True)
    layout.addWidget(label)

    slider_layout = QHBoxLayout()
    slider_label = QLabel("Momento angular L:")
    slider = QSlider(Qt.Horizontal)
    slider.setMinimum(35)
    slider.setMaximum(100)
    slider.setValue(50)
    slider.setTickInterval(1)
    slider.setTickPosition(QSlider.TicksBelow)
    value_label = QLabel("5.0")
    slider_layout.addWidget(slider_label)
    slider_layout.addWidget(slider)
    slider_layout.addWidget(value_label)
    layout.addLayout(slider_layout)

    fig = Figure(figsize=(4,4))
    canvas = FigureCanvas(fig)
    layout.addWidget(canvas)

    def orbit_rhs(phi, y, L):
        r, pr = y
        rs = 1.0
        f = 1 - rs/r
        dpr = (L**2/r**3 - rs*L**2/r**4) - rs/(2*r**2)*pr**2/f
        dr = pr
        return [dr, dpr/f]

    def plot_orbit():
        L = slider.value() / 10
        value_label.setText(f"{L:.1f}")
        r0 = 10.0
        pr0 = 0.0
        y0 = [r0, pr0]
        phis = np.linspace(0, 24*np.pi, 4000)
        try:
            sol = solve_ivp(lambda phi, y: orbit_rhs(phi, y, L), [phis[0], phis[-1]], y0, t_eval=phis, rtol=1e-7, atol=1e-9)
            r = sol.y[0]
            phi = sol.t
            mask = r > 1.01
            if not np.any(mask):
                raise ValueError("La partícula cae en el horizonte de eventos.")
            x = r[mask] * np.cos(phi[mask])
            y = r[mask] * np.sin(phi[mask])
            fig.clear()
            ax = fig.add_subplot(111)
            ax.plot(x, y, color='#0277bd', label="Órbita relativista")
            ax.plot(0, 0, 'ko', markersize=10, label="Masa central")
            ax.set_aspect('equal')
            ax.set_xlabel("x")
            ax.set_ylabel("y")
            ax.set_title("Órbita en Schwarzschild")
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

    slider.valueChanged.connect(plot_orbit)
    value_label.setText(f"{slider.value()/10:.1f}")
    plot_orbit()

    tab.setLayout(layout)
    return tab
