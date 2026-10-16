import numpy as np
import pandas as pd
import pandapower as pp
from src.grid_factory import build_network, add_custom_pv


#diese Datei ist basicly meine main

def create_daily_profiles():
    """
    Erzeugt 24-Stunden-Normprofile (Faktoren zwischen 0.0 und 1.0)
    für Sonnenstrahlung und Haushaltslast.
    """
    hours = np.arange(24)

    # PV-Profil: Glockenkurve zwischen 6 und 20 Uhr mit Peak um 13 Uhr, also kurzgesagt
    # die PV-Erzeugung  
    pv_profile = np.maximum(0.0, np.sin((hours - 6) / 14 * np.pi)) ** 2
    pv_profile[hours < 6] = 0.0
    pv_profile[hours > 20] = 0.0

    # Lastprofil: Morgen- und Abendspitze (typisches Haushaltsverhalten),
    # dass ist einfach die Last
    load_profile = 0.4 + 0.3 * np.exp(-((hours - 8) ** 2) / 8) + 0.5 * np.exp(-((hours - 19) ** 2) / 8)

    df_profiles = pd.DataFrame({
        "hour": hours,
        "pv_factor": pv_profile,
        "load_factor": load_profile
    })
    #dass erstellt basicly einfach eine Art "excel" Tabelle
    return df_profiles


def run_24h_simulation(pv_capacity_mw: float = 3.0):
    """
    Führt für 24 Zeitschritte/Stunden jeweils eine Leistungsflussrechnung durch
    """
    net = build_network()
    #hier wird das Netz erstellt/aufgerufen was wir mit der build_network()
    #Funktion erstellt haben
    pv_id = add_custom_pv(net, bus_index=5, p_mw=pv_capacity_mw)

    profiles = create_daily_profiles()

    #jetzt sind einmal Daten erstellt, jetzt kommen wir dann zur Berechnung

    base_loads = net.load["p_mw"].copy()
    """
    aufgedröselt bedeutet dies:
    1. net.load: Das gesamte Tabellenblatt (der Pandas-DataFrame) 
    für alle Verbraucher
    2. net.load["p_mw"]: Greift sich gezielt nur die Spalte mit der 
    Wirkleistung heraus (in Pandas eine sogenannte Series, 
    also eine 1D-Liste mit Index)
    3. .copy(): Erstellt ein komplett eigenständiges Duplikat dieser 
    Spaltenwerte und speichert es in base_loads ab

    und damit bleibt base_loads unverändert
    """

    # leere Ergebnislisten für die 24 Stunden
    max_line_loading = []
    max_bus_voltage = []
    min_bus_voltage = []

    """
    max_line_loading: der Auslastungswert der am stärksten
    belasteten Leitung (in %) (Zeigt, ob irgendwo im Netz ein 
    Kabel zu heiß wird (Gefahr ab >100%))

    max_bus_voltage: die höchste Spannung im gesamten Netz (in p.u.)
    (Zeigt die Spannungsspitze (meist mittags an Knoten 5 wegen der 
    PV-Einspeisung).)

    min_bus_voltage: die niedrigste Spannung im gesamten Netz (in p.u.)
    (Zeigt den stärksten Spannungseinbruch (meist abends, wenn alle 
    Haushalte kochen)
    """


    for step in range(24):
        #range(24) erzeugt eine Liste von 0 bis 23
        # 1. Profile anwenden
        pv_scale = profiles.loc[step, "pv_factor"]
        load_scale = profiles.loc[step, "load_factor"]

        # PV-Leistung und Lasten für diese Stunde setzen
        net.sgen.at[pv_id, "p_mw"] = pv_capacity_mw * pv_scale
        net.load["p_mw"] = base_loads * load_scale

        # 2. Leistungsfluss rechnen
        pp.runpp(net)

        # 3. Kennzahlen mitschreiben
        max_line_loading.append(net.res_line["loading_percent"].max())
        max_bus_voltage.append(net.res_bus["vm_pu"].max())
        min_bus_voltage.append(net.res_bus["vm_pu"].min())

    results_df = pd.DataFrame({
        "Stunde": profiles["hour"],
        "Max_Leitungsauslastung_%": max_line_loading,
        "Max_Spannung_pu": max_bus_voltage,
        "Min_Spannung_pu": min_bus_voltage
    })

    return results_df