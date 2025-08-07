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

    # --- Efecto Doppler relativista (mejorado) ---
    doppler_widget = QWidget()
    doppler_layout = QVBoxLayout(doppler_widget)
    title_doppler = QGroupBox("🌈 Efecto Doppler Relativista (simulación tipo video)")
    title_doppler.setStyleSheet("QGroupBox { font-size: 15px; font-weight: bold; color: #b26500; border-radius: 12px; background: #fffde7; margin-top: 10px; padding: 10px; }")
    vbox_doppler = QVBoxLayout()
    exp_doppler = QLabel(
        "<b>Simulación tipo video:</b> Observa cómo cambia la frecuencia y el color de la luz cuando la fuente se mueve respecto al observador.<br>"
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
    fig_doppler = Figure(figsize=(6, 3.5))
    canvas_doppler = FigureCanvas(fig_doppler)
    canvas_doppler.setStyleSheet("border-radius:14px; box-shadow:0 2px 12px #ffd54f; margin:10px 0; background: #fffde7;")
    doppler_layout.addWidget(canvas_doppler)
    dynamic_doppler = QLabel("")
    dynamic_doppler.setWordWrap(True)
    dynamic_doppler.setStyleSheet("background: #fffde7; border-radius: 8px; padding: 6px 12px; margin: 4px 0 10px 0; font-size: 13px; color: #b26500;")
    doppler_layout.addWidget(dynamic_doppler)

    # Parámetros para la animación
    v = np.linspace(-0.99, 0.99, 120)
    wave_x = np.linspace(0, 2*np.pi, 200)
    color_map = lambda freq: (
        "#1976d2" if freq > 1.05 else "#b26500" if freq < 0.95 else "#43a047"
    )  # azul, rojo, verde (sin corrimiento)

    def animate_doppler(i):
        fig_doppler.clear()
        ax = fig_doppler.add_subplot(111)
        v_now = v[i]
        gamma = 1/np.sqrt(1-v_now**2)
        freq_obs = gamma*(1-v_now)
        # Simula la onda emitida y la onda observada
        y_emit = np.sin(wave_x)
        y_obs = np.sin(wave_x * freq_obs)
        # Color según corrimiento
        color_emit = "#43a047"
        color_obs = color_map(freq_obs)
        # Dibuja fuente y observador
        ax.plot([-2, -1.2], [0, 0], color="#888", linewidth=3)
        ax.plot([2, 1.2], [0, 0], color="#888", linewidth=3)
        ax.plot(-2, 0, marker="o", markersize=18, color="#1976d2" if v_now < 0 else "#b26500")
        ax.plot(2, 0, marker="o", markersize=18, color="#333")
        ax.text(-2, 0.25, "Fuente", fontsize=12, color="#1976d2" if v_now < 0 else "#b26500", ha="center")
        ax.text(2, 0.25, "Observador", fontsize=12, color="#333", ha="center")
        # Dibuja ondas
        ax.plot(wave_x/np.pi-1.5, y_emit, color=color_emit, linewidth=2.5, label="Onda emitida")
        ax.plot(wave_x/np.pi+1.5, y_obs, color=color_obs, linewidth=2.5, label="Onda observada")
        # Flechas de movimiento
        ax.arrow(-2, -0.5, 0.3 if v_now<0 else -0.3, 0, head_width=0.13, head_length=0.13, fc="#1976d2" if v_now<0 else "#b26500", ec="#1976d2" if v_now<0 else "#b26500")
        ax.set_xlim(-2.5, 2.5)
        ax.set_ylim(-1.2, 1.2)
        ax.axis('off')
        ax.legend(loc="upper center", fontsize=10)
        ax.set_title(f"v/c = {v_now:+.2f}   f_obs = {freq_obs:.2f} f_emitida", color=color_obs)
        canvas_doppler.draw()
        # Texto dinámico según el frame
        if v_now < -0.5:
            dynamic_doppler.setText("La fuente se acerca rápidamente: la onda se comprime (corrimiento al azul).")
        elif v_now > 0.5:
            dynamic_doppler.setText("La fuente se aleja rápidamente: la onda se estira (corrimiento al rojo).")
        else:
            dynamic_doppler.setText("La fuente está casi en reposo relativo: no hay corrimiento apreciable.")

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

    # --- Agujero de gusano (simulación mejorada con dos naves en 3D: la verde llega primero) ---
    wormhole_widget = QWidget()
    wormhole_layout = QVBoxLayout(wormhole_widget)
    title_wormhole = QGroupBox("🌀 Agujero de Gusano (simulación tipo video)")
    title_wormhole.setStyleSheet("QGroupBox { font-size: 15px; font-weight: bold; color: #6a1b9a; border-radius: 12px; background: #ede7f6; margin-top: 10px; padding: 10px; }")
    vbox_wormhole = QVBoxLayout()
    exp_wormhole = QLabel(
        "<b>Simulación tipo video:</b> Observa cómo dos naves espaciales parten de A: la gris toma el camino normal (largo) y la verde el atajo del agujero de gusano (corto y rápido).<br>"
        "<b>¿Qué es un agujero de gusano?</b><br>"
        "Es una hipotética 'puerta' que conecta dos regiones distantes del espacio-tiempo.<br>"
        "<b>Referencia:</b> <a href='https://es.wikipedia.org/wiki/Agujero_de_gusano' style='color:#6a1b9a; text-decoration:underline;'>Wikipedia</a>"
    )
    exp_wormhole.setOpenExternalLinks(True)
    exp_wormhole.setWordWrap(True)
    exp_wormhole.setStyleSheet("font-size: 14px; color: #6a1b9a; margin-bottom: 8px;")
    vbox_wormhole.addWidget(exp_wormhole)
    title_wormhole.setLayout(vbox_wormhole)
    wormhole_layout.addWidget(title_wormhole)
    fig_wormhole = Figure(figsize=(6, 4))
    canvas_wormhole = FigureCanvas(fig_wormhole)
    canvas_wormhole.setStyleSheet("border-radius:14px; box-shadow:0 2px 12px #b39ddb; margin:10px 0; background: #ede7f6;")
    wormhole_layout.addWidget(canvas_wormhole)
    dynamic_wormhole = QLabel("")
    dynamic_wormhole.setWordWrap(True)
    dynamic_wormhole.setStyleSheet("background: #ede7f6; border-radius: 8px; padding: 6px 12px; margin: 4px 0 10px 0; font-size: 13px; color: #6a1b9a;")
    wormhole_layout.addWidget(dynamic_wormhole)

    # Parámetros para la animación
    n_frames = 100
    # Puntos de inicio y fin
    A = np.array([-3, 0, 0])
    B = np.array([3, 0, 0])
    # Camino normal (gris, largo, sobre z=0)
    path_normal = np.linspace(A, B, n_frames)
    # Camino atajo (verde): A -> boca_L -> boca_R -> B, pero la nave verde llega antes
    mouth_L = np.array([-1, 0, 0])
    mouth_R = np.array([1, 0, 0])
    # El túnel del agujero de gusano será un arco en z
    tunnel_z = 2.0
    n1 = n_frames // 4
    n2 = n_frames // 4
    n3 = n_frames // 2
    path1 = np.linspace(A, mouth_L, n1)
    # Túnel: de boca_L a boca_R por un arco en z
    tunnel_t = np.linspace(0, np.pi, n2)
    tunnel_path = np.stack([
        np.linspace(mouth_L[0], mouth_R[0], n2),
        np.zeros(n2),
        tunnel_z * np.sin(tunnel_t)
    ], axis=1)
    path2 = np.linspace(mouth_R, B, n3)
    # La nave verde recorre su camino en n1+n2+n3//2 frames (llega antes)
    total_verde = n1 + n2 + n3//2

    def animate_wormhole(i):
        fig_wormhole.clear()
        ax = fig_wormhole.add_subplot(111, projection='3d')
        # Dibuja el espacio normal (camino largo, gris)
        ax.plot(path_normal[:,0], path_normal[:,1], path_normal[:,2], color="#bdbdbd", linewidth=2, linestyle="--", alpha=0.7, label="Camino normal")
        ax.text(-3, 0, 0.5, "A", fontsize=13, color="#1976d2", ha="center")
        ax.text(3, 0, 0.5, "B", fontsize=13, color="#b26500", ha="center")
        # Dibuja las bocas del agujero de gusano
        ax.scatter([mouth_L[0], mouth_R[0]], [mouth_L[1], mouth_R[1]], [mouth_L[2], mouth_R[2]], color="#6a1b9a", s=80, zorder=5)
        ax.text(mouth_L[0], mouth_L[1], 0.7, "Boca 1", color="#6a1b9a", ha="center", fontsize=11)
        ax.text(mouth_R[0], mouth_R[1], 0.7, "Boca 2", color="#6a1b9a", ha="center", fontsize=11)
        # Dibuja el túnel del agujero de gusano (arco en z)
        ax.plot(tunnel_path[:,0], tunnel_path[:,1], tunnel_path[:,2], color="#43a047", linewidth=2.5, linestyle=":", alpha=0.8, label="Túnel (atajo)")
        # Trayectoria nave verde (atajo)
        if i < n1:
            verde = np.concatenate([path1[:i+1], np.tile(mouth_L, (n2,1)), np.tile(mouth_R, (n3//2,1))], axis=0)
            nave_verde = path1[i]
            dynamic_wormhole.setText("Ambas naves parten de A. La nave verde va hacia la boca del agujero de gusano, la gris sigue el camino largo.")
        elif i < n1+n2:
            idx_tun = i-n1
            verde = np.concatenate([path1, tunnel_path[:idx_tun+1], np.tile(mouth_R, (n3//2,1))], axis=0)
            nave_verde = tunnel_path[idx_tun]
            dynamic_wormhole.setText("La nave verde cruza el túnel del agujero de gusano. La gris sigue avanzando por el camino largo.")
        elif i < total_verde:
            idx_path2 = i-(n1+n2)
            verde = np.concatenate([path1, tunnel_path, path2[:idx_path2+1]], axis=0)
            nave_verde = path2[idx_path2]
            if idx_path2 < n3//2-1:
                dynamic_wormhole.setText("La nave verde ya tomó el atajo y está llegando a B. La gris aún no llega.")
            else:
                dynamic_wormhole.setText("La nave verde llegó primero a B usando el agujero de gusano. La gris sigue en camino.")
        else:
            verde = np.concatenate([path1, tunnel_path, path2[:n3//2]], axis=0)
            nave_verde = path2[n3//2-1]
        ax.plot(verde[:,0], verde[:,1], verde[:,2], color="#43a047", linewidth=2.5, label="Nave (atajo)")
        ax.plot(nave_verde[0], nave_verde[1], nave_verde[2], marker="*", markersize=18, color="#43a047", zorder=10)
        # Trayectoria nave gris (camino largo, más lenta)
        idx_lenta = min(i, n_frames-1)
        nave_lenta = path_normal[idx_lenta]
        ax.plot(path_normal[:idx_lenta+1,0], path_normal[:idx_lenta+1,1], path_normal[:idx_lenta+1,2], color="#bdbdbd", linewidth=2, linestyle="--")
        ax.plot(nave_lenta[0], nave_lenta[1], nave_lenta[2], marker="*", markersize=18, color="#bdbdbd", zorder=10)
        # Ajustes de la vista 3D
        ax.set_xlim(-3.5, 3.5)
        ax.set_ylim(-2, 2)
        ax.set_zlim(-0.5, 2.5)
        ax.axis('off')
        ax.set_title("Viaje espacial: camino normal vs. agujero de gusano", color="#6a1b9a", fontsize=14)
        ax.legend(loc="lower center", fontsize=10)
        canvas_wormhole.draw()

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
        if frame_wormhole[0] > n_frames-1:
            timer_wormhole.stop()
    timer_wormhole.timeout.connect(update_wormhole)
    play_btn_wormhole.clicked.connect(play_wormhole)
    animate_wormhole(0)
    tabs.addTab(wormhole_widget, "Agujero de Gusano")

    # --- Expansión del universo (simulación 3D realista con colisión y ondas gravitacionales) ---
    expansion_widget = QWidget()
    expansion_layout = QVBoxLayout(expansion_widget)
    title_expansion = QGroupBox("🌌 Expansión del Universo (simulación 3D realista)")
    title_expansion.setStyleSheet("QGroupBox { font-size: 15px; font-weight: bold; color: #b26500; border-radius: 12px; background: #fffde7; margin-top: 10px; padding: 10px; }")
    vbox_expansion = QVBoxLayout()
    exp_expansion = QLabel(
        "<b>Simulación tipo video 3D:</b> Observa cómo dos galaxias se acercan, colisionan y generan ondas gravitacionales (esferas en expansión), mientras el resto del universo se expande.<br>"
        "<b>Referencia:</b> <a href='https://es.wikipedia.org/wiki/Expansi%C3%B3n_del_universo' style='color:#b26500; text-decoration:underline;'>Wikipedia</a>"
    )
    exp_expansion.setOpenExternalLinks(True)
    exp_expansion.setWordWrap(True)
    exp_expansion.setStyleSheet("font-size: 14px; color: #b26500; margin-bottom: 8px;")
    vbox_expansion.addWidget(exp_expansion)
    title_expansion.setLayout(vbox_expansion)
    expansion_layout.addWidget(title_expansion)
    fig_expansion = Figure(figsize=(9, 7))
    canvas_expansion = FigureCanvas(fig_expansion)
    canvas_expansion.setStyleSheet("border-radius:14px; box-shadow:0 2px 12px #ffd54f; margin:10px 0; background: #fffde7;")
    expansion_layout.addWidget(canvas_expansion)
    dynamic_expansion = QLabel("")
    dynamic_expansion.setWordWrap(True)
    dynamic_expansion.setStyleSheet("background: #fffde7; border-radius: 8px; padding: 6px 12px; margin: 4px 0 10px 0; font-size: 13px; color: #b26500;")
    expansion_layout.addWidget(dynamic_expansion)

    # Parámetros para la animación 3D
    n_galaxies = 12
    np.random.seed(42)
    theta_gal = np.random.uniform(0, 2*np.pi, n_galaxies)
    phi_gal = np.random.uniform(0, np.pi, n_galaxies)
    r0_gal = np.random.uniform(2.5, 4.5, n_galaxies)
    x0 = r0_gal * np.sin(phi_gal) * np.cos(theta_gal)
    y0 = r0_gal * np.sin(phi_gal) * np.sin(theta_gal)
    z0 = r0_gal * np.cos(phi_gal)
    colors = ["#b26500", "#ffd54f", "#ff7043", "#43a047", "#1976d2", "#ab47bc", "#00897b", "#fbc02d", "#c62828", "#00838f", "#6d4c41", "#c0ca33"]

    # Dos galaxias especiales para la colisión
    gA0 = np.array([-5.5, 0, 0])
    gB0 = np.array([5.5, 0, 0])
    gA_color = "#1976d2"
    gB_color = "#d84315"
    t_max = 4.0
    n_frames_exp = 110

    def animate_expansion(i):
        t = t_max * i / n_frames_exp
        scale = np.exp(0.45 * t)
        fig_expansion.clear()
        ax = fig_expansion.add_subplot(111, projection='3d')

        # Trayectorias de galaxias normales (expansión)
        for j in range(n_galaxies):
            traj_t = np.linspace(0, t, i+1)
            traj_scale = np.exp(0.45 * traj_t)
            ax.plot(x0[j]*traj_scale, y0[j]*traj_scale, z0[j]*traj_scale, color=colors[j%len(colors)], alpha=0.18, linewidth=2)

        # Trayectoria de las dos galaxias que colisionan (líneas que se unen)
        t_col = t_max * 0.45
        t_fusion = t_max * 0.55
        if t < t_col:
            frac = t / t_col
            gA = gA0 * (1-frac)
            gB = gB0 * (1-frac)
            ax.plot([gA0[0], gA[0]], [gA0[1], gA[1]], [gA0[2], gA[2]], color=gA_color, linewidth=3, alpha=0.7)
            ax.plot([gB0[0], gB[0]], [gB0[1], gB[1]], [gB0[2], gB[2]], color=gB_color, linewidth=3, alpha=0.7)
            ax.scatter(gA[0], gA[1], gA[2], color=gA_color, s=180, edgecolor="#fffde7", linewidth=2, zorder=5)
            ax.scatter(gB[0], gB[1], gB[2], color=gB_color, s=180, edgecolor="#fffde7", linewidth=2, zorder=5)
            ax.text(gA[0], gA[1], gA[2]+0.3, "G-A", fontsize=13, color=gA_color, ha="center")
            ax.text(gB[0], gB[1], gB[2]+0.3, "G-B", fontsize=13, color=gB_color, ha="center")
            dynamic_expansion.setText("Dos galaxias se acercan en el universo en expansión.")
        elif t < t_fusion:
            frac = (t-t_col)/(t_fusion-t_col)
            ax.plot([gA0[0], 0], [gA0[1], 0], [gA0[2], 0], color=gA_color, linewidth=3, alpha=0.7)
            ax.plot([gB0[0], 0], [gB0[1], 0], [gB0[2], 0], color=gB_color, linewidth=3, alpha=0.7)
            ax.plot([0, 0], [0, 0], [0, 0.5*frac], color="#ab47bc", linewidth=4, alpha=0.7)
            ax.scatter(0, 0, 0.5*frac, color="#ab47bc", s=220, edgecolor="#fffde7", linewidth=2, zorder=6)
            ax.text(0, 0, 0.5*frac+0.3, "Fusión", fontsize=14, color="#ab47bc", ha="center")
            dynamic_expansion.setText("¡Colisión de galaxias! Se fusionan y emiten ondas gravitacionales.")
        else:
            frac = (t-t_fusion)/(t_max-t_fusion)
            fusion_pos = np.array([0,0,0.5]) * (1-frac)
            fusion_exp = fusion_pos * (1+2*frac)
            ax.plot([gA0[0], 0], [gA0[1], 0], [gA0[2], 0], color=gA_color, linewidth=3, alpha=0.7)
            ax.plot([gB0[0], 0], [gB0[1], 0], [gB0[2], 0], color=gB_color, linewidth=3, alpha=0.7)
            ax.plot([0, fusion_exp[0]], [0, fusion_exp[1]], [0.5, fusion_exp[2]], color="#ab47bc", linewidth=4, alpha=0.7)
            ax.scatter(fusion_exp[0], fusion_exp[1], fusion_exp[2], color="#ab47bc", s=220, edgecolor="#fffde7", linewidth=2, zorder=6)
            ax.text(fusion_exp[0], fusion_exp[1], fusion_exp[2]+0.3, "Galaxia fusionada", fontsize=14, color="#ab47bc", ha="center")
            dynamic_expansion.setText("La galaxia fusionada se aleja tras la colisión y la onda gravitacional se expande.")

        # Galaxias normales (expansión)
        for j in range(n_galaxies):
            x = x0[j]*scale
            y = y0[j]*scale
            z = z0[j]*scale
            dist = np.sqrt(x**2 + y**2 + z**2)
            gal_color = colors[j%len(colors)] if dist < 7 else "#d84315"
            ax.scatter(x, y, z, color=gal_color, s=120, edgecolor="#fffde7", linewidth=2, zorder=3)
            ax.text(x, y, z+0.18, f"G{j+1}", fontsize=11, color=gal_color, ha="center")

        # Vía Láctea en el centro
        ax.scatter(0, 0, 0, color="#1976d2", s=180, edgecolor="#fffde7", linewidth=2, zorder=4)
        ax.text(0, 0, -0.45, "Vía Láctea", fontsize=14, color="#1976d2", ha="center")

        # Onda gravitacional tras colisión (esfera en expansión)
        if t > t_fusion:
            gwave_radius = 0.5 + 7.5 * max(0, (t-t_fusion)/(t_max-t_fusion))
            u = np.linspace(0, 2*np.pi, 40)
            v = np.linspace(0, np.pi, 20)
            xg = gwave_radius * np.outer(np.cos(u), np.sin(v))
            yg = gwave_radius * np.outer(np.sin(u), np.sin(v))
            zg = gwave_radius * np.outer(np.ones_like(u), np.cos(v))
            ax.plot_wireframe(xg, yg, zg, color="#90caf9", alpha=0.32, linewidth=1.1)
            ax.plot_wireframe(1.05*xg, 1.05*yg, 1.05*zg, color="#1976d2", alpha=0.13, linewidth=0.7)

        # Ajustes de la vista 3D
        ax.set_xlim(-12, 12)
        ax.set_ylim(-12, 12)
        ax.set_zlim(-8, 8)
        ax.set_box_aspect([1,1,0.7])
        ax.axis('off')
        ax.set_title("Expansión del universo, colisión y ondas gravitacionales", color="#b26500", fontsize=16)
        canvas_expansion.draw()

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
        if frame_expansion[0] > n_frames_exp:
            timer_expansion.stop()
    timer_expansion.timeout.connect(update_expansion)
    play_btn_expansion.clicked.connect(play_expansion)
    animate_expansion(0)
    tabs.addTab(expansion_widget, "Expansión del Universo")

    # --- Colisión de agujeros negros (simulación realista 3D con ondas gravitacionales) ---
    bh_widget = QWidget()
    bh_layout = QVBoxLayout(bh_widget)
    title_bh = QGroupBox("⚫⚫ Colisión de Agujeros Negros (simulación 3D realista)")
    title_bh.setStyleSheet("QGroupBox { font-size: 15px; font-weight: bold; color: #1976d2; border-radius: 12px; background: #e3f2fd; margin-top: 10px; padding: 10px; }")
    vbox_bh = QVBoxLayout()
    exp_bh = QLabel(
        "<b>Simulación tipo video 3D:</b> Visualiza dos agujeros negros orbitando, colisionando y emitiendo ondas gravitacionales (esferas en expansión).<br>"
        "<b>Referencia:</b> <a href='https://es.wikipedia.org/wiki/Onda_gravitacional#Colisi%C3%B3n_de_agujeros_negros' style='color:#1976d2; text-decoration:underline;'>Wikipedia</a>"
    )
    exp_bh.setOpenExternalLinks(True)
    exp_bh.setWordWrap(True)
    exp_bh.setStyleSheet("font-size: 14px; color: #1976d2; margin-bottom: 8px;")
    vbox_bh.addWidget(exp_bh)
    title_bh.setLayout(vbox_bh)
    bh_layout.addWidget(title_bh)
    fig_bh = Figure(figsize=(7, 5))
    canvas_bh = FigureCanvas(fig_bh)
    canvas_bh.setStyleSheet("border-radius:14px; box-shadow:0 2px 12px #90caf9; margin:10px 0; background: #e3f2fd;")
    bh_layout.addWidget(canvas_bh)
    dynamic_bh = QLabel("")
    dynamic_bh.setWordWrap(True)
    dynamic_bh.setStyleSheet("background: #e3f2fd; border-radius: 8px; padding: 6px 12px; margin: 4px 0 10px 0; font-size: 13px; color: #1976d2;")
    bh_layout.addWidget(dynamic_bh)

    # Parámetros de la simulación
    n_frames_bh = 120
    t_max_bh = 2 * np.pi
    r_orbit = 3.5
    z_orbit = 0.0
    merge_frame = n_frames_bh // 2
    gwave_duration = n_frames_bh // 2

    def animate_bh(i):
        fig_bh.clear()
        ax = fig_bh.add_subplot(111, projection='3d')
        t = t_max_bh * i / n_frames_bh
        # Antes de la fusión: órbitas espirales
        if i < merge_frame:
            # Espiral hacia el centro
            frac = i / merge_frame
            r_now = r_orbit * (1 - 0.7 * frac)
            theta = t * 1.5
            x1 = r_now * np.cos(theta)
            y1 = r_now * np.sin(theta)
            z1 = z_orbit
            x2 = -r_now * np.cos(theta)
            y2 = -r_now * np.sin(theta)
            z2 = z_orbit
            # Trayectorias
            n_traj = 80
            traj_t = np.linspace(0, t, n_traj)
            traj_r = r_orbit * (1 - 0.7 * traj_t / t_max_bh)
            ax.plot(traj_r * np.cos(traj_t*1.5), traj_r * np.sin(traj_t*1.5), np.zeros(n_traj), color="#1976d2", alpha=0.5, linewidth=2)
            ax.plot(-traj_r * np.cos(traj_t*1.5), -traj_r * np.sin(traj_t*1.5), np.zeros(n_traj), color="#b26500", alpha=0.5, linewidth=2)
            # Agujeros negros
            ax.scatter(x1, y1, z1, color="#1976d2", s=300, edgecolor="#fff", linewidth=2, zorder=5)
            ax.scatter(x2, y2, z2, color="#b26500", s=300, edgecolor="#fff", linewidth=2, zorder=5)
            ax.text(x1, y1, z1+0.3, "BH-1", fontsize=13, color="#1976d2", ha="center")
            ax.text(x2, y2, z2+0.3, "BH-2", fontsize=13, color="#b26500", ha="center")
            dynamic_bh.setText("Los agujeros negros orbitan y se acercan, perdiendo energía por ondas gravitacionales.")
        else:
            # Fusión y emisión de onda gravitacional
            frac = (i - merge_frame) / (n_frames_bh - merge_frame)
            # Posición fusionada
            x1 = x2 = y1 = y2 = z1 = z2 = 0
            ax.scatter(0, 0, 0, color="#ab47bc", s=420, edgecolor="#fff", linewidth=2, zorder=6)
            ax.text(0, 0, 0.4, "BH fusionado", fontsize=15, color="#ab47bc", ha="center")
            # Onda gravitacional: esfera en expansión
            gwave_radius = 0.5 + 7.0 * frac
            u = np.linspace(0, 2*np.pi, 40)
            v = np.linspace(0, np.pi, 20)
            xg = gwave_radius * np.outer(np.cos(u), np.sin(v))
            yg = gwave_radius * np.outer(np.sin(u), np.sin(v))
            zg = gwave_radius * np.outer(np.ones_like(u), np.cos(v))
            ax.plot_wireframe(xg, yg, zg, color="#90caf9", alpha=0.32, linewidth=1.1)
            ax.plot_wireframe(1.05*xg, 1.05*yg, 1.05*zg, color="#1976d2", alpha=0.13, linewidth=0.7)
            dynamic_bh.setText("¡Colisión! Los agujeros negros se fusionan y emiten una onda gravitacional que se expande por el espacio.")

        # Ajustes de la vista 3D
        ax.set_xlim(-8, 8)
        ax.set_ylim(-8, 8)
        ax.set_zlim(-3, 3)
        ax.set_box_aspect([1,1,0.5])
        ax.axis('off')
        ax.set_title("Colisión de agujeros negros y ondas gravitacionales", color="#1976d2", fontsize=15)
        canvas_bh.draw()

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
        if frame_bh[0] > n_frames_bh:
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
