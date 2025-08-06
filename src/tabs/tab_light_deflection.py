from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QSlider, QHBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np

import numpy as np
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QSlider, QHBoxLayout
from PyQt5.QtCore import Qt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

def create_light_deflection_tab():
    tab = QWidget()
    layout = QVBoxLayout()
    label = QLabel("""
<div style='background:linear-gradient(120deg,#fffde7 60%,#ffe0b2 100%); border-radius:18px; box-shadow:0 4px 18px #0001; padding:20px 18px 18px 18px; margin-bottom:18px; font-family:Segoe UI,Arial,sans-serif;'>
<h2 style='color:#ef6c00; font-size:1.7em; margin-top:0; margin-bottom:10px; letter-spacing:1px; text-shadow:0 2px 8px #0002;'>Deflexión de la luz</h2>
<div style='font-size:1.1em; margin-bottom:10px;'><b>¿Por qué la luz se curva cerca de una masa?</b></div>
<div style='margin-bottom:8px;'><b>Explicación:</b> La relatividad general predice que la luz sigue geodésicas en el espacio-tiempo curvado. Al pasar cerca de una masa, su trayectoria se desvía.</div>
<div style='margin-bottom:8px;'><b>Visualización:</b> <span style='color:#ef6c00;'>Ajusta el parámetro de impacto para ver cómo cambia la desviación.</span></div>
<div style='margin-bottom:8px;'><b>Fórmula:</b> <span style='background:#fffde7; border-radius:8px; padding:2px 8px; color:#b26500; font-weight:bold;'>Δφ ≈ 4GM/(c²b)</span> <span style='font-size:0.95em;'>(aproximación para campos débiles)</span></div>
<ul style='margin:0 0 0 18px;'>
<li><b>Δφ:</b> ángulo de deflexión</li>
<li><b>b:</b> parámetro de impacto</li>
<li><b>G, M, c:</b> constantes universales</li>
</ul>
<div style='margin-bottom:8px;'><b>Historia:</b> <span style='color:#ef6c00;'>La deflexión de la luz fue confirmada en 1919 durante un eclipse solar, validando la teoría de Einstein.</span></div>
<div style='font-size:0.98em;'><b>Referencia:</b> <a href='https://es.wikipedia.org/wiki/Deflexi%C3%B3n_de_la_luz' style='color:#ef6c00; text-decoration:underline;'>Wikipedia</a></div>
</div>
        """)
    label.setOpenExternalLinks(True)
    label.setWordWrap(True)
    layout.addWidget(label)

    slider_layout = QHBoxLayout()
    slider_label = QLabel("Parámetro de impacto b:")
    slider = QSlider(Qt.Horizontal)
    slider.setMinimum(15)
    slider.setMaximum(100)
    slider.setValue(30)
    slider.setTickInterval(1)
    slider.setTickPosition(QSlider.TicksBelow)
    value_label = QLabel("3.0")
    slider_layout.addWidget(slider_label)
    slider_layout.addWidget(slider)
    slider_layout.addWidget(value_label)
    layout.addLayout(slider_layout)

    fig = Figure(figsize=(4,4))
    canvas = FigureCanvas(fig)
    layout.addWidget(canvas)

    def plot_deflection():
        b = slider.value() / 10
        value_label.setText(f"{b:.1f}")
        rs = 1.0
        r0 = 10.0
        phi = np.linspace(-np.pi/2, np.pi/2, 500)
        # Trayectoria recta (sin masa)
        x0 = b * np.ones_like(phi)
        y0 = r0 * np.tan(phi)
        # Trayectoria desviada (aprox. 1er orden)
        delta = 2 * rs / b  # ángulo de deflexión aproximado
        x1 = b * np.ones_like(phi)
        y1 = r0 * np.tan(phi + delta/2 * np.sign(phi))
        fig.clear()
        ax = fig.add_subplot(111)
        ax.plot(x0, y0, 'b--', label="Sin masa (recta)")
        ax.plot(x1, y1, 'r', label="Con masa (desviada)")
        ax.plot(0, 0, 'ko', markersize=10, label="Masa central")
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_title("Deflexión de la luz por gravedad")
        ax.legend()
        ax.grid(True)
        canvas.draw()

    slider.valueChanged.connect(plot_deflection)
    value_label.setText(f"{slider.value()/10:.1f}")
    plot_deflection()

    tab.setLayout(layout)
    return tab
