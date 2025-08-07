import numpy as np
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

def create_bh_collision_tab():
    tab = QWidget()
    layout = QVBoxLayout(tab)
    layout.addWidget(QLabel("<b>Colisión de Agujeros Negros</b>"))
    desc = QLabel("Visualiza la fusión de dos agujeros negros y la emisión de ondas gravitacionales.")
    desc.setWordWrap(True)
    layout.addWidget(desc)
    fig = Figure(figsize=(5,4))
    canvas = FigureCanvas(fig)
    layout.addWidget(canvas)
    t = np.linspace(0, 2*np.pi, 200)
    x1 = -np.cos(t)
    y1 = np.sin(t)
    x2 = np.cos(t)
    y2 = -np.sin(t)
    fig.clear()
    ax = fig.add_subplot(111)
    ax.plot(x1, y1, color="#1976d2", linewidth=3)
    ax.plot(x2, y2, color="#b26500", linewidth=3)
    ax.plot([0], [0], 'ko', markersize=18)
    ax.set_title("Trayectorias antes de la fusión")
    ax.axis('off')
    canvas.draw()
    tab.setLayout(layout)
    return tab
