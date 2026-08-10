import sqlite3
import pandas as pd
import streamlit as st

# Name der Datenbank-Datei
DB_FILE = "meine_datenbank.db"

# 1. Verbindung herstellen
# check_same_thread=False ist wichtig, da Streamlit Requests in verschiedenen Threads ausführt
def get_connection():
    return sqlite3.connect(DB_FILE, check_same_thread=False)

conn = get_connection()

# 2. Tabelle beim Start automatisch anlegen (falls sie noch nicht existiert)
with conn:
    conn.execute("""
        CREATE TABLE IF NOT EXISTS eintraege (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL
        )
    """)

# --- Streamlit Benutzeroberfläche ---
st.title("Meine SQLite App")

# Formular zum Einfügen von Daten
neuer_eintrag = st.text_input("Neuen Text eingeben:")
if st.button("Speichern"):
    if neuer_eintrag:
        with conn:
            conn.execute("INSERT INTO eintraege (text) VALUES (?)", (neuer_eintrag,))
        st.success("Erfolgreich gespeichert!")
        st.rerun()  # Lädt die Seite neu, damit die Liste sofort aktualisiert wird

# Daten aus der Datenbank auslesen und anzeigen
st.subheader("Bestehende Einträge")
df = pd.read_sql_query("SELECT * FROM eintraege", conn)
st.dataframe(df)
