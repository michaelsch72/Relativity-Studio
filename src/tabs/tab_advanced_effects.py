import numpy as np
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTabWidget, QGroupBox, QPushButton
from PyQt5.QtCore import QTimer
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

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
        "Esto representa el efecto de una onda real sobre el espacio, como se detecta en experimentos tipo LIGO.<br><br>"
        "<b>¿Qué son las ondas gravitacionales?</b><br>"
        "Son perturbaciones del espacio-tiempo que viajan a la velocidad de la luz, predichas por Einstein en 1916.<br>"
        "Se producen en eventos cósmicos extremos, como la fusión de agujeros negros o estrellas de neutrones.<br>"
        "Fueron detectadas por primera vez en 2015 por LIGO.<br><br>"
        "<b>¿Cómo afectan el espacio?</b><br>"
        "Deforman distancias y ángulos, estirando y comprimiendo el espacio en direcciones perpendiculares.<br>"
        "<b>Referencia:</b> <a href='https://es.wikipedia.org/wiki/Onda_gravitacional' style='color:#1565c0; text-decoration:underline;'>Wikipedia</a>"
    )
    exp_gw.setOpenExternalLinks(True)
    exp_gw.setWordWrap(True)
    exp_gw.setStyleSheet("font-size: 14px; color: #1565c0; margin-bottom: 8px;")
    vbox_gw.addWidget(exp_gw)
    title_gw.setLayout(vbox_gw)
    gw_layout.addWidget(title_gw)

    fig_gw = Figure(figsize=(5.5, 4))
    canvas_gw = FigureCanvas(fig_gw)
    canvas_gw.setStyleSheet("border-radius:14px; box-shadow:0 2px 12px #90caf9; margin:10px 0; background: #e3f2fd;")
    gw_layout.addWidget(canvas_gw)
    dynamic_gw = QLabel("")
    dynamic_gw.setWordWrap(True)
    dynamic_gw.setStyleSheet("background: #e3f2fd; border-radius: 8px; padding: 6px 12px; margin: 4px 0 10px 0; font-size: 13px; color: #1976d2;")
    gw_layout.addWidget(dynamic_gw)
    x = np.linspace(-2, 2, 20)
    y = np.linspace(-2, 2, 20)
    X, Y = np.meshgrid(x, y)

    def animate_gw_video(i):
        fig_gw.clear()
        ax = fig_gw.add_subplot(111)
        h = 0.25 * np.sin(2 * np.pi * (X - i/30))
        Xd = X + h * X
        Yd = Y - h * Y
        for j in range(X.shape[0]):
            ax.plot(Xd[j, :], Yd[j, :], color="#1976d2", alpha=0.8, linewidth=2)
        for j in range(X.shape[1]):
            ax.plot(Xd[:, j], Yd[:, j], color="#4dd0e1", alpha=0.7, linewidth=1.5)
        # Añadir ondas superpuestas para hacerlo más visual
        for amp, color, lw in [(0.12, "#b2ebf2", 1), (0.06, "#90caf9", 1)]:
            y_wave = amp * np.sin(8 * np.pi * (x - i/60))
            ax.plot(x, y_wave, color=color, linewidth=lw, alpha=0.7)
            ax.plot(x, -y_wave, color=color, linewidth=lw, alpha=0.7)
        ax.set_xlim(-2.2, 2.2)
        ax.set_ylim(-2.2, 2.2)
        ax.set_aspect('equal')
        ax.axis('off')
        ax.set_title("Onda gravitacional distorsionando el espacio-tiempo", fontsize=13, color="#1565c0")
        canvas_gw.draw()
        # Texto dinámico según el frame
        if i < 20:
            dynamic_gw.setText("La cuadrícula está en reposo. Pronto llegará la onda gravitacional...")
        elif i < 60:
            dynamic_gw.setText("¡La onda gravitacional está pasando! Observa cómo se estira y comprime el espacio-tiempo.")
        elif i < 100:
            dynamic_gw.setText("La onda sigue propagándose, deformando la cuadrícula en direcciones perpendiculares.")
        else:
            dynamic_gw.setText("El espacio-tiempo vuelve a su estado original tras el paso de la onda.")

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
        "Puedes ver cómo cambia la imagen al mover la fuente.<br><br>"
        "<b>¿Qué es una lente gravitacional?</b><br>"
        "Es un fenómeno donde la gravedad de una masa (como una galaxia) curva la trayectoria de la luz de objetos más lejanos.<br>"
        "Esto puede producir imágenes múltiples, arcos o anillos (arcos de Einstein).<br>"
        "<b>Historia:</b> Predicho por Einstein, observado por primera vez en 1979.<br>"
        "<b>Importancia:</b> Permite estudiar objetos muy lejanos y la distribución de materia oscura.<br>"
        "<b>Referencia:</b> <a href='https://es.wikipedia.org/wiki/Lente_gravitacional' style='color:#6a1b9a; text-decoration:underline;'>Wikipedia</a>"
    )
    exp_lens.setOpenExternalLinks(True)
    exp_lens.setWordWrap(True)
    exp_lens.setStyleSheet("font-size: 14px; color: #6a1b9a; margin-bottom: 8px;")
    vbox_lens.addWidget(exp_lens)
    title_lens.setLayout(vbox_lens)
    lens_layout.addWidget(title_lens)

    fig_lens = Figure(figsize=(5.5, 4))
    canvas_lens = FigureCanvas(fig_lens)
    canvas_lens.setStyleSheet("border-radius:14px; box-shadow:0 2px 12px #b39ddb; margin:10px 0; background: #ede7f6;")
    lens_layout.addWidget(canvas_lens)
    dynamic_lens = QLabel("")
    dynamic_lens.setWordWrap(True)
    dynamic_lens.setStyleSheet("background: #ede7f6; border-radius: 8px; padding: 6px 12px; margin: 4px 0 10px 0; font-size: 13px; color: #6a1b9a;")
    lens_layout.addWidget(dynamic_lens)

    def animate_lens_video(i):
        fig_lens.clear()
        ax = fig_lens.add_subplot(111)
        # Masa central con gradiente y "halo"
        ax.scatter(0, 0, color="#6a1b9a", s=400, alpha=0.18, zorder=1)
        ax.plot(0, 0, 'o', color="#6a1b9a", markersize=18, label="Masa", zorder=2)
        # Fuente lejana animada
        fx = 2 + 0.7 * np.sin(i/30)
        fy = 1.5 * np.cos(i/40)
        ax.plot(fx, fy, '*', color="#ffd54f", markersize=22, label="Fuente", zorder=3)
        # Rayos de luz curvados (simulación simple)
        for sign, ray_color in zip([-1, 1], ["#b26500", "#ff9800"]):
            theta = np.linspace(0, np.pi/2, 60)
            x_ray = np.cos(theta)
            y_ray = sign * np.sin(theta)
            curve = 0.18 * np.sin(i/25)
            ax.plot(x_ray, y_ray + curve*y_ray, color=ray_color, linestyle='--', linewidth=2, zorder=2)
            ax.arrow(x_ray[-1], y_ray[-1] + curve*y_ray[-1], 0.7, 0.3*sign, head_width=0.08, head_length=0.13, fc=ray_color, ec=ray_color, zorder=2)
        # Imagenes formadas (arcos de Einstein simplificados)
        arc_theta = np.linspace(0, 2*np.pi, 100)
        arc_r = 1.2 + 0.08 * np.sin(i/40)
        ax.plot(arc_r * np.cos(arc_theta), arc_r * np.sin(arc_theta), color="#1976d2", linewidth=3, alpha=0.8, zorder=4)
        # Fondo con estrellas
        np.random.seed(0)
        ax.scatter(np.random.uniform(-0.5, 2.7, 40), np.random.uniform(-2, 2, 40), color="#fffde7", s=8, alpha=0.7, zorder=0)
        ax.set_xlim(-0.5, 2.7)
        ax.set_ylim(-2, 2)
        ax.set_aspect('equal')
        ax.axis('off')
        ax.set_title("Lente gravitacional: formación de arcos de Einstein", fontsize=13, color="#6a1b9a")
        canvas_lens.draw()
        # Texto dinámico según el frame
        if i < 20:
            dynamic_lens.setText("La fuente lejana está quieta. Observa la alineación con la masa central.")
        elif i < 60:
            dynamic_lens.setText("La fuente se mueve: los rayos de luz se curvan y los arcos de Einstein se forman y deforman.")
        elif i < 100:
            dynamic_lens.setText("La alineación cambia, los arcos se hacen más grandes o pequeños según la posición de la fuente.")
        else:
            dynamic_lens.setText("La fuente vuelve a su posición inicial y el fenómeno se repite.")

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

    # --- Efecto Doppler relativista ---
    doppler_widget = QWidget()
    doppler_layout = QVBoxLayout(doppler_widget)
    title_doppler = QGroupBox("🌈 Efecto Doppler Relativista (simulación tipo video)")
    title_doppler.setStyleSheet("QGroupBox { font-size: 15px; font-weight: bold; color: #b26500; border-radius: 12px; background: #fffde7; margin-top: 10px; padding: 10px; }")
    vbox_doppler = QVBoxLayout()
    exp_doppler = QLabel(
        "<b>Simulación tipo video:</b> Observa cómo cambia la frecuencia de la luz cuando la fuente se mueve respecto al observador.<br>"
        "<b>Corrimiento al azul:</b> Fuente se acerca.<br>"
        "<b>Corrimiento al rojo:</b> Fuente se aleja.<br>"
        "<b>Referencia:</b> <a href='https://es.wikipedia.org/wiki/Efecto_Doppler_relativista' style='color:#b26500; text-decoration:underline;'>Wikipedia</a>"
    )
    exp_doppler.setOpenExternalLinks(True)
    exp_doppler.setWordWrap(True)
    exp_doppler.setStyleSheet("font-size: 14px; color: #b26500; margin-bottom: 8px;")
    vbox_doppler.addWidget(exp_doppler)
    title_doppler.setLayout(vbox_doppler)
    doppler_layout.addWidget(title_doppler)
    fig_doppler = Figure(figsize=(5.5, 3))
    canvas_doppler = FigureCanvas(fig_doppler)
    canvas_doppler.setStyleSheet("border-radius:14px; box-shadow:0 2px 12px #ffd54f; margin:10px 0; background: #fffde7;")
    doppler_layout.addWidget(canvas_doppler)
    dynamic_doppler = QLabel("")
    dynamic_doppler.setWordWrap(True)
    dynamic_doppler.setStyleSheet("background: #fffde7; border-radius: 8px; padding: 6px 12px; margin: 4px 0 10px 0; font-size: 13px; color: #b26500;")
    doppler_layout.addWidget(dynamic_doppler)
    v = np.linspace(-0.99, 0.99, 120)
    def animate_doppler(i):
        fig_doppler.clear()
        ax = fig_doppler.add_subplot(111)
        v_now = v[i]
        gamma = 1/np.sqrt(1-v_now**2)
        freq_obs = gamma*(1-v_now)
        color = "#1976d2" if v_now<0 else "#b26500"
        ax.plot([0,1],[1,freq_obs], color=color, linewidth=6)
        ax.set_ylim(0,2)
        ax.set_xlim(0,1)
        ax.set_title(f"Corrimiento {'al azul' if v_now<0 else 'al rojo'}: f_obs = {freq_obs:.2f} f_emitida", color=color)
        ax.axis('off')
        canvas_doppler.draw()
        if v_now < -0.5:
            dynamic_doppler.setText("La fuente se acerca rápidamente: la luz se ve azulada (corrimiento al azul).")
        elif v_now > 0.5:
            dynamic_doppler.setText("La fuente se aleja rápidamente: la luz se ve enrojecida (corrimiento al rojo).")
        else:
            dynamic_doppler.setText("La fuente está casi en reposo relativo.")
    play_btn_doppler = QPushButton("▶ Reproducir video")
    play_btn_doppler.setStyleSheet("background:#b26500; color:white; font-weight:bold; border-radius:8px; padding:6px 18px; margin:8px 0;")
    doppler_layout.addWidget(play_btn_doppler)
    timer_doppler = QTimer()
    timer_doppler.setInterval(40)
    frame_doppler = [0]
    def play_doppler():
        frame_doppler[0] = 0
        timer_doppler.start()
    def update_doppler():
        animate_doppler(frame_doppler[0])
        frame_doppler[0] += 1
        if frame_doppler[0] >= len(v):
            timer_doppler.stop()
    timer_doppler.timeout.connect(update_doppler)
    play_btn_doppler.clicked.connect(play_doppler)
    animate_doppler(0)
    tabs.addTab(doppler_widget, "Efecto Doppler")

    # --- Agujero de gusano ---
    wormhole_widget = QWidget()
    wormhole_layout = QVBoxLayout(wormhole_widget)
    title_wormhole = QGroupBox("🌀 Agujero de Gusano (simulación tipo video)")
    title_wormhole.setStyleSheet("QGroupBox { font-size: 15px; font-weight: bold; color: #6a1b9a; border-radius: 12px; background: #ede7f6; margin-top: 10px; padding: 10px; }")
    vbox_wormhole = QVBoxLayout()
    exp_wormhole = QLabel(
        "<b>Simulación tipo video:</b> Visualiza la deformación del espacio en un agujero de gusano tipo Morris-Thorne.<br>"
        "<b>Referencia:</b> <a href='https://es.wikipedia.org/wiki/Agujero_de_gusano' style='color:#6a1b9a; text-decoration:underline;'>Wikipedia</a>"
    )
    exp_wormhole.setOpenExternalLinks(True)
    exp_wormhole.setWordWrap(True)
    exp_wormhole.setStyleSheet("font-size: 14px; color: #6a1b9a; margin-bottom: 8px;")
    vbox_wormhole.addWidget(exp_wormhole)
    title_wormhole.setLayout(vbox_wormhole)
    wormhole_layout.addWidget(title_wormhole)
    fig_wormhole = Figure(figsize=(5.5, 3))
    canvas_wormhole = FigureCanvas(fig_wormhole)
    canvas_wormhole.setStyleSheet("border-radius:14px; box-shadow:0 2px 12px #b39ddb; margin:10px 0; background: #ede7f6;")
    wormhole_layout.addWidget(canvas_wormhole)
    dynamic_wormhole = QLabel("")
    dynamic_wormhole.setWordWrap(True)
    dynamic_wormhole.setStyleSheet("background: #ede7f6; border-radius: 8px; padding: 6px 12px; margin: 4px 0 10px 0; font-size: 13px; color: #6a1b9a;")
    wormhole_layout.addWidget(dynamic_wormhole)
    r = np.linspace(-2,2,400)
    def animate_wormhole(i):
        fig_wormhole.clear()
        ax = fig_wormhole.add_subplot(111)
        z = np.sinh(r + 0.5*np.sin(i/20))
        ax.plot(r, z, color="#6a1b9a", linewidth=3)
        ax.set_title("Sección de un agujero de gusano", color="#6a1b9a")
        ax.axis('off')
        canvas_wormhole.draw()
        if i < 40:
            dynamic_wormhole.setText("El agujero de gusano está estable.")
        elif i < 80:
            dynamic_wormhole.setText("El agujero de gusano se deforma: el 'puente' se ensancha.")
        else:
            dynamic_wormhole.setText("El agujero de gusano vuelve a su forma original.")
    play_btn_wormhole = QPushButton("▶ Reproducir video")
    play_btn_wormhole.setStyleSheet("background:#6a1b9a; color:white; font-weight:bold; border-radius:8px; padding:6px 18px; margin:8px 0;")
    wormhole_layout.addWidget(play_btn_wormhole)
    timer_wormhole = QTimer()
    timer_wormhole.setInterval(40)
    frame_wormhole = [0]
    def play_wormhole():
        frame_wormhole[0] = 0
        timer_wormhole.start()
    def update_wormhole():
        animate_wormhole(frame_wormhole[0])
        frame_wormhole[0] += 1
        if frame_wormhole[0] > 120:
            timer_wormhole.stop()
    timer_wormhole.timeout.connect(update_wormhole)
    play_btn_wormhole.clicked.connect(play_wormhole)
    animate_wormhole(0)
    tabs.addTab(wormhole_widget, "Agujero de Gusano")

    # --- Expansión del universo ---
    expansion_widget = QWidget()
    expansion_layout = QVBoxLayout(expansion_widget)
    title_expansion = QGroupBox("🌌 Expansión del Universo (simulación tipo video)")
    title_expansion.setStyleSheet("QGroupBox { font-size: 15px; font-weight: bold; color: #b26500; border-radius: 12px; background: #fffde7; margin-top: 10px; padding: 10px; }")
    vbox_expansion = QVBoxLayout()
    exp_expansion = QLabel(
        "<b>Simulación tipo video:</b> Observa cómo las galaxias se alejan unas de otras según la ley de Hubble.<br>"
        "<b>Referencia:</b> <a href='https://es.wikipedia.org/wiki/Expansi%C3%B3n_del_universo' style='color:#b26500; text-decoration:underline;'>Wikipedia</a>"
    )
    exp_expansion.setOpenExternalLinks(True)
    exp_expansion.setWordWrap(True)
    exp_expansion.setStyleSheet("font-size: 14px; color: #b26500; margin-bottom: 8px;")
    vbox_expansion.addWidget(exp_expansion)
    title_expansion.setLayout(vbox_expansion)
    expansion_layout.addWidget(title_expansion)
    fig_expansion = Figure(figsize=(5.5, 3))
    canvas_expansion = FigureCanvas(fig_expansion)
    canvas_expansion.setStyleSheet("border-radius:14px; box-shadow:0 2px 12px #ffd54f; margin:10px 0; background: #fffde7;")
    expansion_layout.addWidget(canvas_expansion)
    dynamic_expansion = QLabel("")
    dynamic_expansion.setWordWrap(True)
    dynamic_expansion.setStyleSheet("background: #fffde7; border-radius: 8px; padding: 6px 12px; margin: 4px 0 10px 0; font-size: 13px; color: #b26500;")
    expansion_layout.addWidget(dynamic_expansion)
    x = np.linspace(-1,1,10)
    y = np.zeros_like(x)
    def animate_expansion(i):
        t = i/20
        scale = np.exp(0.5*t)
        fig_expansion.clear()
        ax = fig_expansion.add_subplot(111)
        ax.scatter(x*scale, y, color="#b26500", s=80)
        ax.set_xlim(-5,5)
        ax.set_ylim(-1,1)
        ax.set_title(f"Galaxias alejándose (t={t:.1f})", color="#b26500")
        ax.axis('off')
        canvas_expansion.draw()
        if t < 1:
            dynamic_expansion.setText("El universo está casi estático.")
        elif t < 2:
            dynamic_expansion.setText("Las galaxias empiezan a alejarse unas de otras.")
        else:
            dynamic_expansion.setText("La expansión se acelera: las galaxias se separan rápidamente.")
    play_btn_expansion = QPushButton("▶ Reproducir video")
    play_btn_expansion.setStyleSheet("background:#b26500; color:white; font-weight:bold; border-radius:8px; padding:6px 18px; margin:8px 0;")
    expansion_layout.addWidget(play_btn_expansion)
    timer_expansion = QTimer()
    timer_expansion.setInterval(40)
    frame_expansion = [0]
    def play_expansion():
        frame_expansion[0] = 0
        timer_expansion.start()
    def update_expansion():
        animate_expansion(frame_expansion[0])
        frame_expansion[0] += 1
        if frame_expansion[0] > 60:
            timer_expansion.stop()
    timer_expansion.timeout.connect(update_expansion)
    play_btn_expansion.clicked.connect(play_expansion)
    animate_expansion(0)
    tabs.addTab(expansion_widget, "Expansión del Universo")

    # --- Colisión de agujeros negros ---
    bh_widget = QWidget()
    bh_layout = QVBoxLayout(bh_widget)
    title_bh = QGroupBox("⚫⚫ Colisión de Agujeros Negros (simulación tipo video)")
    title_bh.setStyleSheet("QGroupBox { font-size: 15px; font-weight: bold; color: #1976d2; border-radius: 12px; background: #e3f2fd; margin-top: 10px; padding: 10px; }")
    vbox_bh = QVBoxLayout()
    exp_bh = QLabel(
        "<b>Simulación tipo video:</b> Visualiza la fusión de dos agujeros negros y la emisión de ondas gravitacionales.<br>"
        "<b>Referencia:</b> <a href='https://es.wikipedia.org/wiki/Onda_gravitacional#Colisi%C3%B3n_de_agujeros_negros' style='color:#1976d2; text-decoration:underline;'>Wikipedia</a>"
    )
    exp_bh.setOpenExternalLinks(True)
    exp_bh.setWordWrap(True)
    exp_bh.setStyleSheet("font-size: 14px; color: #1976d2; margin-bottom: 8px;")
    vbox_bh.addWidget(exp_bh)
    title_bh.setLayout(vbox_bh)
    bh_layout.addWidget(title_bh)
    fig_bh = Figure(figsize=(5.5, 3))
    canvas_bh = FigureCanvas(fig_bh)
    canvas_bh.setStyleSheet("border-radius:14px; box-shadow:0 2px 12px #90caf9; margin:10px 0; background: #e3f2fd;")
    bh_layout.addWidget(canvas_bh)
    dynamic_bh = QLabel("")
    dynamic_bh.setWordWrap(True)
    dynamic_bh.setStyleSheet("background: #e3f2fd; border-radius: 8px; padding: 6px 12px; margin: 4px 0 10px 0; font-size: 13px; color: #1976d2;")
    bh_layout.addWidget(dynamic_bh)
    t = np.linspace(0, 2*np.pi, 200)
    x1 = -np.cos(t)
    y1 = np.sin(t)
    x2 = np.cos(t)
    y2 = -np.sin(t)
    def animate_bh(i):
        fig_bh.clear()
        ax = fig_bh.add_subplot(111)
        idx = min(i*2, len(t)-1)
        ax.plot(x1[:idx], y1[:idx], color="#1976d2", linewidth=3)
        ax.plot(x2[:idx], y2[:idx], color="#b26500", linewidth=3)
        ax.plot([0], [0], 'ko', markersize=18)
        ax.set_title("Trayectorias antes de la fusión", color="#1976d2")
        ax.axis('off')
        canvas_bh.draw()
        if idx < 100:
            dynamic_bh.setText("Los agujeros negros giran acercándose.")
        elif idx < 180:
            dynamic_bh.setText("¡Colisión! Se fusionan y emiten una onda gravitacional.")
        else:
            dynamic_bh.setText("Queda un solo agujero negro más masivo.")
    play_btn_bh = QPushButton("▶ Reproducir video")
    play_btn_bh.setStyleSheet("background:#1976d2; color:white; font-weight:bold; border-radius:8px; padding:6px 18px; margin:8px 0;")
    bh_layout.addWidget(play_btn_bh)
    timer_bh = QTimer()
    timer_bh.setInterval(40)
    frame_bh = [0]
    def play_bh():
        frame_bh[0] = 0
        timer_bh.start()
    def update_bh():
        animate_bh(frame_bh[0])
        frame_bh[0] += 1
        if frame_bh[0] > 100:
            timer_bh.stop()
    timer_bh.timeout.connect(update_bh)
    play_btn_bh.clicked.connect(play_bh)
    animate_bh(0)
    tabs.addTab(bh_widget, "Colisión de Agujeros Negros")

    # --- Lentes gravitacionales múltiples ---
    multi_lens_widget = QWidget()
    multi_lens_layout = QVBoxLayout(multi_lens_widget)
    title_multi_lens = QGroupBox("🔭🔭 Lentes Gravitacionales Múltiples (simulación tipo video)")
    title_multi_lens.setStyleSheet("QGroupBox { font-size: 15px; font-weight: bold; color: #1976d2; border-radius: 12px; background: #e3f2fd; margin-top: 10px; padding: 10px; }")
    vbox_multi_lens = QVBoxLayout()
    exp_multi_lens = QLabel(
        "<b>Simulación tipo video:</b> Visualiza la trayectoria de la luz en presencia de varias masas (lentes).<br>"
        "<b>Referencia:</b> <a href='https://es.wikipedia.org/wiki/Lente_gravitacional' style='color:#1976d2; text-decoration:underline;'>Wikipedia</a>"
    )
    exp_multi_lens.setOpenExternalLinks(True)
    exp_multi_lens.setWordWrap(True)
    exp_multi_lens.setStyleSheet("font-size: 14px; color: #1976d2; margin-bottom: 8px;")
    vbox_multi_lens.addWidget(exp_multi_lens)
    title_multi_lens.setLayout(vbox_multi_lens)
    multi_lens_layout.addWidget(title_multi_lens)
    fig_multi_lens = Figure(figsize=(5.5, 3))
    canvas_multi_lens = FigureCanvas(fig_multi_lens)
    canvas_multi_lens.setStyleSheet("border-radius:14px; box-shadow:0 2px 12px #90caf9; margin:10px 0; background: #e3f2fd;")
    multi_lens_layout.addWidget(canvas_multi_lens)
    dynamic_multi_lens = QLabel("")
    dynamic_multi_lens.setWordWrap(True)
    dynamic_multi_lens.setStyleSheet("background: #e3f2fd; border-radius: 8px; padding: 6px 12px; margin: 4px 0 10px 0; font-size: 13px; color: #1976d2;")
    multi_lens_layout.addWidget(dynamic_multi_lens)
    masses = [(-1,0), (1,0)]
    x = np.linspace(-2,2,400)
    def animate_multi_lens(i):
        y = 0.2/(x+1.1+0.2*np.sin(i/20)) + 0.2/(x-1.1-0.2*np.cos(i/30))
        fig_multi_lens.clear()
        ax = fig_multi_lens.add_subplot(111)
        ax.plot(x, y, color="#1976d2", linewidth=2)
        for mx, my in masses:
            ax.plot(mx, my, 'o', color="#b26500", markersize=12)
        ax.set_title("Trayectoria de la luz entre dos lentes", color="#1976d2")
        ax.axis('off')
        canvas_multi_lens.draw()
        if i < 30:
            dynamic_multi_lens.setText("La luz pasa entre dos masas fijas.")
        elif i < 60:
            dynamic_multi_lens.setText("Las masas se mueven y la trayectoria de la luz se curva más.")
        else:
            dynamic_multi_lens.setText("La configuración vuelve a la inicial.")
    play_btn_multi_lens = QPushButton("▶ Reproducir video")
    play_btn_multi_lens.setStyleSheet("background:#1976d2; color:white; font-weight:bold; border-radius:8px; padding:6px 18px; margin:8px 0;")
    multi_lens_layout.addWidget(play_btn_multi_lens)
    timer_multi_lens = QTimer()
    timer_multi_lens.setInterval(40)
    frame_multi_lens = [0]
    def play_multi_lens():
        frame_multi_lens[0] = 0
        timer_multi_lens.start()
    def update_multi_lens():
        animate_multi_lens(frame_multi_lens[0])
        frame_multi_lens[0] += 1
        if frame_multi_lens[0] > 90:
            timer_multi_lens.stop()
    timer_multi_lens.timeout.connect(update_multi_lens)
    play_btn_multi_lens.clicked.connect(play_multi_lens)
    animate_multi_lens(0)
    tabs.addTab(multi_lens_widget, "Lentes Gravitacionales Múltiples")

    # --- Paradoja de los gemelos ---
    twins_widget = QWidget()
    twins_layout = QVBoxLayout(twins_widget)
    title_twins = QGroupBox("👬 Paradoja de los Gemelos (simulación tipo video)")
    title_twins.setStyleSheet("QGroupBox { font-size: 15px; font-weight: bold; color: #00897b; border-radius: 12px; background: #e0f7fa; margin-top: 10px; padding: 10px; }")
    vbox_twins = QVBoxLayout()
    exp_twins = QLabel(
        "<b>Simulación tipo video:</b> Visualiza la diferencia de tiempo vivido por dos gemelos: uno viaja a velocidad relativista y el otro permanece en la Tierra.<br>"
        "<b>Referencia:</b> <a href='https://es.wikipedia.org/wiki/Paradoja_de_los_gemelos' style='color:#00897b; text-decoration:underline;'>Wikipedia</a>"
    )
    exp_twins.setOpenExternalLinks(True)
    exp_twins.setWordWrap(True)
    exp_twins.setStyleSheet("font-size: 14px; color: #00897b; margin-bottom: 8px;")
    vbox_twins.addWidget(exp_twins)
    title_twins.setLayout(vbox_twins)
    twins_layout.addWidget(title_twins)
    fig_twins = Figure(figsize=(5.5, 3))
    canvas_twins = FigureCanvas(fig_twins)
    canvas_twins.setStyleSheet("border-radius:14px; box-shadow:0 2px 12px #4dd0e1; margin:10px 0; background: #e0f7fa;")
    twins_layout.addWidget(canvas_twins)
    dynamic_twins = QLabel("")
    dynamic_twins.setWordWrap(True)
    dynamic_twins.setStyleSheet("background: #e0f7fa; border-radius: 8px; padding: 6px 12px; margin: 4px 0 10px 0; font-size: 13px; color: #00897b;")
    twins_layout.addWidget(dynamic_twins)
    v = np.linspace(0, 0.99, 80)
    def animate_twins(i):
        v_now = v[i]
        gamma = 1/np.sqrt(1-v_now**2)
        t_tierra = 10
        t_viajero = t_tierra/gamma
        fig_twins.clear()
        ax = fig_twins.add_subplot(111)
        ax.bar(["Tierra","Viajero"], [t_tierra, t_viajero], color=["#1976d2","#b26500"])
        ax.set_ylim(0,12)
        ax.set_title(f"Tiempo vivido: Tierra={t_tierra:.1f} años, Viajero={t_viajero:.1f} años", color="#00897b")
        canvas_twins.draw()
        if v_now < 0.3:
            dynamic_twins.setText("Ambos gemelos envejecen casi igual.")
        elif v_now < 0.7:
            dynamic_twins.setText("El gemelo viajero envejece más lento.")
        else:
            dynamic_twins.setText("El gemelo viajero apenas envejece comparado con el que se queda.")
    play_btn_twins = QPushButton("▶ Reproducir video")
    play_btn_twins.setStyleSheet("background:#00897b; color:white; font-weight:bold; border-radius:8px; padding:6px 18px; margin:8px 0;")
    twins_layout.addWidget(play_btn_twins)
    timer_twins = QTimer()
    timer_twins.setInterval(40)
    frame_twins = [0]
    def play_twins():
        frame_twins[0] = 0
        timer_twins.start()
    def update_twins():
        animate_twins(frame_twins[0])
        frame_twins[0] += 1
        if frame_twins[0] >= len(v):
            timer_twins.stop()
    timer_twins.timeout.connect(update_twins)
    play_btn_twins.clicked.connect(play_twins)
    animate_twins(0)
    tabs.addTab(twins_widget, "Paradoja de los Gemelos")

    # --- Horizontes y regiones prohibidas ---
    horizon_widget = QWidget()
    horizon_layout = QVBoxLayout(horizon_widget)
    title_horizon = QGroupBox("🕳️ Horizontes y Regiones Prohibidas (simulación tipo video)")
    title_horizon.setStyleSheet("QGroupBox { font-size: 15px; font-weight: bold; color: #b26500; border-radius: 12px; background: #fffde7; margin-top: 10px; padding: 10px; }")
    vbox_horizon = QVBoxLayout()
    exp_horizon = QLabel(
        "<b>Simulación tipo video:</b> Visualiza el horizonte de eventos y las regiones donde no se puede escapar de un agujero negro.<br>"
        "<b>Referencia:</b> <a href='https://es.wikipedia.org/wiki/Horizonte_de_sucesos' style='color:#b26500; text-decoration:underline;'>Wikipedia</a>"
    )
    exp_horizon.setOpenExternalLinks(True)
    exp_horizon.setWordWrap(True)
    exp_horizon.setStyleSheet("font-size: 14px; color: #b26500; margin-bottom: 8px;")
    vbox_horizon.addWidget(exp_horizon)
    title_horizon.setLayout(vbox_horizon)
    horizon_layout.addWidget(title_horizon)
    fig_horizon = Figure(figsize=(5.5, 3))
    canvas_horizon = FigureCanvas(fig_horizon)
    canvas_horizon.setStyleSheet("border-radius:14px; box-shadow:0 2px 12px #ffd54f; margin:10px 0; background: #fffde7;")
    horizon_layout.addWidget(canvas_horizon)
    dynamic_horizon = QLabel("")
    dynamic_horizon.setWordWrap(True)
    dynamic_horizon.setStyleSheet("background: #fffde7; border-radius: 8px; padding: 6px 12px; margin: 4px 0 10px 0; font-size: 13px; color: #b26500;")
    horizon_layout.addWidget(dynamic_horizon)
    theta = np.linspace(0,2*np.pi,200)
    def animate_horizon(i):
        r = 1 + 0.1*np.sin(i/20)
        fig_horizon.clear()
        ax = fig_horizon.add_subplot(111, polar=True)
        ax.fill_between(theta, 0, r, color="#b26500", alpha=0.3, label="Región prohibida")
        ax.plot(theta, np.ones_like(theta), color="#1976d2", linewidth=2, label="Horizonte de eventos")
        ax.set_title("Horizonte de eventos (rₛ)", color="#b26500")
        ax.set_yticklabels([])
        ax.legend()
        canvas_horizon.draw()
        if i < 30:
            dynamic_horizon.setText("El horizonte de eventos es estable.")
        elif i < 60:
            dynamic_horizon.setText("La región prohibida crece y decrece levemente.")
        else:
            dynamic_horizon.setText("El horizonte vuelve a su tamaño original.")
    play_btn_horizon = QPushButton("▶ Reproducir video")
    play_btn_horizon.setStyleSheet("background:#b26500; color:white; font-weight:bold; border-radius:8px; padding:6px 18px; margin:8px 0;")
    horizon_layout.addWidget(play_btn_horizon)
    timer_horizon = QTimer()
    timer_horizon.setInterval(40)
    frame_horizon = [0]
    def play_horizon():
        frame_horizon[0] = 0
        timer_horizon.start()
    def update_horizon():
        animate_horizon(frame_horizon[0])
        frame_horizon[0] += 1
        if frame_horizon[0] > 90:
            timer_horizon.stop()
    timer_horizon.timeout.connect(update_horizon)
    play_btn_horizon.clicked.connect(play_horizon)
    animate_horizon(0)
    tabs.addTab(horizon_widget, "Horizontes y Regiones Prohibidas")

    # --- Caída libre en Schwarzschild/Kerr ---
    freefall_widget = QWidget()
    freefall_layout = QVBoxLayout(freefall_widget)
    title_freefall = QGroupBox("🪂 Caída Libre en Schwarzschild/Kerr (simulación tipo video)")
    title_freefall.setStyleSheet("QGroupBox { font-size: 15px; font-weight: bold; color: #00897b; border-radius: 12px; background: #e0f7fa; margin-top: 10px; padding: 10px; }")
    vbox_freefall = QVBoxLayout()
    exp_freefall = QLabel(
        "<b>Simulación tipo video:</b> Simula la caída libre radial hacia un agujero negro (Schwarzschild).<br>"
        "<b>Referencia:</b> <a href='https://es.wikipedia.org/wiki/Agujero_negro_de_Schwarzschild' style='color:#00897b; text-decoration:underline;'>Wikipedia</a>"
    )
    exp_freefall.setOpenExternalLinks(True)
    exp_freefall.setWordWrap(True)
    exp_freefall.setStyleSheet("font-size: 14px; color: #00897b; margin-bottom: 8px;")
    vbox_freefall.addWidget(exp_freefall)
    title_freefall.setLayout(vbox_freefall)
    freefall_layout.addWidget(title_freefall)
    fig_freefall = Figure(figsize=(5.5, 3))
    canvas_freefall = FigureCanvas(fig_freefall)
    canvas_freefall.setStyleSheet("border-radius:14px; box-shadow:0 2px 12px #4dd0e1; margin:10px 0; background: #e0f7fa;")
    freefall_layout.addWidget(canvas_freefall)
    dynamic_freefall = QLabel("")
    dynamic_freefall.setWordWrap(True)
    dynamic_freefall.setStyleSheet("background: #e0f7fa; border-radius: 8px; padding: 6px 12px; margin: 4px 0 10px 0; font-size: 13px; color: #00897b;")
    freefall_layout.addWidget(dynamic_freefall)
    r0 = 3
    t = np.linspace(0,1,100)
    def animate_freefall(i):
        r = r0*(1-t)**(2/3)
        idx = min(i, len(t)-1)
        fig_freefall.clear()
        ax = fig_freefall.add_subplot(111)
        ax.plot(t[:idx], r[:idx], color="#1976d2", linewidth=2)
        ax.set_ylim(0,r0+1)
        ax.set_title(f"Caída libre desde r₀={r0:.1f} rₛ", color="#00897b")
        ax.set_xlabel("Tiempo propio (unidades)")
        ax.set_ylabel("r/rₛ")
        canvas_freefall.draw()
        if idx < 30:
            dynamic_freefall.setText("La partícula comienza a caer desde lejos.")
        elif idx < 70:
            dynamic_freefall.setText("La caída se acelera al acercarse al agujero negro.")
        else:
            dynamic_freefall.setText("La partícula cruza el horizonte de eventos.")
    play_btn_freefall = QPushButton("▶ Reproducir video")
    play_btn_freefall.setStyleSheet("background:#00897b; color:white; font-weight:bold; border-radius:8px; padding:6px 18px; margin:8px 0;")
    freefall_layout.addWidget(play_btn_freefall)
    timer_freefall = QTimer()
    timer_freefall.setInterval(40)
    frame_freefall = [0]
    def play_freefall():
        frame_freefall[0] = 0
        timer_freefall.start()
    def update_freefall():
        animate_freefall(frame_freefall[0])
        frame_freefall[0] += 1
        if frame_freefall[0] > 99:
            timer_freefall.stop()
    timer_freefall.timeout.connect(update_freefall)
    play_btn_freefall.clicked.connect(play_freefall)
    animate_freefall(0)
    tabs.addTab(freefall_widget, "Caída Libre en Schwarzschild/Kerr")

    # --- Rotación (Kerr) ---
    kerr_widget = QWidget()
    kerr_layout = QVBoxLayout(kerr_widget)
    title_kerr = QGroupBox("🌀 Rotación (Kerr) (simulación tipo video)")
    title_kerr.setStyleSheet("QGroupBox { font-size: 15px; font-weight: bold; color: #6a1b9a; border-radius: 12px; background: #ede7f6; margin-top: 10px; padding: 10px; }")
    vbox_kerr = QVBoxLayout()
    exp_kerr = QLabel(
        "<b>Simulación tipo video:</b> Visualiza el arrastre de referencia y la ergosfera de un agujero negro en rotación.<br>"
        "<b>Referencia:</b> <a href='https://es.wikipedia.org/wiki/Agujero_negro_de_Kerr' style='color:#6a1b9a; text-decoration:underline;'>Wikipedia</a>"
    )
    exp_kerr.setOpenExternalLinks(True)
    exp_kerr.setWordWrap(True)
    exp_kerr.setStyleSheet("font-size: 14px; color: #6a1b9a; margin-bottom: 8px;")
    vbox_kerr.addWidget(exp_kerr)
    title_kerr.setLayout(vbox_kerr)
    kerr_layout.addWidget(title_kerr)
    fig_kerr = Figure(figsize=(5.5, 3))
    canvas_kerr = FigureCanvas(fig_kerr)
    canvas_kerr.setStyleSheet("border-radius:14px; box-shadow:0 2px 12px #b39ddb; margin:10px 0; background: #ede7f6;")
    kerr_layout.addWidget(canvas_kerr)
    dynamic_kerr = QLabel("")
    dynamic_kerr.setWordWrap(True)
    dynamic_kerr.setStyleSheet("background: #ede7f6; border-radius: 8px; padding: 6px 12px; margin: 4px 0 10px 0; font-size: 13px; color: #6a1b9a;")
    kerr_layout.addWidget(dynamic_kerr)
    theta = np.linspace(0,2*np.pi,200)
    def animate_kerr(i):
        a = 0.01 + 0.98*np.abs(np.sin(i/30))
        r_erg = 1 + np.sqrt(1 - a**2 * np.cos(theta)**2)
        r_hor = 1 + np.sqrt(1 - a**2)
        fig_kerr.clear()
        ax = fig_kerr.add_subplot(111, polar=True)
        ax.plot(theta, r_erg, color="#b26500", linewidth=2, label="Ergosfera")
        ax.plot(theta, np.ones_like(theta)*r_hor, color="#1976d2", linewidth=2, label="Horizonte")
        ax.set_title("Agujero negro de Kerr", color="#6a1b9a")
        ax.set_yticklabels([])
        ax.legend()
        canvas_kerr.draw()
        if a < 0.3:
            dynamic_kerr.setText("El agujero negro rota lentamente, la ergosfera es pequeña.")
        elif a < 0.7:
            dynamic_kerr.setText("La rotación aumenta, la ergosfera se expande.")
        else:
            dynamic_kerr.setText("Rotación máxima: la ergosfera es grande y el horizonte se reduce.")
    play_btn_kerr = QPushButton("▶ Reproducir video")
    play_btn_kerr.setStyleSheet("background:#6a1b9a; color:white; font-weight:bold; border-radius:8px; padding:6px 18px; margin:8px 0;")
    kerr_layout.addWidget(play_btn_kerr)
    timer_kerr = QTimer()
    timer_kerr.setInterval(40)
    frame_kerr = [0]
    def play_kerr():
        frame_kerr[0] = 0
        timer_kerr.start()
    def update_kerr():
        animate_kerr(frame_kerr[0])
        frame_kerr[0] += 1
        if frame_kerr[0] > 90:
            timer_kerr.stop()
    timer_kerr.timeout.connect(update_kerr)
    play_btn_kerr.clicked.connect(play_kerr)
    animate_kerr(0)
    tabs.addTab(kerr_widget, "Rotación (Kerr)")

    # --- Energía y momento ---
    energy_widget = QWidget()
    energy_layout = QVBoxLayout(energy_widget)
    title_energy = QGroupBox("⚡ Energía y Momento en Espacio-Tiempo Curvo (simulación tipo video)")
    title_energy.setStyleSheet("QGroupBox { font-size: 15px; font-weight: bold; color: #1976d2; border-radius: 12px; background: #e3f2fd; margin-top: 10px; padding: 10px; }")
    vbox_energy = QVBoxLayout()
    exp_energy = QLabel(
        "<b>Simulación tipo video:</b> Visualiza la conservación de la energía y el momento en trayectorias relativistas.<br>"
        "<b>Referencia:</b> <a href='https://es.wikipedia.org/wiki/Energ%C3%ADa_en_la_relatvidad_general' style='color:#1976d2; text-decoration:underline;'>Wikipedia</a>"
    )
    exp_energy.setOpenExternalLinks(True)
    exp_energy.setWordWrap(True)
    exp_energy.setStyleSheet("font-size: 14px; color: #1976d2; margin-bottom: 8px;")
    vbox_energy.addWidget(exp_energy)
    title_energy.setLayout(vbox_energy)
    energy_layout.addWidget(title_energy)
    fig_energy = Figure(figsize=(5.5, 3))
    canvas_energy = FigureCanvas(fig_energy)
    canvas_energy.setStyleSheet("border-radius:14px; box-shadow:0 2px 12px #90caf9; margin:10px 0; background: #e3f2fd;")
    energy_layout.addWidget(canvas_energy)
    dynamic_energy = QLabel("")
    dynamic_energy.setWordWrap(True)
    dynamic_energy.setStyleSheet("background: #e3f2fd; border-radius: 8px; padding: 6px 12px; margin: 4px 0 10px 0; font-size: 13px; color: #1976d2;")
    energy_layout.addWidget(dynamic_energy)
    t = np.linspace(0, 2*np.pi, 200)
    E = np.ones_like(t)
    p = np.sin(t)
    def animate_energy(i):
        fig_energy.clear()
        ax = fig_energy.add_subplot(111)
        idx = min(i*2, len(t)-1)
        ax.plot(t[:idx], E[:idx], color="#1976d2", label="Energía")
        ax.plot(t[:idx], p[:idx], color="#b26500", label="Momento")
        ax.set_title("Energía y momento (trayectoria relativista)", color="#1976d2")
        ax.legend()
        canvas_energy.draw()
        if idx < 60:
            dynamic_energy.setText("La energía se mantiene constante, el momento varía.")
        elif idx < 120:
            dynamic_energy.setText("El momento cambia de signo, la energía sigue constante.")
        else:
            dynamic_energy.setText("Ambas magnitudes se visualizan a lo largo de la trayectoria.")
    play_btn_energy = QPushButton("▶ Reproducir video")
    play_btn_energy.setStyleSheet("background:#1976d2; color:white; font-weight:bold; border-radius:8px; padding:6px 18px; margin:8px 0;")
    energy_layout.addWidget(play_btn_energy)
    timer_energy = QTimer()
    timer_energy.setInterval(40)
    frame_energy = [0]
    def play_energy():
        frame_energy[0] = 0
        timer_energy.start()
    def update_energy():
        animate_energy(frame_energy[0])
        frame_energy[0] += 1
        if frame_energy[0] > 100:
            timer_energy.stop()
    timer_energy.timeout.connect(update_energy)
    play_btn_energy.clicked.connect(play_energy)
    animate_energy(0)
    tabs.addTab(energy_widget, "Energía y Momento")

    # --- Explicación final ---
    explicacion = QLabel(
        "<span style='color:#1565c0; font-size:1.08em;'><b>¿Qué muestran estas simulaciones?</b></span> "
        "Aquí puedes explorar efectos avanzados de la relatividad general: ondas gravitacionales, lentes, Doppler, expansión cósmica, agujeros de gusano, colisiones, paradojas y más."
    )
    explicacion.setWordWrap(True)
    explicacion.setStyleSheet("background: #e3f2fd; border-radius: 10px; padding: 10px 16px; margin: 12px 0 12px 0; font-size: 14px; color: #1565c0;")
    layout.addWidget(explicacion)

    tab.setLayout(layout)
    return tab
