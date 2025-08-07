import numpy as np
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

def create_wormhole_tab():
    tab = QWidget()
    layout = QVBoxLayout(tab)
    layout.addWidget(QLabel("<b>Agujero de Gusano (visualización)</b>"))
    desc = QLabel("Visualiza la geometría de un agujero de gusano tipo Morris-Thorne.")
    desc.setWordWrap(True)
    layout.addWidget(desc)
    fig = Figure(figsize=(5,4))
    canvas = FigureCanvas(fig)
    layout.addWidget(canvas)
    r = np.linspace(-2,2,400)
    z = np.sinh(r)
    fig.clear()
    ax = fig.add_subplot(111)
    ax.plot(r, z, color="#6a1b9a", linewidth=3)
    ax.set_title("Sección de un agujero de gusano")
    ax.axis('off')
    canvas.draw()
    tab.setLayout(layout)
    return tab
