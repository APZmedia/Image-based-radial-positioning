import json
import numpy as np
import pandas as pd
from scipy.signal import savgol_filter
from scipy.interpolate import UnivariateSpline

def fit_sinusoidal_trend(angular_positions, values):
    """
    Ajusta un modelo sinusoidal a los datos de orientación dentro de cada secuencia.
    Si no se puede ajustar, usa una interpolación cúbica para mayor estabilidad.
    """
    if len(angular_positions) < 3:
        return lambda x: np.mean(values)  # Si hay pocos datos, se usa la media

    from scipy.optimize import curve_fit

    def sinusoidal(x, A, B, C, D):
        return A * np.sin(B * x + C) + D

    try:
        params, _ = curve_fit(sinusoidal, angular_positions, values, 
                              p0=[np.std(values), 2 * np.pi / (max(angular_positions) - min(angular_positions) + 1), 0, np.mean(values)],
                              maxfev=5000)
        return lambda x: sinusoidal(x, *params)
    except RuntimeError:
        print("⚠️ Advertencia: No se pudo ajustar la curva sinusoidal, se usará una spline cúbica como fallback.")
        return UnivariateSpline(angular_positions, values, k=3, s=0.5)

def normalize_kappa(kappa_values):
    """ 
    Ajusta Kappa para que sea una variable continua en lugar de cíclica.
    """
    kappa_values = np.unwrap(np.radians(kappa_values))  # Convertir a radianes y eliminar discontinuidad
    return np.degrees(kappa_values)  # Convertir de nuevo a grados

def compute_sinusoidal_offsets(sequence_items):
    """
    Calcula la tendencia sinusoidal para Omega y Phi y una interpolación lineal modular para Kappa dentro de cada secuencia.
    """
    if len(sequence_items) < 3:
        return None

    angular_positions = np.array([item["Angular position"] for item in sequence_items])
    omega_values = np.array([item["Omega"] for item in sequence_items])
    phi_values = np.array([item["Phi"] for item in sequence_items])
    kappa_values = np.array([item["Kappa"] for item in sequence_items])

    # 📌 Ordenar por posición angular para evitar errores de interpolación
    sorted_indices = np.argsort(angular_positions)
    angular_positions = angular_positions[sorted_indices]
    omega_values = omega_values[sorted_indices]
    phi_values = phi_values[sorted_indices]
    kappa_values = kappa_values[sorted_indices]

    # 📌 Eliminar duplicados en "Angular Position"
    _, unique_indices = np.unique(angular_positions, return_index=True)
    angular_positions = angular_positions[unique_indices]
    omega_values = omega_values[unique_indices]
    phi_values = phi_values[unique_indices]
    kappa_values = kappa_values[unique_indices]

    # Aplicar suavizado Savitzky-Golay para Omega y Phi
    window_size = min(11, len(angular_positions)) if len(angular_positions) > 3 else len(angular_positions)
    poly_order = 3 if window_size > 3 else 1

    omega_values_smooth = savgol_filter(omega_values, window_size, poly_order)
    phi_values_smooth = savgol_filter(phi_values, window_size, poly_order)

    # 📌 Normalizar Kappa en el rango [-180, 180] antes de la interpolación
    kappa_values = np.unwrap(np.radians(kappa_values))  # Eliminar saltos en ±180°
    kappa_values = np.degrees(kappa_values)

    # 📌 Ajustar interpolación lineal para Kappa respetando la continuidad
    kappa_slope, kappa_intercept = np.polyfit(angular_positions, kappa_values, 1)

    def kappa_trend(x):
        kappa_interp = kappa_slope * x + kappa_intercept
        return (kappa_interp + 180) % 360 - 180  # Mantener siempre en [-180, 180]

    omega_trend = fit_sinusoidal_trend(angular_positions, omega_values_smooth)
    phi_trend = fit_sinusoidal_trend(angular_positions, phi_values_smooth)

    return omega_trend, phi_trend, kappa_trend  # Kappa corregido


def apply_orientation_correction(sequence_items, omega_trend, phi_trend, kappa_trend):
    """
    Aplica la corrección basada en la posición angular dentro de la secuencia.
    """
    for item in sequence_items:
        if item.get("Calibration_Status") in ["visually calibrated", "estimated"]:
            x = item["Angular position"]
            item["Omega"] = omega_trend(x)
            item["Phi"] = phi_trend(x)
            item["Kappa"] = kappa_trend(x)  # Ahora Kappa sigue una progresión lineal

def propagate_orientation(json_input_path, json_output_path):
    """
    Corrige la orientación de imágenes no originales usando ajustes sinusoidales y lineales dentro de cada secuencia.
    """
    with open(json_input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    for step, info in data.items():
        items = info.get("items", [])
        sequences = {}

        # Agrupar por secuencia
        for item in items:
            seq_id = item.get("Sequence", "Unknown")
            if seq_id not in sequences:
                sequences[seq_id] = []
            sequences[seq_id].append(item)

        # Procesar cada secuencia individualmente
        for seq_id, sequence_items in sequences.items():
            originals = [it for it in sequence_items if it.get("Calibration_Status") == "original"]
            if len(originals) < 3:
                continue

            omega_trend, phi_trend, kappa_trend = compute_sinusoidal_offsets(originals)
            apply_orientation_correction(sequence_items, omega_trend, phi_trend, kappa_trend)

    with open(json_output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    print(f"✅ Propagación de orientación corregida con Kappa lineal. Archivo guardado en {json_output_path}")
