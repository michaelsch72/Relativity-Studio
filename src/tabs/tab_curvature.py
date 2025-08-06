from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QSlider, QHBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np

import numpy as np
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QSlider, QHBoxLayout
from PyQt5.QtCore import Qt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

def create_curvature_tab():
    tab = QWidget()
    layout = QVBoxLayout()
    label = QLabel("""
<div style='background:linear-gradient(120deg,#ede7f6 60%,#b39ddb 100%); border-radius:18px; box-shadow:0 4px 18px #0001; padding:20px 18px 18px 18px; margin-bottom:18px; font-family:Segoe UI,Arial,sans-serif;'>
<h2 style='color:#6a1b9a; font-size:1.7em; margin-top:0; margin-bottom:10px; letter-spacing:1px; text-shadow:0 2px 8px #0002;'>Curvatura del espacio-tiempo</h2>
<div style='font-size:1.1em; margin-bottom:10px;'><b>¿Cómo se deforma el espacio-tiempo cerca de una masa?</b></div>
<div style='margin-bottom:8px;'><b>Explicación:</b> La relatividad general describe la gravedad como la curvatura del espacio-tiempo causada por la masa y la energía. Cerca de una masa puntual, el espacio se "hunde" y las trayectorias de los objetos se curvan.</div>
<div style='margin-bottom:8px;'><b>Visualización:</b> <span style='color:#6a1b9a;'>Ajusta el radio de Schwarzschild (rₛ) para ver cómo cambia la curvatura.</span></div>
<div style='margin-bottom:8px;'><b>Fórmula:</b> <span style='background:#fffde7; border-radius:8px; padding:2px 8px; color:#b26500; font-weight:bold;'>z(r) = 2√[rₛ(r - rₛ)]</span></div>
<ul style='margin:0 0 0 18px;'>
<li><b>z(r):</b> altura de la superficie embebida</li>
<li><b>rₛ:</b> radio de Schwarzschild</li>
<li><b>r:</b> distancia radial</li>
</ul>
<div style='margin-bottom:8px;'><b>Historia:</b> <span style='color:#6a1b9a;'>Esta visualización fue propuesta por Flamm en 1916, poco después de la publicación de la teoría de Einstein.</span></div>
<div style='font-size:0.98em;'><b>Referencia:</b> <a href='https://es.wikipedia.org/wiki/Soluci%C3%B3n_de_Schwarzschild' style='color:#6a1b9a; text-decoration:underline;'>Wikipedia</a></div>
</div>
        """)
    label.setOpenExternalLinks(True)
    label.setWordWrap(True)
    layout.addWidget(label)

    slider_layout = QHBoxLayout()
    slider_label = QLabel("Radio de Schwarzschild rₛ:")
    slider = QSlider(Qt.Horizontal)
    slider.setMinimum(5)
    slider.setMaximum(50)
    slider.setValue(10)
    slider.setTickInterval(1)
    slider.setTickPosition(QSlider.TicksBelow)
    value_label = QLabel("1.0")
    slider_layout.addWidget(slider_label)
    slider_layout.addWidget(slider)
    slider_layout.addWidget(value_label)
    layout.addLayout(slider_layout)

    fig = Figure(figsize=(4,3))
    canvas = FigureCanvas(fig)
    layout.addWidget(canvas)

    def plot_curvature():
        rs = slider.value() / 10
        value_label.setText(f"{rs:.1f}")
        r = np.linspace(rs + 0.01, rs * 6, 300)
        z = 2 * np.sqrt(rs * (r - rs))
        fig.clear()
        ax = fig.add_subplot(111)
        ax.plot(r, z, color='#8e24aa', label="Superficie embebida")
        ax.set_xlabel("r (radio)")
        ax.set_ylabel("z (curvatura)")
        ax.set_title(f"Curvatura del espacio-tiempo (rₛ = {rs:.1f})")
        ax.grid(True)
        ax.legend()
        canvas.draw()

    slider.valueChanged.connect(plot_curvature)
    value_label.setText(f"{slider.value()/10:.1f}")
    plot_curvature()

    tab.setLayout(layout)
    return tab
