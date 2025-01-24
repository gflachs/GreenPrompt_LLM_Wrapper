import re
import subprocess

# Globale Variable zur Speicherung der Messdaten


def start_calc_sci_score():
    """
    Startet die Messung des Energieverbrauchs mit powerstat.
    """
    print("Messung mit powerstat gestartet...")
    powerstat_process = subprocess.Popen(
        ["powerstat", "1", "-d 0", "-z"],  # 1-Sekunden-Intervall
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    return powerstat_process


def end_calc_sci_score(powerstat_process, results_count,time_diff_in_ms, country_code="DE"):
    """
    Beendet die Messung und berechnet den SCI-Score basierend auf dem Powerstat-Summary.

    :param results_count: Anzahl der Ergebnisse (z. B. verarbeitete Anfragen).
    :param country_code: Ländercode zur Berechnung der Kohlenstoffintensität.
    :return: Berechneter SCI-Score.
    """

    if powerstat_process is None:
        raise RuntimeError("Messung wurde nicht gestartet. Rufen Sie start_calc_sci_score() auf.")

    # Powerstat beenden
    print("Messung beenden...")
    powerstat_process.terminate()
    stdout, stderr = powerstat_process.communicate()

    if stderr:
        print(f"Fehler bei powerstat: {stderr}")
        
    print(stdout)

    # Parse den Powerstat-Summary   
    energy_watts = parse_powerstat_summary(stdout)
    
    print(energy_watts)

    if energy_watts is None:
        raise RuntimeError("Konnte keinen gültigen Watt-Wert aus der powerstat-Ausgabe extrahieren.")

    # Berechnung der Energie in kWh
    duration_seconds = time_diff_in_ms / 1000  # Millisekunden => Sekunden
    energy_kwh = (energy_watts * duration_seconds) / 3600  # Watt * Sekunden => kWh

    # Kohlenstoffintensität holen
    grid_intensity = get_grid_intensity(country_code)

    # Hardware-Kohlenstoff berechnen
    hardware_carbon = calculate_hardware_carbon(energy_kwh, grid_intensity)

    # SCI-Score berechnen
    sci_score = calculate_sci(energy_kwh, grid_intensity, hardware_carbon, results_count)

    print("Messung beendet.")
    return sci_score


def parse_powerstat_summary(output):
    """
    Extrahiert den durchschnittlichen Watt-Wert aus dem Powerstat-Summary.

    :param output: Die gesamte Ausgabe von powerstat.
    :return: Durchschnittlicher Energieverbrauch in Watt (float) oder None, falls kein Wert gefunden wurde.
    """
    match = re.search(r"Summary:\s+System:\s+([\d.]+)\s+Watts", output)
    if match:
        return float(match.group(1))
    return None

def get_grid_intensity(country_code):
    """
    Gibt die Kohlenstoffintensität (gCO₂/kWh) basierend auf dem Ländercode zurück.
    """
    intensities = {
        "DE": 300,  # Germany
        "FR": 60,   # France
        "US": 400,  # United States
        "CN": 600   # China
    }
    return intensities.get(country_code.upper(), 300)


def calculate_hardware_carbon(E_kwh, I_gco2_per_kwh):
    """
    Berechnet die Hardwareemissionen (M) in gCO₂.
    """
    return E_kwh * I_gco2_per_kwh


def calculate_sci(E_kwh, I_gco2_per_kwh, M_gco2, R):
    """
    Berechnet den SCI-Score:
        SCI = ((E * I) + M) / R
    """
    usage_carbon = E_kwh * I_gco2_per_kwh
    total_carbon = usage_carbon + M_gco2
    return total_carbon / R
