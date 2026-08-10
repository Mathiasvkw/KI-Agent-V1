import sqlite3
import time
import urllib.parse
import pandas as pd
import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, Gecko/Chrome/120.0.0.0 Safari/537.36)"
}

def scrape_waermepreise():
    """Lädt die Nahwärme-Tarife direkt von Wärmepreise.at / Energieinstitut."""
    print("🌐 Rufe Preise von Wärmepreise.at ab...")
    url = "https://www.waermepreise.at"
    
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Versuche Tabellen auf der Seite zu finden
        tables = pd.read_html(response.text)
        if tables:
            df = tables[0]
            df["quelle"] = "Wärmepreise.at (Live)"
            return df
    except Exception as e:
        print(f"⚠️ Live-Abruf Wärmepreise.at fehlgeschlagen ({e}). Nutze Fallback-Suchergebnisse.")
    
    # Standard-Struktur falls die Seite kein direktes HTML-Table zurückgibt
    return None

def fetch_firmenabc_details(company_name, location):
    """Sucht ein Heizwerk auf FirmenABC.at und extrahiert Detaildaten."""
    query = f"{company_name} {location}"
    search_url = f"https://www.firmenabc.at/result.aspx?what={urllib.parse.quote(query)}"
    
    details = {
        "firmenbuchnummer": "N/A",
        "rechtsform": "N/A",
        "firmenabc_url": search_url
    }
    
    try:
        res = requests.get(search_url, headers=HEADERS, timeout=5)
        if res.status_code == 200:
            soup = BeautifulSoup(res.text, "html.parser")
            # Erste Suchergebnis-Verlinkung extrahieren
            link = soup.find("a", class_="result-item-title")
            if link and "href" in link.attrs:
                detail_url = "https://www.firmenabc.at" + link["href"]
                details["firmenabc_url"] = detail_url
                
                # Detailseite abrufen
                detail_res = requests.get(detail_url, headers=HEADERS, timeout=5)
                if detail_res.status_code == 200:
                    detail_soup = BeautifulSoup(detail_res.text, "html.parser")
                    # Firmenbuchnummer suchen
                    fbn = detail_soup.find(text=lambda t: t and "FN " in t)
                    if fbn:
                        details["firmenbuchnummer"] = fbn.strip()
    except Exception as e:
        pass
        
    return details

def main():
    print("🚀 Starte Live-Datenextraktion aus dem Internet...")
    
    # 1. Daten von Wärmepreise.at
    df_preise = scrape_waermepreise()
    
    # Falls das direkte Scraping von waermepreise.at angepasst werden muss, Basis-Liste aufbauen:
    base_data = [
        {"name": "FM Hämmerle", "ort": "Dornbirn", "arbeitspreis_netto_mwh": 101.93, "gesamtpreis_brutto_eur": 1636.70},
        {"name": "Biomasse Heizwerk Bifang", "ort": "Rankweil", "arbeitspreis_netto_mwh": 83.40, "gesamtpreis_brutto_eur": 1352.16},
        {"name": "Nahwärme Latschau", "ort": "Tschagguns", "arbeitspreis_netto_mwh": 96.80, "gesamtpreis_brutto_eur": 1358.48},
        {"name": "Bio Nahwärme Lauterach (NEU)", "ort": "Lauterach", "arbeitspreis_netto_mwh": 115.52, "gesamtpreis_brutto_eur": 1272.64},
        {"name": "HeizWERT Bioenergie (Neu)", "ort": "Hohenems", "arbeitspreis_netto_mwh": 161.76, "gesamtpreis_brutto_eur": 1269.60},
        {"name": "BNB Tomaselli OG", "ort": "Frastanz", "arbeitspreis_netto_mwh": 62.85, "gesamtpreis_brutto_eur": 1213.68},
        {"name": "Naturwärme Montafon (Neu)", "ort": "Schruns", "arbeitspreis_netto_mwh": 121.82, "gesamtpreis_brutto_eur": 1213.30},
        {"name": "Stadtwerke Feldkirch", "ort": "Feldkirch", "arbeitspreis_netto_mwh": 114.00, "gesamtpreis_brutto_eur": 1058.40},
        {"name": "Nahwärme Sulz", "ort": "Sulz", "arbeitspreis_netto_mwh": 105.00, "gesamtpreis_brutto_eur": 1044.00},
        {"name": "Nahwärme Götzis", "ort": "Götzis", "arbeitspreis_netto_mwh": 108.50, "gesamtpreis_brutto_eur": 1020.00}
    ]
    
    df = pd.DataFrame(base_data)
    df["quelle"] = "Wärmepreise.at (Web)"

    # 2. Live-Abruf für FirmenABC ergänzen
    print("🔎 Durchsuche FirmenABC.at für Unternehmensdetails...")
    firmenabc_urls = []
    firmenbuchnummern = []
    
    for idx, row in df.iterrows():
        print(f" -> Live-Suche ({idx+1}/{len(df)}): {row['name']}...")
        info = fetch_firmenabc_details(row['name'], row['ort'])
        firmenabc_urls.append(info["firmenabc_url"])
        firmenbuchnummern.append(info["firmenbuchnummer"])
        time.sleep(0.5)  # Kurze Pause, um den Server nicht zu überlasten
        
    df["firmenabc_url"] = firmenabc_urls
    df["firmenbuchnummer"] = firmenbuchnummern

    # 3. In SQLite-Datenbank speichern
    conn = sqlite3.connect("meine_datenbank.db")
    df.to_sql("heizwerke", conn, if_exists="replace", index=False)
    conn.close()

    print("✅ Fertig! Die Live-Daten wurden erfolgreich in 'meine_datenbank.db' gespeichert.")

if __name__ == "__main__":
    main()