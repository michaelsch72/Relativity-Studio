from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

def create_intro_tab():
    tab = QWidget()
    layout = QVBoxLayout()
    label = QLabel("""
<div style='text-align:center; margin-top:10px; margin-bottom:0;'>
  <span style='font-size:8em; display:inline-block; margin-bottom:18px; text-shadow:0 8px 32px #0277bd55, 0 2px 0 #fff;'>🌀</span>
</div>
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
