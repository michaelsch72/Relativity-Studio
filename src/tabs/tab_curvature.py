import numpy as np
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QSlider, QHBoxLayout, QFrame, QGroupBox, QScrollArea
from PyQt5.QtCore import Qt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

def create_curvature_tab():
    tab = QWidget()
    tab.setStyleSheet("""
        QWidget {
            background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 #ede7f6, stop:1 #b39ddb);
        }
    """)
    from PyQt5.QtWidgets import QGroupBox, QScrollArea, QSizePolicy
    scroll = QScrollArea(tab)
    scroll.setWidgetResizable(True)
    content = QWidget()
    layout = QVBoxLayout(content)

    # Título y explicación didáctica
    title_box = QGroupBox("🌌 Curvatura del espacio-tiempo")
    title_box.setStyleSheet("QGroupBox { font-size: 15px; font-weight: bold; color: #6a1b9a; border-radius: 12px; background: #ede7f6; margin-top: 10px; padding: 10px; }")
    vbox_title = QVBoxLayout()
    exp_label = QLabel(
        "<b>¿Cómo se deforma el espacio-tiempo cerca de una masa?</b><br><br>"
        "<b>Explicación:</b> La relatividad general describe la gravedad como la curvatura del espacio-tiempo causada por la masa y la energía. Cerca de una masa puntual, el espacio se 'hunde' y las trayectorias de los objetos se curvan.<br>"
        "<b>Fórmula:</b> z(r) = 2√[rₛ(r - rₛ)]<br>"
        "<b>z(r):</b> altura de la superficie embebida<br><b>rₛ:</b> radio de Schwarzschild<br><b>r:</b> distancia radial<br>"
        "<b>Ejemplo:</b> Si rₛ aumenta, la 'profundidad' de la curvatura es mayor y las trayectorias se desvían más.<br>"
        "<b>Historia:</b> Esta visualización fue propuesta por Flamm en 1916, poco después de la publicación de la teoría de Einstein.<br>"
        "<b>Referencia:</b> <a href='https://es.wikipedia.org/wiki/Soluci%C3%B3n_de_Schwarzschild' style='color:#6a1b9a; text-decoration:underline;'>Wikipedia</a>"
    )
    exp_label.setOpenExternalLinks(True)
    exp_label.setTextFormat(Qt.RichText)
    exp_label.setWordWrap(True)
    exp_label.setStyleSheet("font-size: 15px; color: #333; margin: 0;")
    vbox_title.addWidget(exp_label)
    title_box.setLayout(vbox_title)
    layout.addWidget(title_box)

    # Separador visual
    sep = QFrame()
    sep.setFrameShape(QFrame.HLine)
    sep.setFrameShadow(QFrame.Sunken)
    sep.setStyleSheet("margin: 12px 0; border: 0; border-top: 2px solid #b39ddb;")
    layout.addWidget(sep)

    # Mensaje explicativo de uso
    explicacion_uso = QLabel(
        "<span style='color:#6a1b9a; font-size:1.08em;'><b>¿Cómo usar?</b></span> "
        "Ajusta el <b>radio de Schwarzschild rₛ</b> con el control deslizante y observa cómo cambia la curvatura y el gráfico en tiempo real. "
        "¡Experimenta visualmente la geometría del espacio-tiempo!"
    )
    explicacion_uso.setWordWrap(True)
    explicacion_uso.setStyleSheet("background: #ede7f6; border-radius: 10px; padding: 8px 14px; margin-bottom: 6px; font-size: 14px; color: #6a1b9a;")
    layout.addWidget(explicacion_uso)

    # Controles estilo Material Design
    param_box = QGroupBox()
    param_box.setStyleSheet("QGroupBox { background: transparent; border-radius: 18px; border: none; margin-top: 8px; margin-bottom: 16px; box-shadow: none; padding: 12px 18px 12px 18px; }")
    param_layout = QHBoxLayout(param_box)
    icon_label = QLabel("<span style='font-size:2.2em;'>🌀</span>")
    icon_label.setStyleSheet("margin-right: 18px; background: transparent; border: none;")
    param_layout.addWidget(icon_label)
    slider_label = QLabel("Radio de Schwarzschild rₛ:")
    slider_label.setStyleSheet("font-size: 1.2em; color: #6a1b9a; font-weight: bold; margin-right: 10px; background: transparent; border: none; text-shadow: 0 2px 8px #b39ddb;")
    param_layout.addWidget(slider_label)
    slider = QSlider(Qt.Horizontal)
    slider.setMinimum(5)
    slider.setMaximum(50)
    slider.setValue(10)
    slider.setTickInterval(1)
    slider.setTickPosition(QSlider.TicksBelow)
    slider.setStyleSheet("""
        QSlider { background: transparent; }
        QSlider::groove:horizontal { height: 10px; background: #d1c4e9; border-radius: 5px; }
        QSlider::handle:horizontal { background: #8e24aa; border: 2px solid #6a1b9a; width: 22px; height: 22px; border-radius: 11px; margin: -7px 0; }
        QSlider::sub-page:horizontal { background: #b39ddb; border-radius: 5px; }
        QSlider::add-page:horizontal { background: #ede7f6; border-radius: 5px; }
    """)
    param_layout.addWidget(slider, stretch=2)
    value_label = QLabel("1.0")
    value_label.setStyleSheet("background: #6a1b9a; color: #fff; border-radius: 50%; font-weight:bold; font-size:1.3em; padding: 10px 18px; margin-left: 18px; box-shadow: 0 2px 8px #b39ddb;")
    param_layout.addWidget(value_label)
    layout.addWidget(param_box)

    # Información comparativa
    info_label = QLabel()
    info_label.setWordWrap(True)
    info_label.setStyleSheet("background:#fffde7; border-radius:12px; box-shadow:0 2px 8px #ffd54f; padding:12px; font-size:1.1em; margin:10px 0;")
    layout.addWidget(info_label)
    fig = Figure(figsize=(10, 4.5))
    canvas = FigureCanvas(fig)
    canvas.setMinimumHeight(420)
    canvas.setStyleSheet("border-radius:18px; box-shadow:0 2px 18px #b39ddb; margin:16px 0 6px 0; background: #f3e5f5;")
    layout.addWidget(canvas)

    def plot_curvature():
        rs = slider.value() / 10
        value_label.setText(f"{rs:.1f}")
        r = np.linspace(rs + 0.01, rs * 6, 400)
        z = 2 * np.sqrt(rs * (r - rs))
        info_label.setText(f"<b>Ejemplo:</b> Para rₛ = {rs:.1f}, la curvatura máxima es <span style='color:#6a1b9a;'>{np.max(z):.2f}</span>.")
        fig.clear()
        ax = fig.add_subplot(111)
        ax.plot(r, z, color='#6a1b9a', linewidth=3, label="Superficie embebida")
        ax.scatter([rs*2], [2*np.sqrt(rs*(rs*2-rs))], color='#d500f9', s=100, zorder=5, label="Ejemplo r = 2rₛ")
        ax.set_xlabel("r (radio)", fontsize=14, color='#6a1b9a')
        ax.set_ylabel("z (curvatura)", fontsize=14, color='#6a1b9a')
        ax.set_title(f"Curvatura del espacio-tiempo (rₛ = {rs:.1f})", fontsize=18, color='#4a148c', pad=12)
        ax.legend(fontsize=12)
        ax.grid(True, alpha=0.3)
        ax.tick_params(axis='x', labelsize=12, colors='#6a1b9a')
        ax.tick_params(axis='y', labelsize=12, colors='#6a1b9a')
        ax.annotate(f"Curvatura máxima: {np.max(z):.2f}", xy=(r[np.argmax(z)], np.max(z)), xytext=(r[np.argmax(z)]+1, np.max(z)-1),
                    arrowprops=dict(facecolor='#6a1b9a', shrink=0.05), fontsize=13, color='#4a148c', weight='bold')
        canvas.draw()
    # ...

    slider.valueChanged.connect(plot_curvature)
    value_label.setText(f"{slider.value()/10:.1f}")
    plot_curvature()

    # Explicación didáctica debajo del gráfico
    explicacion_grafico = QLabel(
        "<span style='color:#6a1b9a;'><b>¿Qué muestra este gráfico?</b></span> "
        "La curva representa cómo se <b>hunde</b> el espacio-tiempo cerca de una masa según la Relatividad General. "
        "No es una forma real del espacio, sino una analogía visual para entender la curvatura causada por la gravedad. "
        "El punto destacado muestra el doble del radio de Schwarzschild, una referencia clásica en la teoría."
    )
    explicacion_grafico.setWordWrap(True)
    explicacion_grafico.setStyleSheet("background: #ede7f6; border-radius: 10px; padding: 10px 16px; margin: 8px 0 12px 0; font-size: 14px; color: #6a1b9a;")
    layout.addWidget(explicacion_grafico)

    scroll.setWidget(content)
    tab_layout = QVBoxLayout(tab)
    tab_layout.addWidget(scroll)
    tab.setLayout(tab_layout)
    return tab
