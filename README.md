# GridPulse – Verteilnetz-Monitoring & Sensitivitätsanalyse

GridPulse ist mein erstes größeres Projekt, weil ich vorher nur sehr kleine pandapower Programme geschrieben hatte und ich hiermit zum ersten Mal etwas größeres erstellt habe. Damit ich jetzt einmal gesehen habe, wie so etwas aussehen kann und mir jetzt selber von vorne bis hinten ein großes Projekt erstellen kann. Damit erhoffe ich mir, dass dies das erste von vielen Projekten jetzt sein wird.

---

Interaktives Analysetool zur netztechnischen Bewertung von Photovoltaik-Ausbaupfaden in Verteilnetzen. Das Projekt modelliert ein standardisiertes CIGRE-Mittelspannungsnetz (20 kV) und führt stundenbasierte AC-Leistungsflussrechnungen durch, um Spannungsbandverletzungen und Leitungsengpässe transparent darzustellen.

---

## Funktionen

* **AC-Leistungsflussrechnung:** Physikalisch exakte Berechnung über das Newton-Raphson-Verfahren (`pandapower`).
* **24-Stunden-Ganglinien:** Automatisierte Überlagerung synthetischer PV-Erzeugungsprofile mit typischen Haushaltslastkurven.
* **Normkonforme Grenzwerte:** Überwachung der Spannungsbänder nach DIN EN 50160 ($0.95 \le U \le 1.05\ \text{p.u.}$) sowie der thermischen Leitungsauslastungen ($> 100\%$).
* **Interaktives Dashboard:** Webbasiertes Frontend via Streamlit mit Plotly-Diagrammen und Echtzeit-KPIs bei variabler PV-Leistung.

---

## Python libraries

* **Netzberechnung:** `pandapower`, `scipy`
* **Datenverarbeitung:** `pandas`, `numpy`
* **Web-App & Dashboard:** `streamlit`
* **Visualisierung:** `plotly`

---

## Filesstructure

```text
gridpulse/
├── data/                  # Datenablage & Profile
├── src/
│   ├── __init__.py
│   ├── grid_factory.py    # Erstellung des CIGRE-Netzes & Netzelemente
│   ├── simulation.py      # 24-Stunden-Simulation & Leistungsfluss
│   └── visualizer.py      # Plotly-Visualisierungen für Spannungen & Ströme
├── app.py                 # Streamlit-Webanwendung
├── requirements.txt       # Abhängigkeiten
└── README.md              # Projektdokumentation
