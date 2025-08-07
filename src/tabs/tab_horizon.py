import numpy as np
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

def create_horizon_tab():
    tab = QWidget()
    layout = QVBoxLayout(tab)
    layout.addWidget(QLabel("<b>Horizontes y Regiones Prohibidas</b>"))
    desc = QLabel("Visualiza el horizonte de eventos y las regiones donde no se puede escapar de un agujero negro.")
    desc.setWordWrap(True)
    layout.addWidget(desc)
    fig = Figure(figsize=(5,4))
    canvas = FigureCanvas(fig)
    layout.addWidget(canvas)
    theta = np.linspace(0,2*np.pi,200)
    r = np.ones_like(theta)
    fig.clear()
    ax = fig.add_subplot(111, polar=True)
    ax.fill_between(theta, 0, r, color="#b26500", alpha=0.3, label="Región prohibida")
    ax.plot(theta, r, color="#1976d2", linewidth=2, label="Horizonte de eventos")
    ax.set_title("Horizonte de eventos (rₛ)")
    ax.set_yticklabels([])
    ax.legend()
    canvas.draw()
    tab.setLayout(layout)
    return tab
