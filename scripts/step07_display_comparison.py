import json
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def visualize_camera_positions(json_file_path, selected_sequences=None):
    """
    Genera una visualización con tres gráficos (Omega, Phi, Kappa vs Angular Position) por cada secuencia seleccionada.
    - Muestra distintos colores según `Calibration Status`:
        - 🔴 **Rojo** para "original"
        - 🔵 **Azul** para "visually calibrated"
        - 🟢 **Verde** para "estimated"

    Parámetros:
    - json_file_path: Ruta del JSON con los datos.
    - selected_sequences: Lista de secuencias a visualizar (opcional). Si es None, se visualizan todas.

    Retorna:
    - Un gráfico Plotly con subplots.
    """
    with open(json_file_path, "r", encoding="utf-8") as f:
        json_data = json.load(f)

    all_figs = []  # Lista para almacenar los subplots

    for step_name, step_info in json_data.items():
        if selected_sequences and step_name not in selected_sequences:
            continue  # Saltamos si la secuencia no está seleccionada

        angular_positions = {"original": [], "visually calibrated": [], "estimated": []}
        omega_values = {"original": [], "visually calibrated": [], "estimated": []}
        phi_values = {"original": [], "visually calibrated": [], "estimated": []}
        kappa_values = {"original": [], "visually calibrated": [], "estimated": []}

        # Colores asignados a cada tipo de calibración
        status_colors = {
            "original": "red",
            "visually calibrated": "blue",
            "estimated": "green"
        }

        for item in step_info.get("items", []):
            if all(k in item for k in ["Angular position", "Omega", "Phi", "Kappa", "Calibration_Status"]):
                status = item["Calibration_Status"]
                if status not in angular_positions:
                    continue  # Ignorar si hay un estado desconocido

                angular_positions[status].append(item["Angular position"])
                omega_values[status].append(item["Omega"])
                phi_values[status].append(item["Phi"])
                kappa_values[status].append(item["Kappa"])

        if not any(angular_positions.values()):  # Si no hay datos en ninguna categoría, continuar con la siguiente secuencia
            print(f"⚠️ No hay datos suficientes para graficar la secuencia {step_name}")
            continue

        # Crear subplots con 3 filas (Omega, Phi, Kappa)
        fig = make_subplots(rows=3, cols=1, shared_xaxes=True, subplot_titles=[
            f"Omega vs Angular Position ({step_name})",
            f"Phi vs Angular Position ({step_name})",
            f"Kappa vs Angular Position ({step_name})"
        ])

        # 📌 Agregar trazas por cada tipo de Calibration Status
        for status, color in status_colors.items():
            if angular_positions[status]:  # Solo graficar si hay datos para este estado
                fig.add_trace(go.Scatter(
                    x=angular_positions[status], y=omega_values[status],
                    mode="lines+markers", marker=dict(color=color), name=f"Omega ({status})"
                ), row=1, col=1)

                fig.add_trace(go.Scatter(
                    x=angular_positions[status], y=phi_values[status],
                    mode="lines+markers", marker=dict(color=color), name=f"Phi ({status})"
                ), row=2, col=1)

                fig.add_trace(go.Scatter(
                    x=angular_positions[status], y=kappa_values[status],
                    mode="lines+markers", marker=dict(color=color), name=f"Kappa ({status})"
                ), row=3, col=1)

        fig.update_layout(height=900, width=800, showlegend=True)

        all_figs.append(fig)

    if not all_figs:
        print("❌ No se generaron gráficos. Verifica que las secuencias tengan datos.")
        return None  # Gradio puede manejar None si no hay gráficos

    return all_figs[0]  # Devuelve solo el primer gráfico si hay múltiples secuencias
