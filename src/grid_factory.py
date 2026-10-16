import pandapower as pp
import pandapower.networks as pn


def build_network():
    """
    Lädt ein standardisiertes CIGRE-Mittelspannungsnetz
    mit dezentralen Erzeugern (PV und Wind) 
    ein Schaubild ist unter diesem link verfügbar: 
    https://www.pandapower.org/networks.html#cigre-mv
    """
    net = pn.create_cigre_network_mv(with_der="pv_wind")
    """
    pn.create_cigre_network_mv() erstellt ein standardisiertes 
    Mittelspannungsnetz ohne with_der="pv_wind" hätte das Netz 
    nur Leitungen, Transormatoren und standard Stromverbraucher.
    Außerdem hätte die tabelle für net.sgen wäre leer und der 
    Strom würde nur in eine Richtung fließen, mit 
    with_der="pv_wind" werden dezentrale Erzeuger (PV und Wind) 
    hinzugefügt, die den Stromfluss in beide Richtungen lenken
    (weil an manchen Masten/Knoten stehen jetzt schon 
    Solaranlagen und Windkraftanlagen die bereits Leistung ins 
    Netz einspeisen) with_der="pv_wind" ist eine default Eingabe
    mit einer für die Netzgröße angemessenen Anzahl an Erzeugern
    """
    return net
    #ohne net würde das erstellte Netz nicht außerhalb der 
    #Funktion existieren und wir hätten keinen Zugriff drauf

def add_custom_pv(net, bus_index: int, p_mw: float, q_mvar: float = 0.0):
    """
    Jetzt füge ich an einem ausgewählten Netzknoten eine PV-Anlage 
    hinzu und die Werte werden in der if __name__ == "__main__": 
    übergeben.

    net ist das Datenpaket meines gesamten Netzes und weil es das
    Datenpaket nur verändert und nicht neu erstellt, muss ich es nicht 
    "zurückgeben"

    bus=bus_index ist der Knoten (Adresse) dem die PV-Anlage hinzugefügt 
    wird und überings gibt in unserem default Cigre Netz 0-14 Knoten und 
    bus_index=5

    p_mw: float ist der Wert der Wirkleistung, dabei steht das P für Active 
    Power (Wirkleistung) und MW für Mega Watt, also 10^6 Watt.
    und noch ein kleiner Hinweis die Vorzeichen-Konvention in pandapower: 
    Bei Generatoren (sgen) bedeutet ein positiver Wert, dass Energie in das
    Netz eingespeist wird (im Gegensatz zu Lasten in net.load, wo positive 
    Werte Entnahme bedeuten)

    q_mvar: float ist der Wert der Blindleistung, dabei steht das Q für 
    Reactive Power (Blindleistung) und MVar für Mega Volt Ampere Reactive 
    (Mvar), standmäßig ist die Blindleistung 0,0 MVar, weil wir nur Wirkleistung
    eingespeist wird 
    noch ein weiterer Hinweis:Wenn durch viel PV die Spannung an einem Knoten 
    zu hoch wird, kann man hier oft einen negativen Wert einstellen 
    (untererregter Betrieb), um die Spannung künstlich wieder nach unten zu ziehen

    sgen_id = pp.create_sgen(), dass sgen steht für static generator (statische 
    Erzeuger), dies nutzt man für alles was über einen Wechselrichter einspeist,
    weil es keine rotierende Turbinenmasse gibt
    pp.create_sgen hängt eine neue Zeile an net.sgen an
    die Rückgabe sgen_id ist einfach der Index (die Zeilennummer) diser neuen 
    Anlage (zB 9 oder 10), damit man diese einfach wiederfinden kann
    """
    sgen_id = pp.create_sgen(
        net,
        bus=bus_index,
        p_mw=p_mw,
        q_mvar=q_mvar,
        name=f"Zusatz_PV_Bus_{bus_index}",
        type="PV"
    )
    return sgen_id


#die main function ist nur als Test gedacht, um zu wissen ob de
#Code funtioniert

def main():
    net = build_network()
    add_custom_pv(net, bus_index=5, p_mw=2.0)
    #add_custom_pv() ist eine Funktion die 

    pp.runpp(net)
    #pp.runpp() führt eine nichtlineare Leistungsflussberechnung durch, die die 
    # Spannungen an allen Knoten und die Ströme in allen Leitungen berechnet
    print("Fertig berechnet!")


main()