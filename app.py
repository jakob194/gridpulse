import streamlit as st
from src.simulation import run_24h_simulation
from src.visualizer import plot_line_loading, plot_voltage_profile

# 1. Seitenkonfiguration & Header
st.set_page_config(
    page_title="GridPulse - Netzmonitoring",
    page_icon="⚡",
    layout="wide"
)

st.title("⚡ GridPulse: Verteilnetz-Monitoring & Flexibilitäts-Dashboard")
st.markdown("""
Dieses Tool simuliert ein CIGRE-Mittelspannungsnetz über 24 Stunden. 
Passe in der linken Leiste die installierte **PV-Leistung** an und beobachte, 
wie sich Leitungsbelastungen und Knotenspannungen verhalten.
""")

# 2. Seitenleiste für Benutzereingaben
st.sidebar.header("⚙️ Simulationsparameter")

pv_capacity = st.sidebar.slider(
    label="Installierte PV-Leistung an Knoten 5 (MW):",
    min_value=0.0,
    max_value=10.0,
    value=3.5,
    step=0.5,
    help="Erhöhe die Einspeiseleistung, um Spannungsbandverletzungen und Überlastungen zu provozieren."
)

# 3. Simulation berechnen
with st.spinner("Berechne 24-Stunden-Leistungsfluss..."):
    results_df = run_24h_simulation(pv_capacity_mw=pv_capacity)

# 4. Wichtigste Kennzahlen (KPI-Karten)
max_load = results_df["Max_Leitungsauslastung_%"].max()
max_u = results_df["Max_Spannung_pu"].max()
min_u = results_df["Min_Spannung_pu"].min()

col1, col2, col3 = st.columns(3)

with col1:
    delta_text = "Überlastung!" if max_load > 100.0 else "Im Normbereich"
    st.metric(
        label="Höchste Leitungsbelastung",
        value=f"{max_load:.1f} %",
        delta=delta_text,
        delta_color="inverse"
    )

with col2:
    voltage_violation_high = max_u > 1.05
    st.metric(
        label="Maximale Spannung",
        value=f"{max_u:.3f} p.u.",
        delta="Spannung zu hoch!" if voltage_violation_high else "Konform",
        delta_color="inverse" if voltage_violation_high else "normal"
    )

with col3:
    voltage_violation_low = min_u < 0.95
    st.metric(
        label="Minimale Spannung",
        value=f"{min_u:.3f} p.u.",
        delta="Spannung zu niedrig!" if voltage_violation_low else "Konform",
        delta_color="inverse" if voltage_violation_low else "normal"
    )

st.divider()

# 5. Diagramme ausgeben
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    fig_loading = plot_line_loading(results_df)
    st.plotly_chart(fig_loading, use_container_width=True)

with chart_col2:
    fig_voltage = plot_voltage_profile(results_df)
    st.plotly_chart(fig_voltage, use_container_width=True)

# 6. Tabellarische Daten einblenden
with st.expander("Detaillierte Stundendaten anzeigen"):
    st.dataframe(results_df, use_container_width=True)



#dashboard starten in gridpulse/ aber vorher die vitual 
#environment aktivieren
#streamlit run app.py aber wieder in gridpulse