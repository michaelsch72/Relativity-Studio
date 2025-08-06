import numpy as np
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QSlider, QHBoxLayout, QFrame, QGroupBox, QScrollArea
from PyQt5.QtCore import Qt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from scipy.integrate import solve_ivp

def create_orbits_tab():
    tab = QWidget()
    layout = QVBoxLayout()
    label = QLabel("""
<div style='background:linear-gradient(120deg,#e1f5fe 60%,#b3e5fc 100%); border-radius:18px; box-shadow:0 4px 18px #0001; padding:20px 18px 18px 18px; margin-bottom:18px; font-family:Segoe UI,Arial,sans-serif;'>
<h2 style='color:#0277bd; font-size:1.7em; margin-top:0; margin-bottom:10px; letter-spacing:1px; text-shadow:0 2px 8px #0002;'>Órbitas relativistas</h2>
<div style='font-size:1.1em; margin-bottom:10px;'><b>¿Por qué las órbitas cerca de objetos masivos no son elipses perfectas?</b></div>
<div style='margin-bottom:8px;'><b>Explicación:</b> En la relatividad general, las órbitas de partículas alrededor de una masa central (como el Sol o un agujero negro) presentan precesión y pueden ser inestables o de escape, dependiendo del momento angular.</div>
<div style='margin-bottom:8px;'><b>Visualización:</b> <span style='color:#0277bd;'>Ajusta el momento angular para ver órbitas circulares, elípticas o trayectorias de escape.</span></div>
<div style='margin-bottom:8px;'><b>Fórmula:</b> <span style='background:#fffde7; border-radius:8px; padding:2px 8px; color:#b26500; font-weight:bold;'>d²u/dφ² + u = GM/L² + 3GMu²/c²</span> <span style='font-size:0.95em;'>(ecuación relativista para órbitas)</span></div>
<ul style='margin:0 0 0 18px;'>
<li><b>L:</b> momento angular</li>
<li><b>u = 1/r</b></li>
<li><b>G, M, c:</b> constantes universales</li>
</ul>
<div style='margin-bottom:8px;'><b>Historia:</b> <span style='color:#0277bd;'>La precesión del perihelio de Mercurio fue una de las primeras pruebas de la relatividad general.</span></div>
<div style='font-size:0.98em;'><b>Referencia:</b> <a href='https://es.wikipedia.org/wiki/%C3%93rbita_relativista' style='color:#0277bd; text-decoration:underline;'>Wikipedia</a></div>
</div>
        """)

import numpy as np
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QSlider, QHBoxLayout, QFrame
from PyQt5.QtCore import Qt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from scipy.integrate import solve_ivp

def create_orbits_tab():
    tab = QWidget()
    tab.setStyleSheet("""
        QWidget {
            background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 #e1f5fe, stop:1 #b3e5fc);
        }
    """)
    scroll = QScrollArea(tab)
    scroll.setWidgetResizable(True)
    content = QWidget()
    layout = QVBoxLayout(content)

    # Tarjeta didáctica
    title_box = QGroupBox("🪐 Órbitas relativistas")
    title_box.setStyleSheet("QGroupBox { font-size: 15px; font-weight: bold; color: #0277bd; border-radius: 12px; background: #e1f5fe; margin-top: 10px; padding: 10px; }")
    vbox_title = QVBoxLayout()
    exp_label = QLabel(
        "<b>¿Por qué las órbitas cerca de objetos masivos no son elipses perfectas?</b><br><br>"
        "<b>Explicación:</b> En la relatividad general, las órbitas de partículas alrededor de una masa central presentan precesión y pueden ser inestables o de escape, dependiendo del momento angular.<br>"
        "<b>Fórmula:</b> <span style='background:#fffde7; border-radius:8px; padding:2px 8px; color:#b26500; font-weight:bold;'>d²u/dφ² + u = GM/L² + 3GMu²/c²</span> (ecuación relativista para órbitas)<br>"
        "<b>L:</b> momento angular<br><b>u = 1/r</b><br><b>G, M, c:</b> constantes universales<br>"
        "<b>Ejemplo:</b> La precesión del perihelio de Mercurio fue una de las primeras pruebas de la relatividad general.<br>"
        "<b>Historia:</b> La precesión del perihelio de Mercurio fue una de las primeras pruebas de la relatividad general.<br>"
        "<b>Referencia:</b> <a href='https://es.wikipedia.org/wiki/%C3%93rbita_relativista' style='color:#0277bd; text-decoration:underline;'>Wikipedia</a>"
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
    sep.setStyleSheet("margin: 12px 0; border: 0; border-top: 2px solid #0277bd;")
    layout.addWidget(sep)

    # Mensaje explicativo de uso
    explicacion_uso = QLabel(
        "<span style='color:#0277bd; font-size:1.08em;'><b>¿Cómo usar?</b></span> "
        "Ajusta el <b>momento angular L</b> para ver cómo cambia la órbita alrededor de la masa central. "
        "¡Experimenta visualmente la precesión y la desviación de las órbitas!"
    )
    explicacion_uso.setWordWrap(True)
    explicacion_uso.setStyleSheet("background: #e1f5fe; border-radius: 10px; padding: 8px 14px; margin-bottom: 6px; font-size: 14px; color: #0277bd;")
    layout.addWidget(explicacion_uso)

    # Controles estilo Material Design
    param_box = QGroupBox()
    param_box.setStyleSheet("QGroupBox { background: transparent; border-radius: 18px; border: none; margin-top: 8px; margin-bottom: 16px; box-shadow: none; padding: 12px 18px 12px 18px; }")
    param_layout = QHBoxLayout(param_box)
    icon_label = QLabel("<span style='font-size:2.2em;'>🌀</span>")
    icon_label.setStyleSheet("margin-right: 18px; background: transparent; border: none;")
    param_layout.addWidget(icon_label)
    slider_label = QLabel("Momento angular L:")
    slider_label.setStyleSheet("font-size: 1.2em; color: #0277bd; font-weight: bold; margin-right: 10px; background: transparent; border: none; text-shadow: 0 2px 8px #4fc3f7;")
    param_layout.addWidget(slider_label)
    slider = QSlider(Qt.Horizontal)
    slider.setMinimum(35)
    slider.setMaximum(100)
    slider.setValue(50)
    slider.setTickInterval(1)
    slider.setTickPosition(QSlider.TicksBelow)
    slider.setStyleSheet("""
        QSlider { background: transparent; }
        QSlider::groove:horizontal { height: 10px; background: #b3e5fc; border-radius: 5px; }
        QSlider::handle:horizontal { background: #0277bd; border: 2px solid #4fc3f7; width: 22px; height: 22px; border-radius: 11px; margin: -7px 0; }
        QSlider::sub-page:horizontal { background: #4fc3f7; border-radius: 5px; }
        QSlider::add-page:horizontal { background: #e1f5fe; border-radius: 5px; }
    """)
    param_layout.addWidget(slider, stretch=2)
    value_label = QLabel("5.0")
    value_label.setStyleSheet("background: #0277bd; color: #fff; border-radius: 50%; font-weight:bold; font-size:1.3em; padding: 10px 18px; margin-left: 18px; box-shadow: 0 2px 8px #4fc3f7;")
    param_layout.addWidget(value_label)
    layout.addWidget(param_box)

    # Información comparativa
    info_label = QLabel()
    info_label.setWordWrap(True)
    info_label.setStyleSheet("background:#fffde7; border-radius:12px; box-shadow:0 2px 8px #ffd54f; padding:12px; font-size:1.1em; margin:10px 0;")
    layout.addWidget(info_label)
    fig = Figure(figsize=(8,5))
    canvas = FigureCanvas(fig)
    canvas.setMinimumHeight(400)
    canvas.setStyleSheet("border-radius:18px; box-shadow:0 2px 18px #4fc3f7; margin:16px 0 6px 0; background: #e1f5fe;")
    layout.addWidget(canvas)
    def orbit_rhs(phi, y, L):
        r, pr = y
        rs = 1.0
        f = 1 - rs/r
        dpr = (L**2/r**3 - rs*L**2/r**4) - rs/(2*r**2)*pr**2/f
        dr = pr
        return [dr, dpr/f]
    def plot_orbit():
        L = slider.value() / 10
        value_label.setText(f"{L:.1f}")
        r0 = 10.0
        pr0 = 0.0
        y0 = [r0, pr0]
        phis = np.linspace(0, 24*np.pi, 4000)
        try:
            sol = solve_ivp(lambda phi, y: orbit_rhs(phi, y, L), [phis[0], phis[-1]], y0, t_eval=phis, rtol=1e-7, atol=1e-9)
            r = sol.y[0]
            phi = sol.t
            mask = r > 1.01
            if not np.any(mask):
                raise ValueError("La partícula cae en el horizonte de eventos.")
            x = r[mask] * np.cos(phi[mask])
            y = r[mask] * np.sin(phi[mask])
            info_label.setText(f"<b>Ejemplo:</b> Para L = {L:.1f}, la órbita muestra precesión y desviación.")
            fig.clear()
            ax = fig.add_subplot(111)
            ax.plot(x, y, color='#0277bd', label="Órbita relativista", linewidth=2)
            ax.plot(0, 0, 'ko', markersize=10, label="Masa central")
            ax.set_aspect('equal')
            ax.set_xlabel("x", fontsize=12, color="#0277bd")
            ax.set_ylabel("y", fontsize=12, color="#0277bd")
            ax.set_title("Órbita en Schwarzschild", fontsize=16, color="#0277bd", pad=12)
            ax.legend(fontsize=12)
            ax.grid(True, alpha=0.3)
            ax.annotate("Precesión del perihelio", xy=(x[0], y[0]), xytext=(x[0]+2, y[0]+2), arrowprops=dict(facecolor='#0277bd', shrink=0.05), fontsize=12, color='#0277bd', weight='bold')
            canvas.draw()
        except Exception as e:
            info_label.setText(f"<span style='color:red;'>Error en la integración: {str(e)}</span>")
            fig.clear()
            ax = fig.add_subplot(111)
            ax.text(0.5, 0.5, f"Error en la integración:\n{str(e)}", ha='center', va='center', fontsize=12, color='red', transform=ax.transAxes)
            ax.set_xticks([])
            ax.set_yticks([])
            canvas.draw()
    slider.valueChanged.connect(plot_orbit)
    value_label.setText(f"{slider.value()/10:.1f}")
    plot_orbit()

    # Explicación didáctica debajo del gráfico
    explicacion_grafico = QLabel(
        "<span style='color:#0277bd;'><b>¿Qué muestra este gráfico?</b></span> "
        "La curva muestra la órbita real de una partícula en el espacio-tiempo curvo de Schwarzschild. "
        "El punto central es la masa, y puedes experimentar cambiando el momento angular para ver la precesión y la desviación."
    )
    explicacion_grafico.setWordWrap(True)
    explicacion_grafico.setStyleSheet("background: #e1f5fe; border-radius: 10px; padding: 10px 16px; margin: 8px 0 12px 0; font-size: 14px; color: #0277bd;")
    layout.addWidget(explicacion_grafico)

    scroll.setWidget(content)
    tab_layout = QVBoxLayout(tab)
    tab_layout.addWidget(scroll)
    tab.setLayout(tab_layout)
    return tab
