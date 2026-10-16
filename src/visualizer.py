import plotly.graph_objects as go
import pandas as pd


def plot_line_loading(results_df: pd.DataFrame) -> go.Figure:
    """
    Erstellt ein 24-Stunden-Liniendiagramm für die maximale Leitungsauslastung
    inklusive der kritischen 100%-Grenze.
    """
    fig = go.Figure()

    # Maximale Leitungsauslastung
    fig.add_trace(go.Scatter(
        x=results_df["Stunde"],
        y=results_df["Max_Leitungsauslastung_%"],
        mode="lines+markers",
        name="Max. Auslastung",
        line=dict(color="#1f77b4", width=3)
    ))

    # 100%-Referenzlinie (thermische Belastungsgrenze)
    fig.add_hline(
        y=100.0,
        line_dash="dash",
        line_color="red",
        annotation_text="Überlastgrenze (100%)",
        annotation_position="bottom right"
    )

    fig.update_layout(
        title="Maximale Leitungsbelastung im Tagesverlauf",
        xaxis_title="Uhrzeit (Stunde)",
        yaxis_title="Auslastung (%)",
        template="plotly_white",
        hovermode="x unified"
    )
    return fig


def plot_voltage_profile(results_df: pd.DataFrame) -> go.Figure:
    """
    Erstellt ein Diagramm für das Spannungsband (Min/Max Knotenspannung)
    mit den DIN EN 50160 Grenzwerten (0.95 p.u. bis 1.05 p.u.).
    """
    fig = go.Figure()

    # Maximale Spannung
    fig.add_trace(go.Scatter(
        x=results_df["Stunde"],
        y=results_df["Max_Spannung_pu"],
        mode="lines+markers",
        name="Max. Knotenspannung",
        line=dict(color="#ff7f0e", width=2)
    ))

    # Minimale Spannung
    fig.add_trace(go.Scatter(
        x=results_df["Stunde"],
        y=results_df["Min_Spannung_pu"],
        mode="lines+markers",
        name="Min. Knotenspannung",
        line=dict(color="#2ca02c", width=2)
    ))

    # Grenzwerte (Spannungsband +/- 5% bzw. 10%)
    fig.add_hline(y=1.05, line_dash="dash", line_color="orange", annotation_text="Oberes Spannungsband (1.05 p.u.)")
    fig.add_hline(y=0.95, line_dash="dash", line_color="orange", annotation_text="Unteres Spannungsband (0.95 p.u.)")

    fig.update_layout(
        title="Knotenspannungsverlauf (Spannungsband DIN EN 50160)",
        xaxis_title="Uhrzeit (Stunde)",
        yaxis_title="Spannung (p.u.)",
        template="plotly_white",
        hovermode="x unified"
    )
    return fig



#zum testen

"""
from src.simulation import run_24h_simulation

sim_data = run_24h_simulation(pv_capacity_mw=3.5)
fig1 = plot_line_loading(sim_data)
fig1.show() 
# Öffnet die interaktive Grafik direkt im Webbrowser

"""