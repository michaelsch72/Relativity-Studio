import pytest
from PyQt5.QtWidgets import QApplication
import sys

import relativity_studio

@pytest.fixture(scope="module")
def app():
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    return app

def test_mainwindow_tabs(app):
    window = relativity_studio.MainWindow()
    tab_titles = [window.tabs.tabText(i) for i in range(window.tabs.count())]
    assert "Introducción" in tab_titles
    assert "Dilatación Temporal" in tab_titles
    assert "Curvatura Espacio-Tiempo" in tab_titles
    assert "Geodésicas Numéricas" in tab_titles
    assert "Deflexión de la Luz" in tab_titles
    assert "Órbitas Relativistas" in tab_titles

def test_numeric_geodesics_tab_widget_types(app):
    window = relativity_studio.MainWindow()
    tab = window.create_numeric_geodesics_tab()
    assert tab.layout() is not None
    assert tab.layout().count() > 0

def test_curvature_tab_widget_types(app):
    window = relativity_studio.MainWindow()
    tab = window.create_curvature_tab()
    assert tab.layout() is not None
    assert tab.layout().count() > 0

def test_time_dilation_tab_widget_types(app):
    window = relativity_studio.MainWindow()
    tab = window.create_time_dilation_tab()
    assert tab.layout() is not None
    assert tab.layout().count() > 0


# --- Pruebas físicas y numéricas ---
import numpy as np

def test_gravitational_time_dilation_formula():
    # Tierra
    G = 6.67430e-11
    M = 5.972e24
    R = 6.371e6
    c = 299792458
    delta_t = 86400
    r = R
    factor = np.sqrt(1 - 2 * G * M / (r * c ** 2))
    delta_tau = delta_t * factor
    # Valor esperado cerca de la superficie (debe ser menor que delta_t)
    assert delta_tau < delta_t
    # Diferencia con altitud GPS (~20200 km)
    r_gps = R + 20200e3
    factor_gps = np.sqrt(1 - 2 * G * M / (r_gps * c ** 2))
    delta_tau_gps = delta_t * factor_gps
    diff = delta_tau_gps - delta_tau
    # Debe ser positivo y del orden de decenas de microsegundos
    assert diff > 0
    assert 30 < diff * 1e6 < 60

def test_light_deflection_formula():
    # Parámetros del Sol
    G = 6.67430e-11
    M = 1.98847e30
    R = 6.9634e8
    c = 299792458
    b = R
    delta_theta = 4 * G * M / (c**2 * b)
    delta_theta_arcsec = delta_theta * (180/np.pi) * 3600
    # Valor esperado: ~1.75 segundos de arco
    assert 1.6 < delta_theta_arcsec < 1.9

def test_schwarzschild_radius():
    G = 6.67430e-11
    M = 1.98847e30
    c = 299792458
    rs = 2 * G * M / c**2
    # Radio de Schwarzschild del Sol ~2953 km
    assert 2900e3 < rs < 3000e3

def test_orbit_precession_formula():
    G = 6.67430e-11
    M = 1.98847e30
    c = 299792458
    a = 5.791e10
    e = 0.206
    delta_phi = 6 * np.pi * G * M / (a * (1 - e**2) * c**2)
    delta_phi_arcsec = delta_phi * (180/np.pi) * 3600
    # Precesión por revolución de Mercurio ~0.1035 arcsec
    assert 0.09 < delta_phi_arcsec < 0.12
