import numpy as np
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QSlider
from PyQt5.QtCore import Qt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

def create_twins_tab():
    tab = QWidget()
    layout = QVBoxLayout(tab)
    layout.addWidget(QLabel("<b>Paradoja de los Gemelos</b>"))
    desc = QLabel("Simula la diferencia de tiempo vivido por dos gemelos: uno viaja a velocidad relativista y el otro permanece en la Tierra.")
    desc.setWordWrap(True)
    layout.addWidget(desc)
    slider = QSlider(Qt.Horizontal)
    slider.setMinimum(0)
    slider.setMaximum(99)
    slider.setValue(0)
    layout.addWidget(QLabel("Velocidad del gemelo viajero (% de c):"))
    layout.addWidget(slider)
    fig = Figure(figsize=(5,3))
    canvas = FigureCanvas(fig)
    layout.addWidget(canvas)
    def update():
        v = slider.value()/100
        gamma = 1/np.sqrt(1-v**2) if abs(v)<1 else 1
        t_tierra = 10
        t_viajero = t_tierra/gamma
        fig.clear()
        ax = fig.add_subplot(111)
        ax.bar(["Tierra","Viajero"], [t_tierra, t_viajero], color=["#1976d2","#b26500"])
        ax.set_ylim(0,12)
        ax.set_title(f"Tiempo vivido: Tierra={t_tierra:.1f} años, Viajero={t_viajero:.1f} años")
        canvas.draw()
    slider.valueChanged.connect(update)
    update()
    tab.setLayout(layout)
    return tab
