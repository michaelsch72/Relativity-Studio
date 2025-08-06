import numpy as np
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QSlider, QHBoxLayout, QFrame, QGroupBox, QScrollArea
from PyQt5.QtCore import Qt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

def create_light_deflection_tab():
    tab = QWidget()
    tab.setStyleSheet("""
        QWidget {
            background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 #fffde7, stop:1 #ffe0b2);
        }
    """)
    scroll = QScrollArea(tab)
    scroll.setWidgetResizable(True)
    content = QWidget()
    layout = QVBoxLayout(content)

    # Tarjeta didáctica
    title_box = QGroupBox("🌠 Deflexión de la luz")
    title_box.setStyleSheet("QGroupBox { font-size: 15px; font-weight: bold; color: #ef6c00; border-radius: 12px; background: #fffde7; margin-top: 10px; padding: 10px; }")
    vbox_title = QVBoxLayout()
    exp_label = QLabel(
        "<b>¿Por qué la luz se curva cerca de una masa?</b><br><br>"
        "<b>Explicación:</b> La relatividad general predice que la luz sigue geodésicas en el espacio-tiempo curvado. Al pasar cerca de una masa, su trayectoria se desvía.<br>"
        "<b>Visualización:</b> <span style='color:#ef6c00;'>Ajusta el parámetro de impacto para ver cómo cambia la desviación.</span><br>"
        "<b>Fórmula:</b> <span style='background:#fffde7; border-radius:8px; padding:2px 8px; color:#b26500; font-weight:bold;'>Δφ ≈ 4GM/(c²b)</span> <span style='font-size:0.95em;'>(aproximación para campos débiles)</span><br>"
        "<b>Δφ:</b> ángulo de deflexión<br><b>b:</b> parámetro de impacto<br><b>G, M, c:</b> constantes universales<br>"
        "<b>Historia:</b> La deflexión de la luz fue confirmada en 1919 durante un eclipse solar, validando la teoría de Einstein.<br>"
        "<b>Referencia:</b> <a href='https://es.wikipedia.org/wiki/Deflexi%C3%B3n_de_la_luz' style='color:#ef6c00; text-decoration:underline;'>Wikipedia</a>"
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
    sep.setStyleSheet("margin: 12px 0; border: 0; border-top: 2px solid #ef6c00;")
    layout.addWidget(sep)

    # Mensaje explicativo de uso
    explicacion_uso = QLabel(
        "<span style='color:#ef6c00; font-size:1.08em;'><b>¿Cómo usar?</b></span> "
        "Ajusta el <b>parámetro de impacto b</b> para ver cómo cambia la desviación de la luz al pasar cerca de la masa central. "
        "¡Experimenta visualmente la predicción de Einstein!"
    )
    explicacion_uso.setWordWrap(True)
    explicacion_uso.setStyleSheet("background: #fffde7; border-radius: 10px; padding: 8px 14px; margin-bottom: 6px; font-size: 14px; color: #ef6c00;")
    layout.addWidget(explicacion_uso)

    # Controles estilo Material Design
    param_box = QGroupBox()
    param_box.setStyleSheet("QGroupBox { background: transparent; border-radius: 18px; border: none; margin-top: 8px; margin-bottom: 16px; box-shadow: none; padding: 12px 18px 12px 18px; }")
    param_layout = QHBoxLayout(param_box)
    icon_label = QLabel("<span style='font-size:2.2em;'>💡</span>")
    icon_label.setStyleSheet("margin-right: 18px; background: transparent; border: none;")
    param_layout.addWidget(icon_label)
    slider_label = QLabel("Parámetro de impacto b:")
    slider_label.setStyleSheet("font-size: 1.2em; color: #ef6c00; font-weight: bold; margin-right: 10px; background: transparent; border: none; text-shadow: 0 2px 8px #ffd54f;")
    param_layout.addWidget(slider_label)
    slider = QSlider(Qt.Horizontal)
    slider.setMinimum(15)
    slider.setMaximum(100)
    slider.setValue(30)
    slider.setTickInterval(1)
    slider.setTickPosition(QSlider.TicksBelow)
    slider.setStyleSheet("""
        QSlider { background: transparent; }
        QSlider::groove:horizontal { height: 10px; background: #ffe0b2; border-radius: 5px; }
        QSlider::handle:horizontal { background: #ef6c00; border: 2px solid #ffd54f; width: 22px; height: 22px; border-radius: 11px; margin: -7px 0; }
        QSlider::sub-page:horizontal { background: #ffd54f; border-radius: 5px; }
        QSlider::add-page:horizontal { background: #fffde7; border-radius: 5px; }
    """)
    param_layout.addWidget(slider, stretch=2)
    value_label = QLabel("3.0")
    value_label.setStyleSheet("background: #ef6c00; color: #fff; border-radius: 50%; font-weight:bold; font-size:1.3em; padding: 10px 18px; margin-left: 18px; box-shadow: 0 2px 8px #ffd54f;")
    param_layout.addWidget(value_label)
    layout.addWidget(param_box)

    # Información comparativa
    info_label = QLabel()
    info_label.setWordWrap(True)
    info_label.setStyleSheet("background:#fffde7; border-radius:12px; box-shadow:0 2px 8px #ffd54f; padding:12px; font-size:1.1em; margin:10px 0;")
    layout.addWidget(info_label)
    fig = Figure(figsize=(6,5))
    canvas = FigureCanvas(fig)
    canvas.setMinimumHeight(400)
    canvas.setStyleSheet("border-radius:18px; box-shadow:0 2px 18px #ffd54f; margin:16px 0 6px 0; background: #fffde7;")
    layout.addWidget(canvas)

    def plot_deflection():
        b = slider.value() / 10
        value_label.setText(f"{b:.1f}")
        rs = 1.0
        r0 = 10.0
        phi = np.linspace(-np.pi/2, np.pi/2, 500)
        # Trayectoria recta (sin masa)
        x0 = b * np.ones_like(phi)
        y0 = r0 * np.tan(phi)
        # Trayectoria desviada (aprox. 1er orden)
        delta = 2 * rs / b  # ángulo de deflexión aproximado
        x1 = b * np.ones_like(phi)
        y1 = r0 * np.tan(phi + delta/2 * np.sign(phi))
        fig.clear()
        ax = fig.add_subplot(111)
        ax.plot(x0, y0, 'b--', label="Sin masa (recta)")
        ax.plot(x1, y1, 'r', label="Con masa (desviada)")
        ax.plot(0, 0, 'ko', markersize=10, label="Masa central")
        ax.set_xlabel("x", fontsize=12, color="#ef6c00")
        ax.set_ylabel("y", fontsize=12, color="#ef6c00")
        ax.set_title("Deflexión de la luz por gravedad", fontsize=16, color="#ef6c00", pad=12)
        ax.legend(fontsize=12)
        ax.grid(True, alpha=0.3)
        ax.annotate("Masa central", xy=(0,0), xytext=(2,2), arrowprops=dict(facecolor='#ef6c00', shrink=0.05), fontsize=12, color='#ef6c00', weight='bold')
        canvas.draw()

    slider.valueChanged.connect(plot_deflection)
    value_label.setText(f"{slider.value()/10:.1f}")
    plot_deflection()

    # Explicación didáctica debajo del gráfico
    explicacion_grafico = QLabel(
        "<span style='color:#ef6c00;'><b>¿Qué muestra este gráfico?</b></span> "
        "La curva roja muestra cómo la luz se desvía al pasar cerca de una masa, mientras que la azul sería la trayectoria sin masa. "
        "El punto central es la masa responsable de la curvatura. "
        "Puedes experimentar cambiando el parámetro de impacto para ver el efecto de la gravedad."
    )
    explicacion_grafico.setWordWrap(True)
    explicacion_grafico.setStyleSheet("background: #fffde7; border-radius: 10px; padding: 10px 16px; margin: 8px 0 12px 0; font-size: 14px; color: #ef6c00;")
    layout.addWidget(explicacion_grafico)

    scroll.setWidget(content)
    tab_layout = QVBoxLayout(tab)
    tab_layout.addWidget(scroll)
    tab.setLayout(tab_layout)
    return tab
