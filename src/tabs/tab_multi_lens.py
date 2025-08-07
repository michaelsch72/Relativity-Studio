import numpy as np
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

def create_multi_lens_tab():
    tab = QWidget()
    layout = QVBoxLayout(tab)
    layout.addWidget(QLabel("<b>Lentes Gravitacionales Múltiples</b>"))
    desc = QLabel("Simula la trayectoria de la luz en presencia de varias masas (lentes).")
    desc.setWordWrap(True)
    layout.addWidget(desc)
    fig = Figure(figsize=(5,4))
    canvas = FigureCanvas(fig)
    layout.addWidget(canvas)
    # Dos masas
    masses = [(-1,0), (1,0)]
    x = np.linspace(-2,2,400)
    y = 0.2/(x+1.1) + 0.2/(x-1.1)
    fig.clear()
    ax = fig.add_subplot(111)
    ax.plot(x, y, color="#1976d2", linewidth=2)
    for mx, my in masses:
        ax.plot(mx, my, 'o', color="#b26500", markersize=12)
    ax.set_title("Trayectoria de la luz entre dos lentes")
    ax.axis('off')
    canvas.draw()
    tab.setLayout(layout)
    return tab
