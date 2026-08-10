import sqlite3
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Heizwerke Übersicht", layout="wide")

st.title("🔥 Übersicht der Heizwerke in Vorarlberg")
st.caption("Tarifdaten & Finanzdaten (FirmenABC)")

# Daten sicher aus SQLite laden
@st.cache_data
def load_data():
    try:
        conn = sqlite3.connect("meine_datenbank.db")
        df = pd.read_sql_query("SELECT * FROM heizwerke", conn)
        conn.close()
        return df
    except Exception:
        # Falls die Tabelle noch nicht existiert, leeres DataFrame zurückgeben
        return pd.DataFrame(columns=[
            "Heizwerk", "Ort", "Arbeitspreis", "Grundpreis", 
            "Bilanzsumme", "Bilanzgewinn", "Anlagevermögen", "Eigenkapital"
        ])

df = load_data()

# Wenn die Tabelle leer ist, Hinweis anzeigen
if df.empty:
    st.warning("⚠️ Keine Datenbank oder Tabelle 'heizwerke' gefunden.")
    st.info("Bitte führe einmalig folgenden Befehl im Terminal aus, um die Daten zu generieren:")
    st.code("python extrakt.py", language="bash")
else:
    # Filter & Suche
    col1, col2 = st.columns(2)
    with col1:
        ort_filter = st.multiselect("Nach Ort filtern:", sorted(df["Ort"].unique()))
    with col2:
        suchbegriff = st.text_input("Nach Heizwerk suchen:", "")

    gefiltert = df.copy()

    if ort_filter:
        gefiltert = gefiltert[gefiltert["Ort"].isin(ort_filter)]
    if suchbegriff:
        gefiltert = gefiltert[gefiltert["Heizwerk"].str.contains(suchbegriff, case=False, na=False)]

    st.divider()

    spalten = [
        "Heizwerk", "Ort", "Arbeitspreis", "Grundpreis", 
        "Bilanzsumme", "Bilanzgewinn", "Anlagevermögen", "Eigenkapital"
    ]

    st.dataframe(
        gefiltert[spalten],
        column_config={
            "Arbeitspreis": st.column_config.NumberColumn("Arbeitspreis (€/MWh)", format="%.2f €"),
            "Grundpreis": st.column_config.NumberColumn("Grundpreis (€/kW*a)", format="%.2f €"),
        },
        hide_index=True,
        use_container_width=True
    )