import numpy as np
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTabWidget, QGroupBox, QPushButton, QFileDialog
from PyQt5.QtCore import QTimer
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.animation as animation

def create_advanced_effects_tab():
    tab = QWidget()
    tabs = QTabWidget(tab)
    layout = QVBoxLayout(tab)
    layout.addWidget(tabs)

    # --- Onda gravitacional: simulación estilo "video" ---
    gw_widget = QWidget()
    gw_layout = QVBoxLayout(gw_widget)
    title_gw = QGroupBox("🌊 Onda gravitacional (simulación tipo video)")
    title_gw.setStyleSheet("QGroupBox { font-size: 15px; font-weight: bold; color: #1565c0; border-radius: 12px; background: #e3f2fd; margin-top: 10px; padding: 10px; }")
    vbox_gw = QVBoxLayout()
    exp_gw = QLabel(
        "<b>Simulación tipo video:</b> Observa cómo una onda gravitacional distorsiona una cuadrícula de espacio-tiempo.<br>"
        "Esto representa el efecto de una onda real sobre el espacio, como se detecta en experimentos tipo LIGO."
    )
    exp_gw.setWordWrap(True)
    exp_gw.setStyleSheet("font-size: 14px; color: #1565c0; margin-bottom: 8px;")
    vbox_gw.addWidget(exp_gw)
    title_gw.setLayout(vbox_gw)
    gw_layout.addWidget(title_gw)

    fig_gw = Figure(figsize=(5.5, 4))
    canvas_gw = FigureCanvas(fig_gw)
    canvas_gw.setStyleSheet("border-radius:14px; box-shadow:0 2px 12px #90caf9; margin:10px 0; background: #e3f2fd;")
    gw_layout.addWidget(canvas_gw)

    # Parámetros de la cuadrícula
    x = np.linspace(-2, 2, 20)
    y = np.linspace(-2, 2, 20)
    X, Y = np.meshgrid(x, y)

    # Animación estilo video
    def animate_gw_video(i):
        fig_gw.clear()
        ax = fig_gw.add_subplot(111)
        # Onda gravitacional: distorsión sinusoidal transversal
        h = 0.25 * np.sin(2 * np.pi * (X - i/30))
        Xd = X + h * X
        Yd = Y - h * Y
        for j in range(X.shape[0]):
            ax.plot(Xd[j, :], Yd[j, :], color="#1976d2", alpha=0.7)
        for j in range(X.shape[1]):
            ax.plot(Xd[:, j], Yd[:, j], color="#1976d2", alpha=0.7)
        ax.set_xlim(-2.2, 2.2)
        ax.set_ylim(-2.2, 2.2)
        ax.set_aspect('equal')
        ax.axis('off')
        ax.set_title("Onda gravitacional distorsionando el espacio-tiempo", fontsize=13, color="#1565c0")
        canvas_gw.draw()

    # Botón para reproducir la animación tipo video
    play_btn = QPushButton("▶ Reproducir video")
    play_btn.setStyleSheet("background:#1976d2; color:white; font-weight:bold; border-radius:8px; padding:6px 18px; margin:8px 0;")
    gw_layout.addWidget(play_btn)
    timer_gw = QTimer()
    timer_gw.setInterval(35)
    frame_gw = [0]
    def play_gw():
        frame_gw[0] = 0
        timer_gw.start()
    def update_gw():
        animate_gw_video(frame_gw[0])
        frame_gw[0] += 1
        if frame_gw[0] > 120:
            timer_gw.stop()
    timer_gw.timeout.connect(update_gw)
    play_btn.clicked.connect(play_gw)
    # Mostrar primer frame
    animate_gw_video(0)
    tabs.addTab(gw_widget, "Onda gravitacional (video)")

    # --- Lente gravitacional: simulación tipo video ---
    lens_widget = QWidget()
    lens_layout = QVBoxLayout(lens_widget)
    title_lens = QGroupBox("🔭 Lente gravitacional (simulación tipo video)")
    title_lens.setStyleSheet("QGroupBox { font-size: 15px; font-weight: bold; color: #6a1b9a; border-radius: 12px; background: #ede7f6; margin-top: 10px; padding: 10px; }")
    vbox_lens = QVBoxLayout()
    exp_lens = QLabel(
        "<b>Simulación tipo video:</b> Observa cómo la luz de una fuente lejana se curva al pasar cerca de una masa, formando arcos de Einstein.<br>"
        "Puedes ver cómo cambia la imagen al mover la fuente."
    )
    exp_lens.setWordWrap(True)
    exp_lens.setStyleSheet("font-size: 14px; color: #6a1b9a; margin-bottom: 8px;")
    vbox_lens.addWidget(exp_lens)
    title_lens.setLayout(vbox_lens)
    lens_layout.addWidget(title_lens)

    fig_lens = Figure(figsize=(5.5, 4))
    canvas_lens = FigureCanvas(fig_lens)
    canvas_lens.setStyleSheet("border-radius:14px; box-shadow:0 2px 12px #b39ddb; margin:10px 0; background: #ede7f6;")
    lens_layout.addWidget(canvas_lens)

    # Parámetros para la animación de la lente
    def animate_lens_video(i):
        fig_lens.clear()
        ax = fig_lens.add_subplot(111)
        # Masa central
        ax.plot(0, 0, 'o', color="#6a1b9a", markersize=18, label="Masa")
        # Fuente lejana animada
        fx = 2 + 0.7 * np.sin(i/30)
        fy = 1.5 * np.cos(i/40)
        ax.plot(fx, fy, '*', color="#ffd54f", markersize=22, label="Fuente")
        # Rayos de luz curvados (simulación simple)
        for sign in [-1, 1]:
            theta = np.linspace(0, np.pi/2, 60)
            x_ray = np.cos(theta)
            y_ray = sign * np.sin(theta)
            curve = 0.18 * np.sin(i/25)
            ax.plot(x_ray, y_ray + curve*y_ray, color="#b26500", linestyle='--', linewidth=2)
            ax.arrow(x_ray[-1], y_ray[-1] + curve*y_ray[-1], 0.7, 0.3*sign, head_width=0.08, head_length=0.13, fc="#b26500", ec="#b26500")
        # Imagenes formadas (arcos de Einstein simplificados)
        arc_theta = np.linspace(0, 2*np.pi, 100)
        arc_r = 1.2 + 0.08 * np.sin(i/40)
        ax.plot(arc_r * np.cos(arc_theta), arc_r * np.sin(arc_theta), color="#1976d2", linewidth=3, alpha=0.7)
        ax.set_xlim(-0.5, 2.7)
        ax.set_ylim(-2, 2)
        ax.set_aspect('equal')
        ax.axis('off')
        ax.set_title("Lente gravitacional: formación de arcos de Einstein", fontsize=13, color="#6a1b9a")
        canvas_lens.draw()

    # Botón para reproducir la animación tipo video
    play_btn_lens = QPushButton("▶ Reproducir video")
    play_btn_lens.setStyleSheet("background:#6a1b9a; color:white; font-weight:bold; border-radius:8px; padding:6px 18px; margin:8px 0;")
    lens_layout.addWidget(play_btn_lens)
    timer_lens = QTimer()
    timer_lens.setInterval(40)
    frame_lens = [0]
    def play_lens():
        frame_lens[0] = 0
        timer_lens.start()
    def update_lens():
        animate_lens_video(frame_lens[0])
        frame_lens[0] += 1
        if frame_lens[0] > 120:
            timer_lens.stop()
    timer_lens.timeout.connect(update_lens)
    play_btn_lens.clicked.connect(play_lens)
    # Mostrar primer frame
    animate_lens_video(0)
    tabs.addTab(lens_widget, "Lente gravitacional (video)")

    # --- Explicación final ---
    explicacion = QLabel(
        "<span style='color:#1565c0; font-size:1.08em;'><b>¿Qué muestran estas simulaciones?</b></span> "
        "Puedes observar cómo las ondas gravitacionales y las lentes gravitacionales afectan el espacio-tiempo y la luz. "
        "Ambos fenómenos han sido confirmados experimentalmente y son predicciones clave de la Relatividad General."
    )
    explicacion.setWordWrap(True)
    explicacion.setStyleSheet("background: #e3f2fd; border-radius: 10px; padding: 10px 16px; margin: 12px 0 12px 0; font-size: 14px; color: #1565c0;")
    layout.addWidget(explicacion)

    tab.setLayout(layout)
    return tab
