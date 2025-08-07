import numpy as np
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

def create_energy_momentum_tab():
    tab = QWidget()
    layout = QVBoxLayout(tab)
    layout.addWidget(QLabel("<b>Energía y Momento en Espacio-Tiempo Curvo</b>"))
    desc = QLabel("Visualiza la conservación de la energía y el momento en trayectorias relativistas.")
    desc.setWordWrap(True)
    layout.addWidget(desc)
    fig = Figure(figsize=(5,3))
    canvas = FigureCanvas(fig)
    layout.addWidget(canvas)
    t = np.linspace(0, 2*np.pi, 200)
    E = np.ones_like(t)
    p = np.sin(t)
    fig.clear()
    ax = fig.add_subplot(111)
    ax.plot(t, E, color="#1976d2", label="Energía")
    ax.plot(t, p, color="#b26500", label="Momento")
    ax.set_title("Energía y momento (trayectoria relativista)")
    ax.legend()
    canvas.draw()
    tab.setLayout(layout)
    return tab
