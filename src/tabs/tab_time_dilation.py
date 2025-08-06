from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QSlider, QHBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np

import numpy as np
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QSlider, QHBoxLayout
from PyQt5.QtCore import Qt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

def create_time_dilation_tab():
    tab = QWidget()
    layout = QVBoxLayout()
    label = QLabel("""
<div style='background:linear-gradient(120deg,#e3f2fd 60%,#90caf9 100%); border-radius:18px; box-shadow:0 4px 18px #0001; padding:20px 18px 18px 18px; margin-bottom:18px; font-family:Segoe UI,Arial,sans-serif;'>
<h2 style='color:#1565c0; font-size:1.7em; margin-top:0; margin-bottom:10px; letter-spacing:1px; text-shadow:0 2px 8px #0002;'>Dilatación temporal gravitacional</h2>
<div style='font-size:1.1em; margin-bottom:10px;'><b>¿Sabías que el tiempo transcurre más lento cerca de objetos masivos?</b></div>
<div style='margin-bottom:8px;'><b>Explicación:</b> Según la relatividad general, la presencia de una masa deforma el espacio-tiempo y ralentiza el paso del tiempo en su proximidad. Este efecto es medible, por ejemplo, en satélites GPS y cerca de agujeros negros.</div>
<div style='margin-bottom:8px;'><b>Fórmula:</b> <span style='background:#fffde7; border-radius:8px; padding:2px 8px; color:#b26500; font-weight:bold;'>Δt' = Δt · √(1 - rₛ/r)</span></div>
<ul style='margin:0 0 0 18px;'>
<li><b>Δt'</b>: tiempo propio (cerca de la masa)</li>
<li><b>Δt</b>: tiempo lejano (lejos de la masa)</li>
<li><b>rₛ</b>: radio de Schwarzschild</li>
<li><b>r</b>: distancia al centro de la masa</li>
</ul>
<div style='margin-bottom:8px;'><b>Historia:</b> <span style='color:#1565c0;'>Este fenómeno fue predicho por Einstein en 1916 y confirmado experimentalmente con relojes atómicos en diferentes alturas.</span></div>
<div style='font-size:0.98em;'><b>Referencia:</b> <a href='https://es.wikipedia.org/wiki/Dilataci%C3%B3n_del_tiempo_gravitacional' style='color:#1565c0; text-decoration:underline;'>Wikipedia</a></div>
</div>
        """)
    label.setOpenExternalLinks(True)
    label.setWordWrap(True)
    layout.addWidget(label)

    slider_layout = QHBoxLayout()
    slider_label = QLabel("r/rₛ:")
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
            result_label.setText("<span style='color:red;'>r debe ser mayor que rₛ</span>")
            return
        dilation = np.sqrt(1 - rs/r)
        result_label.setText(f"<b>Relación temporal:</b> Δt'/Δt = <span style='color:#1565c0;'>{dilation:.5f}</span>")
        fig.clear()
        ax = fig.add_subplot(111)
        r_vals = np.linspace(1.01, 10, 200)
        y = np.sqrt(1 - 1/r_vals)
        ax.plot(r_vals, y, color='#1976d2')
        ax.axvline(r_over_rs, color='r', linestyle='--')
        ax.set_xlabel("r/rₛ")
        ax.set_ylabel("Δt'/Δt")
        ax.set_title("Dilatación temporal gravitacional")
        ax.grid(True)
        canvas.draw()

    slider.valueChanged.connect(update)
    value_label.setText(f"{slider.value()/10:.1f}")
    update()

    tab.setLayout(layout)
    return tab
