import numpy as np
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QSlider, QHBoxLayout
from PyQt5.QtCore import Qt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

def create_doppler_tab():
    tab = QWidget()
    layout = QVBoxLayout(tab)
    layout.addWidget(QLabel("<b>Efecto Doppler Relativista</b>"))
    desc = QLabel("Visualiza el corrimiento al rojo y azul de la luz para diferentes velocidades relativas.")
    desc.setWordWrap(True)
    layout.addWidget(desc)
    slider = QSlider(Qt.Horizontal)
    slider.setMinimum(-99)
    slider.setMaximum(99)
    slider.setValue(0)
    layout.addWidget(QLabel("Velocidad relativa (% de c):"))
    layout.addWidget(slider)
    fig = Figure(figsize=(5,2))
    canvas = FigureCanvas(fig)
    layout.addWidget(canvas)
    def update():
        v = slider.value()/100
        gamma = 1/np.sqrt(1-v**2) if abs(v)<1 else 1
        freq_obs = gamma*(1-v)
        fig.clear()
        ax = fig.add_subplot(111)
        color = "#1976d2" if v<0 else "#b26500"
        ax.plot([0,1],[1,freq_obs], color=color, linewidth=4)
        ax.set_ylim(0,2)
        ax.set_title(f"Corrimiento {'al azul' if v<0 else 'al rojo'}: f_obs = {freq_obs:.2f} f_emitida")
        ax.axis('off')
        canvas.draw()
    slider.valueChanged.connect(update)
    update()
    tab.setLayout(layout)
    return tab
