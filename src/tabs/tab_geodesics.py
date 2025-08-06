import numpy as np
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QSlider, QHBoxLayout, QComboBox, QFrame, QGroupBox, QScrollArea
from PyQt5.QtCore import Qt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from scipy.integrate import solve_ivp

def create_numeric_geodesics_tab():
    tab = QWidget()
    tab.setStyleSheet("""
        QWidget {
            background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 #e0f7fa, stop:1 #b2ebf2);
        }
    """)
    scroll = QScrollArea(tab)
    scroll.setWidgetResizable(True)
    content = QWidget()
    layout = QVBoxLayout(content)

    # Tarjeta didáctica
    title_box = QGroupBox("🛰️ Geodésicas numéricas (Schwarzschild)")
    title_box.setStyleSheet("QGroupBox { font-size: 15px; font-weight: bold; color: #00897b; border-radius: 12px; background: #e0f7fa; margin-top: 10px; padding: 10px; }")
    vbox_title = QVBoxLayout()
    exp_label = QLabel(
        "<b>¿Cómo se mueven la luz y las partículas en el espacio-tiempo curvo?</b><br><br>"
        "<b>Explicación:</b> Las geodésicas son las trayectorias más 'rectas' posibles en un espacio-tiempo curvado. En Schwarzschild, describen cómo la gravedad afecta el movimiento de la luz y de las partículas.<br>"
        "<b>Fórmulas:</b> <span style='background:#fffde7; border-radius:8px; padding:2px 8px; color:#b26500; font-weight:bold;'>d²r/dφ² = r - 3rₛ/2</span> (luz), para partículas: ecuación similar, pero con energía y masa.<br>"
        "<b>Ejemplo:</b> La precesión del perihelio de Mercurio y la deflexión de la luz se explican con geodésicas.<br>"
        "<b>Historia:</b> El cálculo de geodésicas permitió predecir la precesión del perihelio de Mercurio y la deflexión de la luz.<br>"
        "<b>Referencia:</b> <a href='https://es.wikipedia.org/wiki/Geod%C3%A9sica' style='color:#00897b; text-decoration:underline;'>Wikipedia</a>"
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
    sep.setStyleSheet("margin: 12px 0; border: 0; border-top: 2px solid #00897b;")
    layout.addWidget(sep)

    # Mensaje explicativo de uso
    explicacion_uso = QLabel(
        "<span style='color:#00897b; font-size:1.08em;'><b>¿Cómo usar?</b></span> "
        "Ajusta el <b>parámetro de impacto b</b> y elige el tipo de partícula para ver la trayectoria real. "
        "¡Experimenta visualmente cómo la gravedad curva el espacio-tiempo!"
    )
    explicacion_uso.setWordWrap(True)
    explicacion_uso.setStyleSheet("background: #e0f7fa; border-radius: 10px; padding: 8px 14px; margin-bottom: 6px; font-size: 14px; color: #00897b;")
    layout.addWidget(explicacion_uso)

    # Controles estilo Material Design
    param_box = QGroupBox()
    param_box.setStyleSheet("QGroupBox { background: transparent; border-radius: 18px; border: none; margin-top: 8px; margin-bottom: 16px; box-shadow: none; padding: 12px 18px 12px 18px; }")
    param_layout = QHBoxLayout(param_box)
    icon_label = QLabel("<span style='font-size:2.2em;'>🌠</span>")
    icon_label.setStyleSheet("margin-right: 18px; background: transparent; border: none;")
    param_layout.addWidget(icon_label)
    slider_label = QLabel("Parámetro de impacto b:")
    slider_label.setStyleSheet("font-size: 1.2em; color: #00897b; font-weight: bold; margin-right: 10px; background: transparent; border: none; text-shadow: 0 2px 8px #4dd0e1;")
    param_layout.addWidget(slider_label)
    slider = QSlider(Qt.Horizontal)
    slider.setMinimum(15)
    slider.setMaximum(100)
    slider.setValue(30)
    slider.setTickInterval(1)
    slider.setTickPosition(QSlider.TicksBelow)
    slider.setStyleSheet("""
        QSlider { background: transparent; }
        QSlider::groove:horizontal { height: 10px; background: #b2ebf2; border-radius: 5px; }
        QSlider::handle:horizontal { background: #00897b; border: 2px solid #4dd0e1; width: 22px; height: 22px; border-radius: 11px; margin: -7px 0; }
        QSlider::sub-page:horizontal { background: #4dd0e1; border-radius: 5px; }
        QSlider::add-page:horizontal { background: #e0f7fa; border-radius: 5px; }
    """)
    param_layout.addWidget(slider, stretch=2)
    value_label = QLabel("3.0")
    value_label.setStyleSheet("background: #00897b; color: #fff; border-radius: 50%; font-weight:bold; font-size:1.3em; padding: 10px 18px; margin-left: 18px; box-shadow: 0 2px 8px #4dd0e1;")
    param_layout.addWidget(value_label)
    type_label = QLabel("Tipo:")
    type_label.setStyleSheet("font-size: 1.1em; color: #00897b; font-weight: bold; margin-left: 18px; background: transparent; border: none;")
    param_layout.addWidget(type_label)
    type_combo = QComboBox()
    type_combo.addItems(["Luz", "Partícula con masa"])
    type_combo.setStyleSheet("font-size: 1.1em; color: #00897b; background: #e0f7fa; border-radius: 8px; padding: 4px 12px; margin-left: 8px;")
    param_layout.addWidget(type_combo)
    layout.addWidget(param_box)

    # Información comparativa
    info_label = QLabel()
    info_label.setWordWrap(True)
    info_label.setStyleSheet("background:#fffde7; border-radius:12px; box-shadow:0 2px 8px #ffd54f; padding:12px; font-size:1.1em; margin:10px 0;")
    layout.addWidget(info_label)
    fig = Figure(figsize=(8,5))
    canvas = FigureCanvas(fig)
    canvas.setMinimumHeight(400)
    canvas.setStyleSheet("border-radius:18px; box-shadow:0 2px 18px #4dd0e1; margin:16px 0 6px 0; background: #e0f7fa;")
    layout.addWidget(canvas)
    def geodesic_rhs(phi, y, b, is_light):
        r, pr = y
        rs = 1.0
        if is_light:
            E = 1.0
            L = b
            f = 1 - rs/r
            dpr = (L**2/r**3 - rs*L**2/r**4)
            dr = pr
            return [dr, dpr/f]
        else:
            E = 1.0
            L = b
            f = 1 - rs/r
            dpr = (L**2/r**3 - rs*L**2/r**4) - rs/(2*r**2)*pr**2/f
            dr = pr
            return [dr, dpr/f]
    def plot_geodesic():
        b = slider.value() / 10
        value_label.setText(f"{b:.1f}")
        is_light = (type_combo.currentIndex() == 0)
        r0 = 10.0
        pr0 = -0.1 if is_light else 0.0
        y0 = [r0, pr0]
        phis = np.linspace(0, 8*np.pi, 2000)
        try:
            sol = solve_ivp(lambda phi, y: geodesic_rhs(phi, y, b, is_light), [phis[0], phis[-1]], y0, t_eval=phis, rtol=1e-6)
            r = sol.y[0]
            phi = sol.t
            mask = r > 1.01
            if not np.any(mask):
                raise ValueError("La trayectoria cae en el horizonte de eventos.")
            x = r[mask] * np.cos(phi[mask])
            y = r[mask] * np.sin(phi[mask])
            info_label.setText(f"<b>Ejemplo:</b> Para b = {b:.1f}, la trayectoria es <span style='color:#00897b;'>{'luz' if is_light else 'partícula con masa'}</span>.")
            fig.clear()
            ax = fig.add_subplot(111)
            ax.plot(x, y, label="Trayectoria", linewidth=2)
            ax.plot(0, 0, 'ko', markersize=10, label="Masa central")
            ax.set_aspect('equal')
            ax.set_xlabel("x", fontsize=12, color="#00897b")
            ax.set_ylabel("y", fontsize=12, color="#00897b")
            ax.set_title("Geodésica en Schwarzschild", fontsize=16, color="#00897b", pad=12)
            ax.legend(fontsize=12)
            ax.grid(True, alpha=0.3)
            ax.annotate("Horizonte de eventos", xy=(0,0), xytext=(2,2), arrowprops=dict(facecolor='#00897b', shrink=0.05), fontsize=12, color='#00897b', weight='bold')
            canvas.draw()
        except Exception as e:
            info_label.setText(f"<span style='color:red;'>Error en la integración: {str(e)}</span>")
            fig.clear()
            ax = fig.add_subplot(111)
            ax.text(0.5, 0.5, f"Error en la integración:\n{str(e)}", ha='center', va='center', fontsize=12, color='red', transform=ax.transAxes)
            ax.set_xticks([])
            ax.set_yticks([])
            canvas.draw()
    slider.valueChanged.connect(plot_geodesic)
    type_combo.currentIndexChanged.connect(plot_geodesic)
    value_label.setText(f"{slider.value()/10:.1f}")
    plot_geodesic()

    # Explicación didáctica debajo del gráfico
    explicacion_grafico = QLabel(
        "<span style='color:#00897b;'><b>¿Qué muestra este gráfico?</b></span> "
        "La curva representa la trayectoria real de la luz o una partícula en el espacio-tiempo curvo de Schwarzschild. "
        "El punto central es la masa, y el horizonte de eventos es el límite donde nada puede escapar. "
        "Puedes experimentar cambiando el parámetro de impacto y el tipo de partícula."
    )
    explicacion_grafico.setWordWrap(True)
    explicacion_grafico.setStyleSheet("background: #e0f7fa; border-radius: 10px; padding: 10px 16px; margin: 8px 0 12px 0; font-size: 14px; color: #00897b;")
    layout.addWidget(explicacion_grafico)

    scroll.setWidget(content)
    tab_layout = QVBoxLayout(tab)
    tab_layout.addWidget(scroll)
    tab.setLayout(tab_layout)
    return tab
