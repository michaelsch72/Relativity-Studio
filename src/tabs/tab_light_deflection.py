import numpy as np
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QSlider, QHBoxLayout, QComboBox, QFrame, QGroupBox, QScrollArea
from PyQt5.QtCore import Qt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from mpl_toolkits.mplot3d import Axes3D

def create_light_deflection_tab():
    tab = QWidget()
    tab.setStyleSheet("""
        QWidget {
            background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 #fffde7, stop:1 #ffe082);
        }
    """)
    scroll = QScrollArea(tab)
    scroll.setWidgetResizable(True)
    content = QWidget()
    layout = QVBoxLayout(content)

    # Título y explicación
    title_box = QGroupBox("🌠 Deflexión de la luz por gravedad")
    title_box.setStyleSheet("QGroupBox { font-size: 15px; font-weight: bold; color: #b26500; border-radius: 12px; background: #fffde7; margin-top: 10px; padding: 10px; }")
    vbox_title = QVBoxLayout()
    exp_label = QLabel(
        "<b>¿Cómo se curva la luz cerca de una masa?</b><br><br>"
        "<b>Explicación:</b> La luz se desvía al pasar cerca de una masa debido a la curvatura del espacio-tiempo.<br>"
        "<b>Fórmula (aprox.):</b> Δθ ≈ 4GM/(c²b)<br>"
        "<b>Ejemplo:</b> La luz de las estrellas se curva al pasar cerca del Sol.<br>"
        "<b>Historia:</b> Confirmado en 1919 por Eddington.<br>"
        "<b>Referencia:</b> <a href='https://es.wikipedia.org/wiki/Deflexi%C3%B3n_de_la_luz' style='color:#b26500; text-decoration:underline;'>Wikipedia</a>"
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
    sep.setStyleSheet("margin: 12px 0; border: 0; border-top: 2px solid #ffd54f;")
    layout.addWidget(sep)

    # Mensaje explicativo de uso
    explicacion_uso = QLabel(
        "<span style='color:#b26500; font-size:1.08em;'><b>¿Cómo usar?</b></span> "
        "Ajusta el <b>parámetro de impacto b</b> para ver cómo varía la deflexión de la luz. "
        "Puedes visualizar la trayectoria en 2D o 3D."
    )
    explicacion_uso.setWordWrap(True)
    explicacion_uso.setStyleSheet("background: #fffde7; border-radius: 10px; padding: 8px 14px; margin-bottom: 6px; font-size: 14px; color: #b26500;")
    layout.addWidget(explicacion_uso)

    # Controles
    param_box = QGroupBox()
    param_box.setStyleSheet("QGroupBox { background: transparent; border-radius: 18px; border: none; margin-top: 8px; margin-bottom: 16px; box-shadow: none; padding: 12px 18px 12px 18px; }")
    param_layout = QHBoxLayout(param_box)
    icon_label = QLabel("<span style='font-size:2.2em;'>💡</span>")
    icon_label.setStyleSheet("margin-right: 18px; background: transparent; border: none;")
    param_layout.addWidget(icon_label)
    slider_label = QLabel("Parámetro de impacto b:")
    slider_label.setStyleSheet("font-size: 1.2em; color: #b26500; font-weight: bold; margin-right: 10px; background: transparent; border: none; text-shadow: 0 2px 8px #ffd54f;")
    param_layout.addWidget(slider_label)
    slider = QSlider(Qt.Horizontal)
    slider.setMinimum(15)
    slider.setMaximum(100)
    slider.setValue(30)
    slider.setTickInterval(1)
    slider.setTickPosition(QSlider.TicksBelow)
    slider.setStyleSheet("""
        QSlider { background: transparent; }
        QSlider::groove:horizontal { height: 10px; background: #ffe082; border-radius: 5px; }
        QSlider::handle:horizontal { background: #b26500; border: 2px solid #ffd54f; width: 22px; height: 22px; border-radius: 11px; margin: -7px 0; }
        QSlider::sub-page:horizontal { background: #ffd54f; border-radius: 5px; }
        QSlider::add-page:horizontal { background: #fffde7; border-radius: 5px; }
    """)
    param_layout.addWidget(slider, stretch=2)
    value_label = QLabel("3.0")
    value_label.setStyleSheet("background: #b26500; color: #fff; border-radius: 50%; font-weight:bold; font-size:1.3em; padding: 10px 18px; margin-left: 18px; box-shadow: 0 2px 8px #ffd54f;")
    param_layout.addWidget(value_label)

    # Selector de gráfico 2D/3D alineado a la derecha
    graph_label = QLabel("Gráfico:")
    graph_label.setStyleSheet("font-size: 1.1em; color: #b26500; font-weight: bold; margin-left: 18px; margin-right: 8px;")
    param_layout.addWidget(graph_label)
    graph_select = QComboBox()
    graph_select.addItems(["2D", "3D"])
    graph_select.setStyleSheet("""
        QComboBox {
            font-size: 1.1em;
            background: #fffde7;
            color: #b26500;
            border: 1.5px solid #ffd54f;
            border-radius: 8px;
            padding: 4px 18px 4px 12px;
            min-width: 70px;
        }
        QComboBox QAbstractItemView {
            background: #fffde7;
            color: #b26500;
            selection-background-color: #ffd54f;
        }
    """)
    param_layout.addWidget(graph_select)
    layout.addWidget(param_box)

    # Información comparativa
    info_label = QLabel()
    info_label.setWordWrap(True)
    info_label.setStyleSheet("background:#fffde7; border-radius:12px; box-shadow:0 2px 8px #ffd54f; padding:12px; font-size:1.1em; margin:10px 0;")
    layout.addWidget(info_label)
    fig = Figure(figsize=(8,5))
    canvas = FigureCanvas(fig)
    canvas.setMinimumHeight(400)
    canvas.setStyleSheet("border-radius:18px; box-shadow:0 2px 18px #ffd54f; margin:16px 0 6px 0; background: #fffde7;")
    layout.addWidget(canvas)

    def deflection_rhs(phi, y, b):
        r, pr = y
        rs = 1.0
        L = b
        f = 1 - rs/r
        dpr = (L**2/r**3 - rs*L**2/r**4)
        dr = pr
        return [dr, dpr/f]

    def plot_deflection():
        b = slider.value() / 10
        value_label.setText(f"{b:.1f}")
        r0 = 10.0
        pr0 = -0.1
        y0 = [r0, pr0]
        phis = np.linspace(0, 6*np.pi, 2000)
        try:
            from scipy.integrate import solve_ivp
            sol = solve_ivp(lambda phi, y: deflection_rhs(phi, y, b), [phis[0], phis[-1]], y0, t_eval=phis, rtol=1e-6)
            r = sol.y[0]
            phi = sol.t
            mask = r > 1.01
            if not np.any(mask):
                raise ValueError("La trayectoria cae en el horizonte de eventos.")
            x = r[mask] * np.cos(phi[mask])
            y = r[mask] * np.sin(phi[mask])
            delta_theta = 4 / b  # Aproximación para rs=1, G=c=1
            info_label.setText(f"<b>Ejemplo:</b> Para b = {b:.1f}, la deflexión aproximada es <span style='color:#b26500;'>{delta_theta:.3f} rad</span>.")
            fig.clear()
            if graph_select.currentText() == "2D":
                ax = fig.add_subplot(111)
                ax.plot(x, y, label="Trayectoria de la luz", linewidth=2, color="#b26500")
                ax.plot(0, 0, 'ko', markersize=10, label="Masa central")
                ax.set_aspect('equal')
                ax.set_xlabel("x", fontsize=12, color="#b26500")
                ax.set_ylabel("y", fontsize=12, color="#b26500")
                ax.set_title("Deflexión de la luz (2D)", fontsize=16, color="#b26500", pad=12)
                ax.legend(fontsize=12)
                ax.grid(True, alpha=0.3)
            else:
                # Gráfico 3D: superficie embebida + trayectoria
                rs = 1.0
                r_surf = np.linspace(rs + 0.01, r0, 80)
                theta_surf = np.linspace(0, 2*np.pi, 80)
                R_surf, Theta_surf = np.meshgrid(r_surf, theta_surf)
                Z_surf = 2 * np.sqrt(rs * (R_surf - rs))
                X_surf = R_surf * np.cos(Theta_surf)
                Y_surf = R_surf * np.sin(Theta_surf)
                z_traj = 2 * np.sqrt(rs * (r[mask] - rs))
                z_traj = np.where(np.isreal(z_traj), np.real(z_traj), 0)
                ax = fig.add_subplot(111, projection='3d')
                surf = ax.plot_surface(X_surf, Y_surf, Z_surf, cmap='YlOrBr', alpha=0.5, linewidth=0, antialiased=True)
                ax.plot(x, y, z_traj, label="Trayectoria", linewidth=2.5, color="#b26500")
                ax.scatter([0], [0], [0], color='k', s=60, label="Masa central")
                ax.set_xlabel("x")
                ax.set_ylabel("y")
                ax.set_zlabel("z (curvatura)")
                ax.set_title("Deflexión de la luz (3D)", fontsize=15, color="#b26500", pad=10)
                ax.legend()
                fig.colorbar(surf, ax=ax, shrink=0.6, aspect=12, pad=0.1, label="Curvatura")
                ax.grid(True, alpha=0.3)
                ax.view_init(elev=35, azim=45)
            canvas.draw()
        except Exception as e:
            info_label.setText(f"<span style='color:red;'>Error en la integración: {str(e)}</span>")
            fig.clear()
            ax = fig.add_subplot(111)
            ax.text(0.5, 0.5, f"Error en la integración:\n{str(e)}", ha='center', va='center', fontsize=12, color='red', transform=ax.transAxes)
            ax.set_xticks([])
            ax.set_yticks([])
            canvas.draw()

    slider.valueChanged.connect(plot_deflection)
    graph_select.currentIndexChanged.connect(plot_deflection)
    value_label.setText(f"{slider.value()/10:.1f}")
    plot_deflection()

    # Explicación didáctica debajo del gráfico
    explicacion_grafico = QLabel(
        "<span style='color:#b26500;'><b>¿Qué muestra este gráfico?</b></span> "
        "La curva representa la trayectoria de la luz al pasar cerca de una masa. "
        "Puedes experimentar cambiando el parámetro de impacto y alternar entre la vista 2D y 3D."
    )
    explicacion_grafico.setWordWrap(True)
    explicacion_grafico.setStyleSheet("background: #fffde7; border-radius: 10px; padding: 10px 16px; margin: 8px 0 12px 0; font-size: 14px; color: #b26500;")
    layout.addWidget(explicacion_grafico)

    scroll.setWidget(content)
    tab_layout = QVBoxLayout(tab)
    tab_layout.addWidget(scroll)
    tab.setLayout(tab_layout)
    return tab
