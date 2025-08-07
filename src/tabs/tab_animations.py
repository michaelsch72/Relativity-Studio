import numpy as np
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QGroupBox
from PyQt5.QtCore import QTimer
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

def create_animations_tab():
    tab = QWidget()
    layout = QVBoxLayout(tab)

    title = QLabel("<b>Animaciones Relativistas</b>")
    title.setStyleSheet("font-size: 18px; color: #1565c0; margin: 10px 0;")
    layout.addWidget(title)

    desc = QLabel("Ejemplo: animación de una órbita relativista precesando alrededor de una masa central.")
    desc.setWordWrap(True)
    desc.setStyleSheet("font-size: 14px; color: #333; margin-bottom: 10px;")
    layout.addWidget(desc)

    fig = Figure(figsize=(6, 5))
    canvas = FigureCanvas(fig)
    layout.addWidget(canvas)

    # Parámetros de la órbita
    rs = 1.0
    a = 6
    e = 0.3
    phi = np.linspace(0, 8 * np.pi, 2000)
    r = a * (1 - e ** 2) / (1 + e * np.cos(phi - 0.05 * phi))  # precesión simple
    x = r * np.cos(phi)
    y = r * np.sin(phi)

    # Animación con QTimer
    idx = [0]
    def animate():
        fig.clear()
        ax = fig.add_subplot(111)
        ax.plot(x, y, color="#1976d2", alpha=0.3)
        ax.plot(0, 0, 'ko', markersize=10)
        ax.plot(x[:idx[0]], y[:idx[0]], color="#1976d2", linewidth=2)
        ax.set_aspect('equal')
        ax.set_xlim(-a*1.2, a*1.2)
        ax.set_ylim(-a*1.2, a*1.2)
        ax.set_title("Órbita relativista animada", fontsize=15, color="#1976d2")
        ax.axis('off')
        idx[0] += 8
        if idx[0] > len(x):
            idx[0] = 0
        canvas.draw()

    timer = QTimer()
    timer.timeout.connect(animate)
    timer.start(30)

    animate()

    tab.setLayout(layout)
    return tab
