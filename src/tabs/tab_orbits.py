import numpy as np
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QSlider, QHBoxLayout, QComboBox, QFrame, QGroupBox, QScrollArea
from PyQt5.QtCore import Qt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from mpl_toolkits.mplot3d import Axes3D
from scipy.integrate import solve_ivp

def create_orbits_tab():
    tab = QWidget()
    tab.setStyleSheet("""
        QWidget {
            background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 #f3e5f5, stop:1 #ce93d8);
        }
    """)
    scroll = QScrollArea(tab)
    scroll.setWidgetResizable(True)
    content = QWidget()
    layout = QVBoxLayout(content)

    # Título y explicación
    title_box = QGroupBox("🪐 Órbitas relativistas (Schwarzschild)")
    title_box.setStyleSheet("QGroupBox { font-size: 15px; font-weight: bold; color: #6a1b9a; border-radius: 12px; background: #f3e5f5; margin-top: 10px; padding: 10px; }")
    vbox_title = QVBoxLayout()
    exp_label = QLabel(
        "<b>¿Cómo son las órbitas cerca de una masa compacta?</b><br><br>"
        "<b>Explicación:</b> Las órbitas en relatividad general muestran precesión y comportamientos distintos a la física clásica.<br>"
        "<b>Fórmula:</b> Ecuación de la órbita relativista para Schwarzschild.<br>"
        "<b>Ejemplo:</b> Precesión del perihelio de Mercurio.<br>"
        "<b>Referencia:</b> <a href='https://es.wikipedia.org/wiki/%C3%93rbita_relativista' style='color:#6a1b9a; text-decoration:underline;'>Wikipedia</a>"
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

    # Controles
    param_box = QGroupBox()
    param_box.setStyleSheet("QGroupBox { background: transparent; border-radius: 18px; border: none; margin-top: 8px; margin-bottom: 16px; box-shadow: none; padding: 12px 18px 12px 18px; }")
    param_layout = QHBoxLayout(param_box)
    icon_label = QLabel("<span style='font-size:2.2em;'>🪐</span>")
    icon_label.setStyleSheet("margin-right: 18px; background: transparent; border: none;")
    param_layout.addWidget(icon_label)
    l_label = QLabel("Momento angular L:")
    l_label.setStyleSheet("font-size: 1.2em; color: #6a1b9a; font-weight: bold; margin-right: 10px; background: transparent; border: none; text-shadow: 0 2px 8px #b39ddb;")
    param_layout.addWidget(l_label)
    l_slider = QSlider(Qt.Horizontal)
    l_slider.setMinimum(10)
    l_slider.setMaximum(50)
    l_slider.setValue(20)
    l_slider.setTickInterval(1)
    l_slider.setTickPosition(QSlider.TicksBelow)
    l_slider.setStyleSheet("""
        QSlider { background: transparent; }
        QSlider::groove:horizontal { height: 10px; background: #d1c4e9; border-radius: 5px; }
        QSlider::handle:horizontal { background: #8e24aa; border: 2px solid #6a1b9a; width: 22px; height: 22px; border-radius: 11px; margin: -7px 0; }
        QSlider::sub-page:horizontal { background: #b39ddb; border-radius: 5px; }
        QSlider::add-page:horizontal { background: #f3e5f5; border-radius: 5px; }
    """)
    param_layout.addWidget(l_slider, stretch=2)
    l_value = QLabel("2.0")
    l_value.setStyleSheet("background: #6a1b9a; color: #fff; border-radius: 50%; font-weight:bold; font-size:1.3em; padding: 10px 18px; margin-left: 18px; box-shadow: 0 2px 8px #b39ddb;")
    param_layout.addWidget(l_value)

    # Selector de gráfico 2D/3D alineado a la derecha
    graph_label = QLabel("Gráfico:")
    graph_label.setStyleSheet("font-size: 1.1em; color: #6a1b9a; font-weight: bold; margin-left: 18px; margin-right: 8px;")
    param_layout.addWidget(graph_label)
    graph_select = QComboBox()
    graph_select.addItems(["2D", "3D"])
    graph_select.setStyleSheet("""
        QComboBox {
            font-size: 1.1em;
            background: #f3e5f5;
            color: #6a1b9a;
            border: 1.5px solid #b39ddb;
            border-radius: 8px;
            padding: 4px 18px 4px 12px;
            min-width: 70px;
        }
        QComboBox QAbstractItemView {
            background: #f3e5f5;
            color: #6a1b9a;
            selection-background-color: #b39ddb;
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
    canvas.setStyleSheet("border-radius:18px; box-shadow:0 2px 18px #b39ddb; margin:16px 0 6px 0; background: #f3e5f5;")
    layout.addWidget(canvas)

    def orbit_rhs(phi, y, L):
        r, pr = y
        rs = 1.0
        f = 1 - rs/r
        dpr = (L**2/r**3 - rs*L**2/r**4) - rs/(2*r**2)*pr**2/f
        dr = pr
        return [dr, dpr/f]

    def plot_orbit():
        L = l_slider.value() / 10
        l_value.setText(f"{L:.1f}")
        r0 = 10.0
        pr0 = 0.0
        y0 = [r0, pr0]
        phis = np.linspace(0, 16*np.pi, 4000)
        try:
            sol = solve_ivp(lambda phi, y: orbit_rhs(phi, y, L), [phis[0], phis[-1]], y0, t_eval=phis, rtol=1e-6)
            r = sol.y[0]
            phi = sol.t
            mask = r > 1.01
            if not np.any(mask):
                raise ValueError("La órbita cae en el horizonte de eventos.")
            x = r[mask] * np.cos(phi[mask])
            y = r[mask] * np.sin(phi[mask])
            info_label.setText(f"<b>Ejemplo:</b> Para L = {L:.1f}, la órbita muestra precesión relativista.")
            fig.clear()
            if graph_select.currentText() == "2D":
                ax = fig.add_subplot(111)
                ax.plot(x, y, label="Órbita", linewidth=2, color="#6a1b9a")
                ax.plot(0, 0, 'ko', markersize=10, label="Masa central")
                ax.set_aspect('equal')
                ax.set_xlabel("x", fontsize=12, color="#6a1b9a")
                ax.set_ylabel("y", fontsize=12, color="#6a1b9a")
                ax.set_title("Órbita relativista (2D)", fontsize=16, color="#6a1b9a", pad=12)
                ax.legend(fontsize=12)
                ax.grid(True, alpha=0.3)
            else:
                # Gráfico 3D: superficie embebida + órbita
                rs = 1.0
                r_surf = np.linspace(rs + 0.01, r0, 80)
                theta_surf = np.linspace(0, 2*np.pi, 80)
                R_surf, Theta_surf = np.meshgrid(r_surf, theta_surf)
                Z_surf = 2 * np.sqrt(rs * (R_surf - rs))
                X_surf = R_surf * np.cos(Theta_surf)
                Y_surf = R_surf * np.sin(Theta_surf)
                z_orb = 2 * np.sqrt(rs * (r[mask] - rs))
                z_orb = np.where(np.isreal(z_orb), np.real(z_orb), 0)
                ax = fig.add_subplot(111, projection='3d')
                surf = ax.plot_surface(X_surf, Y_surf, Z_surf, cmap='plasma', alpha=0.5, linewidth=0, antialiased=True)
                ax.plot(x, y, z_orb, label="Órbita", linewidth=2.5, color="#6a1b9a")
                ax.scatter([0], [0], [0], color='k', s=60, label="Masa central")
                ax.set_xlabel("x")
                ax.set_ylabel("y")
                ax.set_zlabel("z (curvatura)")
                ax.set_title("Órbita relativista (3D)", fontsize=15, color="#6a1b9a", pad=10)
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

    l_slider.valueChanged.connect(plot_orbit)
    graph_select.currentIndexChanged.connect(plot_orbit)
    l_value.setText(f"{l_slider.value()/10:.1f}")
    plot_orbit()

    # Explicación didáctica debajo del gráfico
    explicacion_grafico = QLabel(
        "<span style='color:#6a1b9a;'><b>¿Qué muestra este gráfico?</b></span> "
        "La curva representa la órbita real de una partícula en el espacio-tiempo curvo de Schwarzschild. "
        "Puedes experimentar cambiando el momento angular y alternar entre la vista 2D y 3D."
    )
    explicacion_grafico.setWordWrap(True)
    explicacion_grafico.setStyleSheet("background: #f3e5f5; border-radius: 10px; padding: 10px 16px; margin: 8px 0 12px 0; font-size: 14px; color: #6a1b9a;")
    layout.addWidget(explicacion_grafico)

    scroll.setWidget(content)
    tab_layout = QVBoxLayout(tab)
    tab_layout.addWidget(scroll)
    tab.setLayout(tab_layout)
    return tab
