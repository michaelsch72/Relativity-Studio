import numpy as np
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QSlider
from PyQt5.QtCore import Qt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

def create_kerr_tab():
    tab = QWidget()
    layout = QVBoxLayout(tab)
    layout.addWidget(QLabel("<b>Rotación (Agujero Negro de Kerr)</b>"))
    desc = QLabel("Visualiza el arrastre de referencia y la ergosfera de un agujero negro en rotación.")
    desc.setWordWrap(True)
    layout.addWidget(desc)
    slider = QSlider(Qt.Horizontal)
    slider.setMinimum(0)
    slider.setMaximum(99)
    slider.setValue(50)
    layout.addWidget(QLabel("Parámetro de rotación a/M:"))
    layout.addWidget(slider)
    fig = Figure(figsize=(5,4))
    canvas = FigureCanvas(fig)
    layout.addWidget(canvas)
    def update():
        a = slider.value()/100
        theta = np.linspace(0,2*np.pi,200)
        r_erg = 1 + np.sqrt(1 - a**2 * np.cos(theta)**2)
        r_hor = 1 + np.sqrt(1 - a**2)
        fig.clear()
        ax = fig.add_subplot(111, polar=True)
        ax.plot(theta, r_erg, color="#b26500", linewidth=2, label="Ergosfera")
        ax.plot(theta, np.ones_like(theta)*r_hor, color="#1976d2", linewidth=2, label="Horizonte")
        ax.set_title("Agujero negro de Kerr")
        ax.set_yticklabels([])
        ax.legend()
        canvas.draw()
    slider.valueChanged.connect(update)
    update()
    tab.setLayout(layout)
    return tab
