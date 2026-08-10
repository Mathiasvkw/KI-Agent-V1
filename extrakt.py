import sqlite3
import pandas as pd

print("⚡ Speichere die 45 Heizwerke in der Datenbank...")

# Die aus der Excel-Datei gefilterten Heizwerke (Wärmepreise.at / FirmenABC)
heizwerke_liste = [
    ('FM Hämmerle', 'Dornbirn', 'Wärmepreise.at'),
    ('Biomasse Heizwerk Bifang', 'Rankweil', 'Wärmepreise.at'),
    ('Nahwärme Latschau', 'Tschagguns', 'Wärmepreise.at'),
    ('Bio Nahwärme Lauterach (NEU)', 'Lauterach', 'Wärmepreise.at'),
    ('HeizWERT Bioenergie (Neu)', 'Hohenems', 'Wärmepreise.at'),
    ('BNB Tomaselli OG', 'Frastanz', 'Wärmepreise.at'),
    ('Naturwärme Montafon (Neu)', 'Schruns', 'Wärmepreise.at'),
    ('NW Schetteregg Standard', 'Schetteregg', 'Wärmepreise.at'),
    ('Naturwärme Montafon (Alt)', 'Schruns', 'Wärmepreise.at'),
    ('Bio Nahwärme Lauterach (Alt) 01', 'Lauterach', 'Wärmepreise.at'),
    ('Fernwärme Ludesch', 'Ludesch', 'Wärmepreise.at'),
    ('Stadtwerke Feldkirch', 'Feldkirch', 'Wärmepreise.at'),
    ('Nahwärme Sulz', 'Sulz', 'Wärmepreise.at'),
    ('Nahwärme Götzis', 'Götzis', 'Wärmepreise.at'),
    ('Bio Wärme Frastanz', 'Frastanz', 'Wärmepreise.at'),
    ('Bioenergie Kleinwalsertal', 'Kleinwalsertal', 'Wärmepreise.at'),
    ('Heizwerk Oberlech 2024-2025', 'Oberlech', 'Wärmepreise.at'),
    ('Gemeinde Altach', 'Altach', 'Wärmepreise.at'),
    ('Wälderbau Energie GmbH', 'Schwarzenberg', 'Wärmepreise.at'),
    ('vkw Nahwärme Dornbirn (Ilg)', 'Dornbirn', 'Wärmepreise.at'),
    ('Holzheizwerk Stadt Dronbirn (2024)', 'Dornbirn', 'Wärmepreise.at'),
    ('Gemeinde Blons', 'Blons', 'Wärmepreise.at'),
    ('Biomasse Heizwerk Bezau', 'Bezau', 'Wärmepreise.at'),
    ('Biomasse Heizwerk Damüls', 'Damüls', 'Wärmepreise.at'),
    ('BWR Biomasse Rankweil', 'Rankweil', 'Wärmepreise.at'),
    ('Gemeinde Schnifis', 'Schnifis', 'Wärmepreise.at'),
    ('HeizWERT Bioenergie (alt)', 'Hohenems', 'Wärmepreise.at'),
    ('Biomasse Heizwerk Zürs', 'Zürs', 'Wärmepreise.at'),
    ('Gemeinde Düns', 'Düns', 'Wärmepreise.at'),
    ('Biomasse Fernwärme Sulzberg', 'Sulzberg', 'Wärmepreise.at'),
    ('Nahwärme Hard', 'Hard', 'Wärmepreise.at'),
    ('Biomasse Heizwerk Mellau', 'Mellau', 'Wärmepreise.at'),
    ('Biomasse Heizwerk Au eGEN 2024', 'Au', 'Wärmepreise.at'),
    ('Gemeinde Langen bei Bregenz', 'Langen', 'Wärmepreise.at'),
    ('Biomasse Heizwerk Lech', 'Lech', 'Wärmepreise.at'),
    ('Biomasse Heizwerk Alberschwende', 'Alberschende', 'Wärmepreise.at'),
    ('Holzheizwerk Stadt Dronbirn (2023)', 'Dornbirn', 'Wärmepreise.at'),
    ('Biomasse Heizwerk Au eGEN 2023', 'Au', 'Wärmepreise.at'),
    ('Gemeinde Altach Tarif 2', 'Altach', 'Wärmepreise.at'),
    ('Biomasse Heizwerk Zug', 'Lech', 'Wärmepreise.at'),
    ('Hilbe Nahwärme', 'Dornbirn', 'Wärmepreise.at'),
    ('Biomasse Heizwerk Bürs', 'Bürs', 'Wärmepreise.at'),
    ('Gemeinde Innerbraz', 'Innerbraz', 'Wärmepreise.at'),
    ('Gemeinde Altach Tarif 3', 'Altach', 'Wärmepreise.at'),
    ('Gemeinde Altach Tarif 4', 'Altach', 'Wärmepreise.at')
]

# DataFrame erstellen
df = pd.DataFrame(heizwerke_liste, columns=['name', 'ort', 'quelle'])

# In SQLite-Datenbank speichern
conn = sqlite3.connect("meine_datenbank.db")
df.to_sql("heizwerke", conn, if_exists="replace", index=False)
conn.close()

print(f"✅ Erfolgreich {len(df)} Heizwerke in der Datenbank gespeichert!")