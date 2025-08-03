"""
Lanzador principal de Relativity Studio
"""
import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QLabel, QSlider, QHBoxLayout
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from scipy.integrate import solve_ivp

class MainWindow(QMainWindow):
    def create_numeric_geodesics_tab(self):
        from PyQt5.QtWidgets import QComboBox
        tab = QWidget()
        layout = QVBoxLayout()
        label = QLabel("""
<div style='background:linear-gradient(120deg,#e0f7fa 60%,#b2ebf2 100%); border-radius:18px; box-shadow:0 4px 18px #0001; padding:20px 18px 18px 18px; margin-bottom:18px; font-family:Segoe UI,Arial,sans-serif;'>
<h2 style='color:#00897b; font-size:1.7em; margin-top:0; margin-bottom:10px; letter-spacing:1px; text-shadow:0 2px 8px #0002;'>Geodésicas numéricas <span style="font-size:0.7em; color:#555;">(Schwarzschild)</span></h2>
<div style='font-size:1.1em; margin-bottom:10px;'><b>¿Cómo se mueven la luz y las partículas en el espacio-tiempo curvo?</b></div>
<div style='margin-bottom:8px;'><b>Explicación:</b> Las geodésicas son las trayectorias más "rectas" posibles en un espacio-tiempo curvado. En Schwarzschild, describen cómo la gravedad afecta el movimiento de la luz y de las partículas.</div>
<div style='margin-bottom:8px;'><b>Visualización:</b> <span style='color:#00897b;'>Ajusta el parámetro de impacto y elige el tipo de partícula para ver la trayectoria real en el espacio-tiempo curvo.</span></div>
<div style='margin-bottom:8px;'><b>Fórmulas:</b>
<ul style='margin:0 0 0 18px;'>
<li>Para luz: <span style='background:#fffde7; border-radius:8px; padding:2px 8px; color:#b26500; font-weight:bold;'>d²r/dφ² = r - 3rₛ/2</span></li>
<li>Para partículas: <span style='background:#fffde7; border-radius:8px; padding:2px 8px; color:#b26500;'>ecuación similar, pero con energía y masa</span></li>
</ul></div>
<div style='margin-bottom:8px;'><b>Historia:</b> <span style='color:#00897b;'>El cálculo de geodésicas permitió predecir la precesión del perihelio de Mercurio y la deflexión de la luz.</span></div>
<div style='font-size:0.98em;'><b>Referencia:</b> <a href='https://es.wikipedia.org/wiki/Geod%C3%A9sica' style='color:#00897b; text-decoration:underline;'>Wikipedia</a></div>
</div>
        """)
        label.setOpenExternalLinks(True)
        label.setWordWrap(True)
        layout.addWidget(label)

        controls = QHBoxLayout()
        slider_label = QLabel("Parámetro de impacto b:")
        slider = QSlider(Qt.Horizontal)
        slider.setMinimum(15)
        slider.setMaximum(100)
        slider.setValue(30)
        slider.setTickInterval(1)
        slider.setTickPosition(QSlider.TicksBelow)
        value_label = QLabel("3.0")
        controls.addWidget(slider_label)
        controls.addWidget(slider)
        controls.addWidget(value_label)

        type_label = QLabel("Tipo:")
        type_combo = QComboBox()
        type_combo.addItems(["Luz", "Partícula con masa"])
        controls.addWidget(type_label)
        controls.addWidget(type_combo)
        layout.addLayout(controls)

        fig = Figure(figsize=(4,4))
        canvas = FigureCanvas(fig)
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
            pr0 = -0.1
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
                fig.clear()
                ax = fig.add_subplot(111)
                ax.plot(x, y, label="Trayectoria")
                ax.plot(0, 0, 'ko', markersize=10, label="Masa central")
                ax.set_aspect('equal')
                ax.set_xlabel("x")
                ax.set_ylabel("y")
                ax.set_title("Geodésica en Schwarzschild")
                ax.legend()
                ax.grid(True)
                canvas.draw()
            except Exception as e:
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

        tab.setLayout(layout)
        return tab

    def create_curvature_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        label = QLabel("""
<div style='background:linear-gradient(120deg,#ede7f6 60%,#b39ddb 100%); border-radius:18px; box-shadow:0 4px 18px #0001; padding:20px 18px 18px 18px; margin-bottom:18px; font-family:Segoe UI,Arial,sans-serif;'>
<h2 style='color:#6a1b9a; font-size:1.7em; margin-top:0; margin-bottom:10px; letter-spacing:1px; text-shadow:0 2px 8px #0002;'>Curvatura del espacio-tiempo</h2>
<div style='font-size:1.1em; margin-bottom:10px;'><b>¿Cómo se deforma el espacio-tiempo cerca de una masa?</b></div>
<div style='margin-bottom:8px;'><b>Explicación:</b> La relatividad general describe la gravedad como la curvatura del espacio-tiempo causada por la masa y la energía. Cerca de una masa puntual, el espacio se "hunde" y las trayectorias de los objetos se curvan.</div>
<div style='margin-bottom:8px;'><b>Visualización:</b> <span style='color:#6a1b9a;'>Ajusta el radio de Schwarzschild (rₛ) para ver cómo cambia la curvatura.</span></div>
<div style='margin-bottom:8px;'><b>Fórmula:</b> <span style='background:#fffde7; border-radius:8px; padding:2px 8px; color:#b26500; font-weight:bold;'>z(r) = 2√[rₛ(r - rₛ)]</span></div>
<ul style='margin:0 0 0 18px;'>
<li><b>z(r):</b> altura de la superficie embebida</li>
<li><b>rₛ:</b> radio de Schwarzschild</li>
<li><b>r:</b> distancia radial</li>
</ul>
<div style='margin-bottom:8px;'><b>Historia:</b> <span style='color:#6a1b9a;'>Esta visualización fue propuesta por Flamm en 1916, poco después de la publicación de la teoría de Einstein.</span></div>
<div style='font-size:0.98em;'><b>Referencia:</b> <a href='https://es.wikipedia.org/wiki/Soluci%C3%B3n_de_Schwarzschild' style='color:#6a1b9a; text-decoration:underline;'>Wikipedia</a></div>
</div>
        """)
        label.setOpenExternalLinks(True)
        label.setWordWrap(True)
        layout.addWidget(label)

        # Slider para r_s
        slider_layout = QHBoxLayout()
        slider_label = QLabel("Radio de Schwarzschild rₛ:")
        slider = QSlider(Qt.Horizontal)
        slider.setMinimum(5)
        slider.setMaximum(50)
        slider.setValue(10)
        slider.setTickInterval(1)
        slider.setTickPosition(QSlider.TicksBelow)
        value_label = QLabel("1.0")
        slider_layout.addWidget(slider_label)
        slider_layout.addWidget(slider)
        slider_layout.addWidget(value_label)
        layout.addLayout(slider_layout)

        fig = Figure(figsize=(4,3))
        canvas = FigureCanvas(fig)
        layout.addWidget(canvas)

        def plot_curvature():
            rs = slider.value() / 10
            value_label.setText(f"{rs:.1f}")
            r = np.linspace(rs + 0.01, rs * 6, 300)
            z = 2 * np.sqrt(rs * (r - rs))
            fig.clear()
            ax = fig.add_subplot(111)
            ax.plot(r, z, color='#8e24aa', label="Superficie embebida")
            ax.set_xlabel("r (radio)")
            ax.set_ylabel("z (curvatura)")
            ax.set_title(f"Curvatura del espacio-tiempo (rₛ = {rs:.1f})")
            ax.grid(True)
            ax.legend()
            canvas.draw()

        slider.valueChanged.connect(plot_curvature)
        value_label.setText(f"{slider.value()/10:.1f}")
        plot_curvature()

        tab.setLayout(layout)
        return tab

    def create_time_dilation_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        label = QLabel("""
<div style='background:linear-gradient(120deg,#e3f2fd 60%,#90caf9 100%); border-radius:18px; box-shadow:0 4px 18px #0001; padding:20px 18px 18px 18px; margin-bottom:18px; font-family:Segoe UI,Arial,sans-serif;'>
<h2 style='color:#1565c0; font-size:1.7em; margin-top:0; margin-bottom:10px; letter-spacing:1px; text-shadow:0 2px 8px #0002;'>Dilatación temporal gravitacional</h2>
<div style='font-size:1.1em; margin-bottom:10px;'><b>¿Sabías que el tiempo transcurre más lento cerca de objetos masivos?</b></div>
<div style='margin-bottom:8px;'><b>Explicación:</b> Según la relatividad general, la presencia de una masa deforma el espacio-tiempo y ralentiza el paso del tiempo en su proximidad. Este efecto es medible, por ejemplo, en satélites GPS y cerca de agujeros negros.</div>
<div style='margin-bottom:8px;'><b>Fórmula:</b> <span style='background:#fffde7; border-radius:8px; padding:2px 8px; color:#b26500; font-weight:bold;'>Δt' = Δt · √(1 - rₛ/r)</span></div>
<ul style='margin:0 0 0 18px;'>
<li><b>Δt'</b>: tiempo propio (cerca de la masa)</li>
<li><b>Δt</b>: tiempo lejano (lejos de la masa)</li>
<li><b>rₛ</b>: radio de Schwarzschild</li>
<li><b>r</b>: distancia al centro de la masa</li>
</ul>
<div style='margin-bottom:8px;'><b>Historia:</b> <span style='color:#1565c0;'>Este fenómeno fue predicho por Einstein en 1916 y confirmado experimentalmente con relojes atómicos en diferentes alturas.</span></div>
<div style='font-size:0.98em;'><b>Referencia:</b> <a href='https://es.wikipedia.org/wiki/Dilataci%C3%B3n_del_tiempo_gravitacional' style='color:#1565c0; text-decoration:underline;'>Wikipedia</a></div>
</div>
        """)
        label.setOpenExternalLinks(True)
        label.setWordWrap(True)
        layout.addWidget(label)

        slider_layout = QHBoxLayout()
        slider_label = QLabel("r/rₛ:")
        slider = QSlider(Qt.Horizontal)
        slider.setMinimum(11)
        slider.setMaximum(100)
        slider.setValue(20)
        slider.setTickInterval(1)
        slider.setTickPosition(QSlider.TicksBelow)
        value_label = QLabel("2.0")
        slider_layout.addWidget(slider_label)
        slider_layout.addWidget(slider)
        slider_layout.addWidget(value_label)
        layout.addLayout(slider_layout)

        result_label = QLabel()
        layout.addWidget(result_label)

        fig = Figure(figsize=(4,2))
        canvas = FigureCanvas(fig)
        layout.addWidget(canvas)

        def update():
            r_over_rs = slider.value() / 10
            value_label.setText(f"{r_over_rs:.1f}")
            rs = 1.0
            r = r_over_rs * rs
            if r <= rs:
                result_label.setText("<span style='color:red;'>r debe ser mayor que rₛ</span>")
                return
            dilation = np.sqrt(1 - rs/r)
            result_label.setText(f"<b>Relación temporal:</b> Δt'/Δt = <span style='color:#1565c0;'>{dilation:.5f}</span>")
            fig.clear()
            ax = fig.add_subplot(111)
            r_vals = np.linspace(1.01, 10, 200)
            y = np.sqrt(1 - 1/r_vals)
            ax.plot(r_vals, y, color='#1976d2')
            ax.axvline(r_over_rs, color='r', linestyle='--')
            ax.set_xlabel("r/rₛ")
            ax.set_ylabel("Δt'/Δt")
            ax.set_title("Dilatación temporal gravitacional")
            ax.grid(True)
            canvas.draw()

        slider.valueChanged.connect(update)
        value_label.setText(f"{slider.value()/10:.1f}")
        update()

        tab.setLayout(layout)
        return tab

    def create_intro_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        label = QLabel("""
<div style='background:linear-gradient(120deg,#f5fafd 60%,#e3f2fd 100%); border-radius:22px; box-shadow:0 6px 24px #0002; padding:32px 28px 24px 28px; margin:18px 0 24px 0; font-family:Segoe UI,Arial,sans-serif;'>
  <h1 style='color:#01579b; font-size:2.5em; margin-top:0; margin-bottom:8px; letter-spacing:2px; text-shadow:0 2px 12px #0001;'>Relativity Studio</h1>
  <div style='font-size:1.3em; color:#0277bd; margin-bottom:18px; font-weight:bold;'>Explora la relatividad general de forma interactiva y didáctica</div>
  <div style='font-size:1.1em; color:#333; margin-bottom:18px;'>
    Bienvenido a <span style='color:#01579b; font-weight:bold;'>Relativity Studio</span>, tu enciclopedia visual y simulador interactivo de los fenómenos más fascinantes de la relatividad general. Aprende, experimenta y visualiza conceptos clave de la física moderna de manera intuitiva.
  </div>
  <div style='margin:18px 0 18px 0; padding:18px 18px 12px 18px; background:rgba(255,255,255,0.95); border-radius:16px; box-shadow:0 2px 12px #0277bd22;'>
    <ul style='list-style:none; padding:0; margin:0;'>
      <li style='margin-bottom:12px;'><span style='font-size:1.5em; margin-right:8px;'>⏳</span><b>Dilatación temporal:</b> Descubre cómo el tiempo se ralentiza cerca de objetos masivos.</li>
      <li style='margin-bottom:12px;'><span style='font-size:1.5em; margin-right:8px;'>🌌</span><b>Curvatura:</b> Visualiza la deformación del espacio-tiempo.</li>
      <li style='margin-bottom:12px;'><span style='font-size:1.5em; margin-right:8px;'>🌀</span><b>Geodésicas:</b> Simula trayectorias de luz y partículas.</li>
      <li style='margin-bottom:12px;'><span style='font-size:1.5em; margin-right:8px;'>💡</span><b>Deflexión de la luz:</b> Observa cómo la gravedad curva la luz.</li>
      <li style='margin-bottom:0;'><span style='font-size:1.5em; margin-right:8px;'>🔵</span><b>Órbitas relativistas:</b> Explora órbitas no-newtonianas.</li>
    </ul>
  </div>
  <div style='margin-top:18px; font-size:1.05em; color:#444;'>
    <b>Referencias:</b> 
    <a href='https://es.wikipedia.org/wiki/Relatividad_general' style='color:#0277bd; text-decoration:underline; font-weight:bold;'>Wikipedia</a> |
    <a href='https://einstein-online.info/en/spotlight/changing_places/' style='color:#0277bd; text-decoration:underline; font-weight:bold;'>Einstein Online</a>
  </div>
</div>
        """)
        label.setOpenExternalLinks(True)
        label.setWordWrap(True)
        layout.addWidget(label)
        tab.setLayout(layout)
        return tab

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Relativity Studio - Relatividad General Didáctica")
        self.setGeometry(100, 100, 1000, 700)
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        self.init_tabs()

    def init_tabs(self):
        self.tabs.addTab(self.create_intro_tab(), "Introducción")
        self.tabs.addTab(self.create_time_dilation_tab(), "Dilatación Temporal")
        self.tabs.addTab(self.create_curvature_tab(), "Curvatura Espacio-Tiempo")
        self.tabs.addTab(self.create_numeric_geodesics_tab(), "Geodésicas Numéricas")
        self.tabs.addTab(self.create_light_deflection_tab(), "Deflexión de la Luz")
        self.tabs.addTab(self.create_orbits_tab(), "Órbitas Relativistas")

    def create_light_deflection_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        label = QLabel("""
<div style='background:linear-gradient(120deg,#fffde7 60%,#ffe0b2 100%); border-radius:18px; box-shadow:0 4px 18px #0001; padding:20px 18px 18px 18px; margin-bottom:18px; font-family:Segoe UI,Arial,sans-serif;'>
<h2 style='color:#ef6c00; font-size:1.7em; margin-top:0; margin-bottom:10px; letter-spacing:1px; text-shadow:0 2px 8px #0002;'>Deflexión de la luz</h2>
<div style='font-size:1.1em; margin-bottom:10px;'><b>¿Por qué la luz se curva cerca de una masa?</b></div>
<div style='margin-bottom:8px;'><b>Explicación:</b> La relatividad general predice que la luz sigue geodésicas en el espacio-tiempo curvado. Al pasar cerca de una masa, su trayectoria se desvía.</div>
<div style='margin-bottom:8px;'><b>Visualización:</b> <span style='color:#ef6c00;'>Ajusta el parámetro de impacto para ver cómo cambia la desviación.</span></div>
<div style='margin-bottom:8px;'><b>Fórmula:</b> <span style='background:#fffde7; border-radius:8px; padding:2px 8px; color:#b26500; font-weight:bold;'>Δφ ≈ 4GM/(c²b)</span> <span style='font-size:0.95em;'>(aproximación para campos débiles)</span></div>
<ul style='margin:0 0 0 18px;'>
<li><b>Δφ:</b> ángulo de deflexión</li>
<li><b>b:</b> parámetro de impacto</li>
<li><b>G, M, c:</b> constantes universales</li>
</ul>
<div style='margin-bottom:8px;'><b>Historia:</b> <span style='color:#ef6c00;'>La deflexión de la luz fue confirmada en 1919 durante un eclipse solar, validando la teoría de Einstein.</span></div>
<div style='font-size:0.98em;'><b>Referencia:</b> <a href='https://es.wikipedia.org/wiki/Deflexi%C3%B3n_de_la_luz' style='color:#ef6c00; text-decoration:underline;'>Wikipedia</a></div>
</div>
        """)
        label.setOpenExternalLinks(True)
        label.setWordWrap(True)
        layout.addWidget(label)

        slider_layout = QHBoxLayout()
        slider_label = QLabel("Parámetro de impacto b:")
        slider = QSlider(Qt.Horizontal)
        slider.setMinimum(15)
        slider.setMaximum(100)
        slider.setValue(30)
        slider.setTickInterval(1)
        slider.setTickPosition(QSlider.TicksBelow)
        value_label = QLabel("3.0")
        slider_layout.addWidget(slider_label)
        slider_layout.addWidget(slider)
        slider_layout.addWidget(value_label)
        layout.addLayout(slider_layout)

        fig = Figure(figsize=(4,4))
        canvas = FigureCanvas(fig)
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
            ax.set_xlabel("x")
            ax.set_ylabel("y")
            ax.set_title("Deflexión de la luz por gravedad")
            ax.legend()
            ax.grid(True)
            canvas.draw()

        slider.valueChanged.connect(plot_deflection)
        value_label.setText(f"{slider.value()/10:.1f}")
        plot_deflection()

        tab.setLayout(layout)
        return tab

    def create_orbits_tab(self):
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
        label.setOpenExternalLinks(True)
        label.setWordWrap(True)
        layout.addWidget(label)

        slider_layout = QHBoxLayout()
        slider_label = QLabel("Momento angular L:")
        slider = QSlider(Qt.Horizontal)
        slider.setMinimum(35)
        slider.setMaximum(100)
        slider.setValue(50)
        slider.setTickInterval(1)
        slider.setTickPosition(QSlider.TicksBelow)
        value_label = QLabel("5.0")
        slider_layout.addWidget(slider_label)
        slider_layout.addWidget(slider)
        slider_layout.addWidget(value_label)
        layout.addLayout(slider_layout)

        fig = Figure(figsize=(4,4))
        canvas = FigureCanvas(fig)
        layout.addWidget(canvas)

        def orbit_rhs(phi, y, L):
            r, pr = y
            rs = 1.0
            f = 1 - rs/r
            # Ecuación relativista para órbitas (Schwarzschild)
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
                fig.clear()
                ax = fig.add_subplot(111)
                ax.plot(x, y, color='#0277bd', label="Órbita relativista")
                ax.plot(0, 0, 'ko', markersize=10, label="Masa central")
                ax.set_aspect('equal')
                ax.set_xlabel("x")
                ax.set_ylabel("y")
                ax.set_title("Órbita en Schwarzschild")
                ax.legend()
                ax.grid(True)
                canvas.draw()
            except Exception as e:
                fig.clear()
                ax = fig.add_subplot(111)
                ax.text(0.5, 0.5, f"Error en la integración:\n{str(e)}", ha='center', va='center', fontsize=12, color='red', transform=ax.transAxes)
                ax.set_xticks([])
                ax.set_yticks([])
                canvas.draw()

        slider.valueChanged.connect(plot_orbit)
        value_label.setText(f"{slider.value()/10:.1f}")
        plot_orbit()

        tab.setLayout(layout)
        return tab

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
