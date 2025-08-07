import numpy as np
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QSlider, QHBoxLayout, QFrame, QScrollArea, QGroupBox
from PyQt5.QtCore import Qt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from mpl_toolkits.mplot3d import Axes3D  # <-- Añadido para 3D


def create_time_dilation_tab():
    # (Importación eliminada: QScrollArea)
    tab = QWidget()
    tab.setStyleSheet("""
        QWidget {
            background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 #e3f2fd, stop:1 #90caf9);
        }
    """)
    scroll = QScrollArea(tab)
    scroll.setWidgetResizable(True)
    content = QWidget()
    layout = QVBoxLayout(content)

    # Sección de título y explicación con QGroupBox
    # (Importación eliminada: QGroupBox)
    title_box = QGroupBox("🕒 Dilatación temporal gravitacional")
    title_box.setStyleSheet("QGroupBox { font-size: 15px; font-weight: bold; color: #1565c0; border-radius: 12px; background: #e3f2fd; margin-top: 10px; padding: 10px; }")
    vbox_title = QVBoxLayout()
    exp_label = QLabel(
        "<b>¿Por qué el tiempo se ralentiza cerca de una masa?</b> 🌌<br><br>"
        "<b>Postulado clave:</b> La presencia de masa y energía curva el espacio-tiempo y afecta el ritmo del tiempo.<br>"
        "<b>Explicación física:</b> En la relatividad general, el tiempo propio de un observador cerca de una masa transcurre más lento que para uno lejos de la masa.<br>"
        "<b>Fórmula:</b> Δt' = Δt · √(1 - rₛ/r)<br>"
        "<b>Δt':</b> tiempo propio (cerca de la masa)<br><b>Δt:</b> tiempo lejano<br><b>rₛ:</b> radio de Schwarzschild = 2GM/c²<br><b>r:</b> distancia radial al centro de la masa<br>"
        "<b>Ejemplo cotidiano:</b> Los satélites GPS deben corregir sus relojes por dilatación temporal.<br>"
        "<b>Ejemplo extremo:</b> Cerca de un agujero negro, la dilatación temporal es tan fuerte que un minuto cerca del horizonte de eventos puede equivaler a años lejos de la masa.<br>"
        "<b>Historia y validación:</b> Predicho por Einstein en 1916, confirmado con relojes atómicos en satélites y experimentos en la Tierra.<br>"
        "<b>Referencia:</b> Wikipedia"
    )
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
    sep.setStyleSheet("margin: 12px 0; border: 0; border-top: 2px solid #90caf9;")
    layout.addWidget(sep)


    # Controles para comparar dos observadores estilo Material Design
    param_box = QGroupBox()
    param_box.setStyleSheet("""
        QGroupBox {
            background: transparent;
            border-radius: 18px;
            border: none;
            margin-top: 8px;
            margin-bottom: 16px;
            box-shadow: none;
            padding: 12px 18px 12px 18px;
        }
    """)
    param_layout = QHBoxLayout(param_box)
    icon_label = QLabel("<span style='font-size:2.2em;'>🪐</span>")
    icon_label.setStyleSheet("margin-right: 18px; background: transparent; border: none;")
    param_layout.addWidget(icon_label)
    slider_label = QLabel("Distancia al centro (r/rₛ):")
    slider_label.setStyleSheet("font-size: 1.2em; color: #1976d2; font-weight: bold; margin-right: 10px; background: transparent; border: none; text-shadow: 0 2px 8px #90caf9;")
    param_layout.addWidget(slider_label)
    slider = QSlider(Qt.Horizontal)
    slider.setMinimum(11)
    slider.setMaximum(100)
    slider.setValue(20)
    slider.setTickInterval(1)
    slider.setTickPosition(QSlider.TicksBelow)
    slider.setStyleSheet("""
        QSlider { background: transparent; }
        QSlider::groove:horizontal { height: 10px; background: #b2ebf2; border-radius: 5px; }
        QSlider::handle:horizontal { background: #00bcd4; border: 2px solid #00838f; width: 22px; height: 22px; border-radius: 11px; margin: -7px 0; }
        QSlider::sub-page:horizontal { background: #4dd0e1; border-radius: 5px; }
        QSlider::add-page:horizontal { background: #e0f7fa; border-radius: 5px; }
    """)
    param_layout.addWidget(slider, stretch=2)
    value_label = QLabel("2.0")
    value_label.setStyleSheet("background: #1976d2; color: #fff; border-radius: 50%; font-weight:bold; font-size:1.3em; padding: 10px 18px; margin-left: 18px; box-shadow: 0 2px 8px #90caf9;")
    param_layout.addWidget(value_label)
    layout.addWidget(param_box)

    # Mensaje explicativo para el usuario
    explicacion_uso = QLabel(
        "<span style='color:#1976d2; font-size:1.08em;'><b>¿Cómo usar?</b></span> "
        "Ajusta el <b>tiempo lejano Δt</b> con el control numérico y observa cómo cambian el reloj, la comparación y el gráfico en tiempo real. "
        "¡Así puedes experimentar la dilatación temporal de forma interactiva!"
    )
    explicacion_uso.setWordWrap(True)
    explicacion_uso.setStyleSheet("background: #e3f2fd; border-radius: 10px; padding: 8px 14px; margin-bottom: 6px; font-size: 14px; color: #1976d2;")
    layout.addWidget(explicacion_uso)

    # Control para elegir el tiempo lejano (t_lejano) y tipo de gráfico (2D/3D) juntos
    from PyQt5.QtWidgets import QSpinBox, QSizePolicy
    t_lejano_box = QGroupBox()
    t_lejano_box.setStyleSheet("QGroupBox { background: transparent; border: none; margin: 0; padding: 0; }")
    t_lejano_layout = QHBoxLayout(t_lejano_box)
    t_lejano_label = QLabel("Tiempo lejano Δt (s):")
    t_lejano_label.setStyleSheet("font-size: 1.1em; color: #1976d2; font-weight: bold; margin-right: 10px; background: transparent; border: none;")
    t_lejano_layout.addWidget(t_lejano_label)
    t_lejano_spin = QSpinBox()
    t_lejano_spin.setRange(1, 3600)
    t_lejano_spin.setValue(60)
    t_lejano_spin.setSingleStep(1)
    t_lejano_spin.setStyleSheet("QSpinBox { font-size: 1.1em; background: #e3f2fd; border-radius: 8px; padding: 4px 12px; min-width: 70px; } QSpinBox::up-button, QSpinBox::down-button { width: 18px; }")
    t_lejano_spin.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
    t_lejano_layout.addWidget(t_lejano_spin)

    # --- Selector de tipo de gráfico (2D/3D) al lado del spinbox ---
    from PyQt5.QtWidgets import QComboBox
    graph_select_label = QLabel("Gráfico:")
    graph_select_label.setStyleSheet("font-size: 1.1em; color: #1976d2; font-weight: bold; margin-left: 18px; margin-right: 8px; background: transparent; border: none;")
    t_lejano_layout.addWidget(graph_select_label)
    graph_select = QComboBox()
    graph_select.addItems(["2D", "3D"])
    graph_select.setStyleSheet("QComboBox { font-size: 1.1em; background: #e3f2fd; border-radius: 8px; padding: 4px 12px; min-width: 70px; }")
    t_lejano_layout.addWidget(graph_select)

    layout.addWidget(t_lejano_box)

    # Información comparativa
    info_label = QLabel()
    info_label.setWordWrap(True)
    info_label.setStyleSheet("background:#fffde7; border-radius:12px; box-shadow:0 2px 8px #ffd54f; padding:12px; font-size:1.1em; margin:10px 0;")
    layout.addWidget(info_label)


    # Gráfico y animación visual
    fig = Figure(figsize=(9,4))
    canvas = FigureCanvas(fig)
    canvas.setMinimumHeight(350)
    canvas.setStyleSheet("border-radius:18px; box-shadow:0 2px 12px #90caf9; margin:10px 0;")
    layout.addWidget(canvas)

    # Animación visual: dos relojes comparando el paso del tiempo con QTimer
    from PyQt5.QtCore import QTimer
    anim_label = QLabel()
    anim_label.setWordWrap(True)
    anim_label.setStyleSheet("background:#e0f7fa; border-radius:12px; box-shadow:0 2px 8px #4dd0e1; padding:10px; font-size:1.1em; margin:10px 0;")
    layout.addWidget(anim_label)
    reloj_animado = ["🕒", "🕑", "🕐", "🕛", "🕧", "🕜", "🕝", "🕞", "🕟", "🕠", "🕡", "🕢"]
    anim_index = {"lejano": 0, "cerca": 0}
    def animar_relojes():
        anim_index["lejano"] = (anim_index["lejano"] + 1) % len(reloj_animado)
        anim_index["cerca"] = (anim_index["cerca"] + 1) % len(reloj_animado)
        anim_label.setText(anim_label.text().replace("🕒", reloj_animado[anim_index["lejano"]]))
    timer = QTimer()
    timer.timeout.connect(animar_relojes)
    timer.start(1000)


    def update():
        r_over_rs = slider.value() / 10
        value_label.setText(f"{r_over_rs:.1f}")
        rs = 1.0
        r = r_over_rs * rs
        if r <= rs:
            fig.clear()
            ax = fig.add_subplot(111)
            ax.text(0.5, 0.5, "r debe ser mayor que rₛ", ha='center', va='center', fontsize=14, color='red', transform=ax.transAxes)
            ax.set_xticks([])
            ax.set_yticks([])
            canvas.draw()
            info_label.setText("<span style='color:red;'>La distancia está dentro del radio de Schwarzschild (agujero negro).</span>")
            anim_label.setText("")
            return
        dilation = np.sqrt(1 - rs/r)
        t_lejano = t_lejano_spin.value()
        t_cerca = t_lejano * dilation
        info_label.setText(
            f"<b>Comparación:</b> Si un observador lejano mide <span style='color:#1565c0;'>{t_lejano:.0f} s</span>,<br>"
            f"un observador cerca de la masa medirá <span style='color:#1565c0;'>{t_cerca:.2f} s</span>.<br>"
            f"<b>Relación temporal:</b> Δt'/Δt = <span style='color:#1565c0;'>{dilation:.5f}</span>"
        )
        # Animación visual simple: dos relojes
        reloj_lejano = "🕒" * max(1, int(t_lejano // 10))
        reloj_cerca = "🕒" * max(1, int(t_cerca // 10))
        anim_label.setText(
            f"Reloj lejano: {reloj_lejano}  {t_lejano:.0f} s\n"
            f"Reloj cerca de la masa: {reloj_cerca}  {t_cerca:.2f} s"
        )
        fig.clear()
        if graph_select.currentText() == "2D":
            # --- Gráfico 2D ---
            ax = fig.add_subplot(111)
            r_vals = np.linspace(1.01, 10, 300)
            y = np.sqrt(1 - 1/r_vals)
            ax.plot(r_vals, y, color='#1976d2', linewidth=2, label="Relación Δt'/Δt")
            ax.axvline(r_over_rs, color='r', linestyle='--', linewidth=2, label=f"r = {r_over_rs:.1f} rₛ")
            ax.scatter([r_over_rs], [dilation], color='red', s=80, zorder=5)
            ax.set_xlabel("r/rₛ", fontsize=12)
            ax.set_ylabel("Δt'/Δt", fontsize=12)
            ax.set_title("Dilatación temporal gravitacional", fontsize=16, pad=8)
            fig.subplots_adjust(top=0.93)
            ax.legend()
            ax.grid(True, alpha=0.3)
            ax.annotate(f"Δt'/Δt = {dilation:.3f}", xy=(r_over_rs, dilation), xytext=(r_over_rs+1, dilation-0.1),
                        arrowprops=dict(facecolor='black', shrink=0.05), fontsize=11, color='black')
        else:
            # --- Gráfico 3D ---
            ax = fig.add_subplot(111, projection='3d')
            r_vals = np.linspace(1.01, 10, 80)
            t_vals = np.linspace(1, 3600, 80)
            R, T = np.meshgrid(r_vals, t_vals)
            DIL = np.sqrt(1 - 1/R)
            T_PRIMA = T * DIL
            surf = ax.plot_surface(R, T, T_PRIMA, cmap='viridis', alpha=0.85)
            ax.set_xlabel("r/rₛ", fontsize=10)
            ax.set_ylabel("Δt (s)", fontsize=10)
            ax.set_zlabel("Δt' (s)", fontsize=10)
            ax.set_title("Dilatación temporal gravitacional (superficie 3D)", fontsize=13, pad=10)
            ax.scatter([r_over_rs], [t_lejano], [t_cerca], color='red', s=60, label="Situación actual")
            fig.colorbar(surf, ax=ax, shrink=0.6, aspect=12, pad=0.1, label="Δt'")
            ax.legend()
        canvas.draw()

    slider.valueChanged.connect(update)
    t_lejano_spin.valueChanged.connect(update)
    graph_select.currentIndexChanged.connect(update)  # <-- Añadido para actualizar al cambiar el selector
    value_label.setText(f"{slider.value()/10:.1f}")
    update()

    scroll.setWidget(content)
    tab_layout = QVBoxLayout(tab)
    tab_layout.addWidget(scroll)
    tab.setLayout(tab_layout)
    return tab
