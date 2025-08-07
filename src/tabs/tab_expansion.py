import numpy as np
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QSlider
from PyQt5.QtCore import Qt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

def create_expansion_tab():
    tab = QWidget()
    layout = QVBoxLayout(tab)
    layout.addWidget(QLabel("<b>Expansión del Universo</b>"))
    desc = QLabel("Simula la expansión de galaxias según la ley de Hubble.")
    desc.setWordWrap(True)
    layout.addWidget(desc)
    slider = QSlider(Qt.Horizontal)
    slider.setMinimum(0)
    slider.setMaximum(100)
    slider.setValue(0)
    layout.addWidget(QLabel("Tiempo (unidades arbitrarias):"))
    layout.addWidget(slider)
    fig = Figure(figsize=(5,4))
    canvas = FigureCanvas(fig)
    layout.addWidget(canvas)
    def update():
        t = slider.value()/20
        x = np.linspace(-1,1,10)
        y = np.zeros_like(x)
        scale = np.exp(0.5*t)
        fig.clear()
        ax = fig.add_subplot(111)
        ax.scatter(x*scale, y, color="#b26500", s=80)
        ax.set_xlim(-5,5)
        ax.set_ylim(-1,1)
        ax.set_title(f"Galaxias alejándose (t={t:.1f})")
        ax.axis('off')
        canvas.draw()
    slider.valueChanged.connect(update)
    update()
    tab.setLayout(layout)
    return tab
