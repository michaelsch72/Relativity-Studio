import numpy as np
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QSlider
from PyQt5.QtCore import Qt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

def create_freefall_tab():
    tab = QWidget()
    layout = QVBoxLayout(tab)
    layout.addWidget(QLabel("<b>Caída Libre en Schwarzschild/Kerr</b>"))
    desc = QLabel("Simula la caída libre radial hacia un agujero negro (Schwarzschild).")
    desc.setWordWrap(True)
    layout.addWidget(desc)
    slider = QSlider(Qt.Horizontal)
    slider.setMinimum(10)
    slider.setMaximum(100)
    slider.setValue(30)
    layout.addWidget(QLabel("Distancia inicial (r₀/rₛ):"))
    layout.addWidget(slider)
    fig = Figure(figsize=(5,3))
    canvas = FigureCanvas(fig)
    layout.addWidget(canvas)
    def update():
        r0 = slider.value()/10
        t = np.linspace(0,1,100)
        r = r0*(1-t)**(2/3)
        fig.clear()
        ax = fig.add_subplot(111)
        ax.plot(t, r, color="#1976d2", linewidth=2)
        ax.set_ylim(0,slider.value()/10+1)
        ax.set_title(f"Caída libre desde r₀={r0:.1f} rₛ")
        ax.set_xlabel("Tiempo propio (unidades)")
        ax.set_ylabel("r/rₛ")
        canvas.draw()
    slider.valueChanged.connect(update)
    update()
    tab.setLayout(layout)
    return tab
